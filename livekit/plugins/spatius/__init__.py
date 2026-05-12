"""Spatius avatar plugin for LiveKit Agents.

This plugin provides integration with Spatius's avatar service for
lip-synced avatar rendering in LiveKit voice agents.

See https://docs.spatius.ai for more information.

Usage:
    from livekit.plugins.spatius import AvatarSession

    avatar = AvatarSession()
    await avatar.start(agent_session, room=ctx.room)
"""

from importlib.metadata import PackageNotFoundError, version

from .avatar import AvatarSession, SpatiusException

try:
    __version__ = version("livekit-plugins-spatius")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "AvatarSession",
    "SpatiusException",
    "__version__",
]

# Try to register plugin if Plugin class is available (livekit-agents >= 1.3)
try:
    from livekit.agents import Plugin

    from .log import logger

    class SpatiusPlugin(Plugin):
        """LiveKit plugin registration shim for Spatius avatar support."""

        def __init__(self) -> None:
            super().__init__(__name__, __version__, __package__, logger)

    Plugin.register_plugin(SpatiusPlugin())
except (ImportError, AttributeError):
    # Plugin registration not available in older versions
    pass
