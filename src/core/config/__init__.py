from .config import Config, get_translation
from .logger import Logger

config = Config()

logger = Logger()

__all__ = ['config', 'logger', 'get_translation']