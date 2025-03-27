import os

from .config import Config

CODYSSI_DIR = "CODYSSI_DIR"
CODYSSI_TOKEN = "CODYSSI_TOKEN"  # nosec B105
CODYSSI_CONFIG_TOML = "CODYSSI_CONFIG_TOML"

if CODYSSI_CONFIG_TOML not in os.environ:
    os.environ[CODYSSI_CONFIG_TOML] = "pyproject.toml"

CONFIG = Config(os.environ[CODYSSI_CONFIG_TOML])
