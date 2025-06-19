import logging
import os
import platform
from logging.handlers import RotatingFileHandler

APP_NAME = "PromptLab"
LOG_LEVEL = os.environ.get("PROMPTLAB_LOG_LEVEL", "INFO").upper()

# Determine platform-specific log directory
if os.environ.get("PROMPTLAB_LOG_DIR"):
    LOG_DIR = os.environ["PROMPTLAB_LOG_DIR"]
elif platform.system() == "Windows":
    LOG_DIR = os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), APP_NAME, "Logs"
    )
elif platform.system() == "Darwin":
    LOG_DIR = os.path.expanduser(f"~/Library/Logs/{APP_NAME}/")
else:  # Linux and other
    LOG_DIR = os.path.expanduser(f"~/.{APP_NAME.lower()}/logs/")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "promptlab.log")

LEVEL = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=10)
file_handler.setLevel(LEVEL)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(LEVEL)
console_handler.setFormatter(formatter)

logging.basicConfig(level=LEVEL, handlers=[file_handler, console_handler])

logger = logging.getLogger("promptlab")
logger.setLevel(LEVEL)
