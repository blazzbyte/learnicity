from .config import Config
from .logger import Logger

config = Config()

logger = Logger()

__all__ = ['config', 'logger']