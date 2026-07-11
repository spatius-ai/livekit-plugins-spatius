# LiveKit Agents Plugin for Spatius Avatar

LiveKit Agents plugin for [Spatius](https://www.spatius.ai) avatar sessions. It forwards TTS audio from a LiveKit agent session to Spatius and lets the avatar publish synchronized audio and motion data back into the same room.

## Client-side rendering

Spatius avatars are rendered on the client instead of being sent as conventional
server-rendered video. The avatar's LiveKit video track carries motion data in
otherwise black frames, so a standard LiveKit video renderer will display a black
screen. Your frontend must use the Spatius client SDK and LiveKit adapter to decode
the track and render the avatar.

See the [client integration guide](https://docs.spatius.ai/livekit-agents/client) and
the [reference frontend](https://github.com/spatius-ai/spatius-avatar-demo/tree/main/platform-integrations/livekit-agents-demo/livekit-agents-reference-demo/frontend)
for a working implementation.

## Installation

```bash
pip install livekit-plugins-spatius
```

## Quick Start

Set credentials:

```bash
export SPATIUS_API_KEY=your-api-key
export SPATIUS_APP_ID=your-app-id
export SPATIUS_AVATAR_ID=your-avatar-id

export LIVEKIT_URL=wss://your-livekit-host
export LIVEKIT_API_KEY=your-livekit-api-key
export LIVEKIT_API_SECRET=your-livekit-api-secret
```

Use plugin in your LiveKit agent:

```python
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import spatius


class VoiceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice assistant.")


async def entrypoint(ctx: JobContext) -> None:
    await ctx.connect()

    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=llm,
        tts=tts,
    )

    avatar = spatius.AvatarSession()
    await avatar.start(session, room=ctx.room)

    await session.start(agent=VoiceAssistant(), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

For detailed usage, see the [Spatius LiveKit Agents documentation](https://docs.spatius.ai/livekit-agents/overview).

## License

MIT
