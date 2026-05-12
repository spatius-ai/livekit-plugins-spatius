# LiveKit Agents Plugin for Spatius Avatar

LiveKit Agents plugin for [Spatius](https://www.spatius.ai) avatar sessions. It forwards TTS audio from a LiveKit agent session to Spatius and lets the avatar publish synchronized audio/video back into the same room.

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

`AvatarSession` defaults to `region="us-west"` and composes Spatius endpoints from that region. To use another region:

```python
avatar = spatius.AvatarSession(region="us-east")
```

Explicit endpoint URLs still override region:

```python
avatar = spatius.AvatarSession(
    console_endpoint_url="https://console.example.com/v1/console",
    ingress_endpoint_url="wss://api.example.com/v2/driveningress",
)
```

For detailed usage, see [Spatius docs](https://docs.spatius.ai).

## License

MIT
