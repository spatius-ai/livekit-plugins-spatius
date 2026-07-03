"""Spatius avatar plugin for LiveKit Agents."""

from importlib.metadata import PackageNotFoundError, version

from spatius import AudioFormat

from .avatar import AvatarSession, SpatiusException

try:
    __version__ = version("livekit-plugins-spatius")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "AudioFormat",
    "AvatarSession",
    "SpatiusException",
    "__version__",
]

from livekit.agents import Plugin

from .log import logger


class SpatiusPlugin(Plugin):
    def __init__(self) -> None:
        super().__init__(__name__, __version__, __package__, logger)


Plugin.register_plugin(SpatiusPlugin())
