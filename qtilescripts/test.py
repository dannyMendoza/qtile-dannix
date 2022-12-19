from libqtile.config import Key
from libqtile.lazy import lazy
from libqtile.log_utils import logger

@lazy.function
def multiply(qtile, value, multiplier=10):
    logger.warning(f"Multiplication results: {value * multiplier}")
