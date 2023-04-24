import json
import os
from dataclasses import dataclass
from api.core.exceptions import ConfigError


@dataclass
class Settings():
    APP_ENV: str = "development"
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8080
    SERVER_WORKERS: int = 1
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "info"
    API_URL: str = "https://api.nbp.pl/api"


def get_settings() -> Settings:
    """
    Loads configuration options from a JSON file based on the current environment.
    """

    if os.getenv("APP_ENV") is None or os.getenv("APP_ENV") == "production":
        print("Loading production configuration...")
        config_file = "appsettings.json"
    else:
        print("Loading development configuration...")
        config_file = "appsettings.development.json"
    try:
        with open(f"./app/{config_file}", "r") as f:
            config_json = f.read()
        config_dict = json.loads(config_json)
        config = Settings(**config_dict)
    except (FileNotFoundError, ValueError) as e:
        raise ConfigError(f"Error loading configuration: {e}")
    return config


config = get_settings()
