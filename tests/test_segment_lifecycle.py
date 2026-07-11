from __future__ import annotations

import asyncio
import unittest
from collections import deque

from spatius.proto.generated import message_pb2

from livekit import rtc
from livekit.plugins.spatius.avatar import AvatarSession


class _FakeSpatiusSession:
    def __init__(self, request_ids: list[str]) -> None:
        self._request_ids = iter(request_ids)

    async def send_audio(self, *, audio: bytes, end: bool) -> str:
        return next(self._request_ids)


class _FakeAudioBuffer:
    def __init__(self) -> None:
        self.completions: list[tuple[float, bool]] = []

    def notify_playback_finished(self, playback_position: float, interrupted: bool) -> None:
        self.completions.append((playback_position, interrupted))


class SegmentLifecycleTest(unittest.IsolatedAsyncioTestCase):
    def _new_session(self, request_ids: list[str]) -> tuple[AvatarSession, _FakeAudioBuffer]:
        session = AvatarSession.__new__(AvatarSession)
        session._spatius_session = _FakeSpatiusSession(request_ids)
        audio_buffer = _FakeAudioBuffer()
        session._audio_buffer = audio_buffer
        session._segments = []
        session._request_segments = {}
        session._pending_segments = deque()
        session._active_segment = None
        session._segment_finalize_lock = asyncio.Lock()
        return session, audio_buffer

    @staticmethod
    def _audio_frame() -> rtc.AudioFrame:
        return rtc.AudioFrame.create(
            sample_rate=24000,
            num_channels=1,
            samples_per_channel=480,
        )

    @staticmethod
    def _completion_frame(request_id: str) -> bytes:
        message = message_pb2.Message()
        message.type = message_pb2.MESSAGE_SERVER_RESPONSE_ANIMATION
        message.server_response_animation.req_id = request_id
        message.server_response_animation.end = True
        return message.SerializeToString()

    async def test_provider_completion_before_flush_notifies_once(self) -> None:
        session, audio_buffer = self._new_session(["request-1", "request-1"])

        await session._send_audio_frame(self._audio_frame())
        session._on_transport_frame(self._completion_frame("request-1"), is_last=True)
        self.assertEqual(audio_buffer.completions, [])

        await session._finalize_active_segment(source="segment_end")
        self.assertEqual(len(audio_buffer.completions), 1)

        session._on_transport_frame(self._completion_frame("request-1"), is_last=True)
        self.assertEqual(len(audio_buffer.completions), 1)

    async def test_request_id_change_within_livekit_segment_notifies_once(self) -> None:
        session, audio_buffer = self._new_session(["request-1", "request-2", "request-2"])

        await session._send_audio_frame(self._audio_frame())
        await session._send_audio_frame(self._audio_frame())
        await session._finalize_active_segment(source="segment_end")

        session._on_transport_frame(self._completion_frame("request-1"), is_last=True)
        self.assertEqual(audio_buffer.completions, [])

        session._on_transport_frame(self._completion_frame("request-2"), is_last=True)
        self.assertEqual(len(audio_buffer.completions), 1)

    async def test_timeout_and_provider_completion_cannot_double_notify(self) -> None:
        session, audio_buffer = self._new_session(["request-1", "request-1"])

        await session._send_audio_frame(self._audio_frame())
        await session._finalize_active_segment(source="segment_end")
        segment = session._pending_segments[0]

        self.assertTrue(session._complete_segment(segment=segment, interrupted=False, reason="timeout"))
        session._on_transport_frame(self._completion_frame("request-1"), is_last=True)

        self.assertEqual(len(audio_buffer.completions), 1)
