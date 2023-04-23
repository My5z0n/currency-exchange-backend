import json
import os
from dataclasses import dataclass


@dataclass
class Settings():
    APP_ENV: str = "development"
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    SERVER_WORKERS: int = 1
    DEBUG_MODE: bool = False
    LOG_LEVEL: str = "info"
    API_URL: str = "https://api.nbp.pl/api"


def get_settings() -> Settings:
    """
    Loads configuration options from a JSON file based on the current environment.
    """
    print("----------------------------------------------")
    if os.getenv("MY_APP_ENV") is None or os.getenv("MY_APP_ENV") == "production":
        config_file = "appsettings.json"
    else:
        config_file = "config.development.json"
    try:
        with open(f"./app/{config_file}", "r") as f:
            config_json = f.read()
        config_dict = json.loads(config_json)
        config = Settings(**config_dict)
    except (FileNotFoundError, ValueError) as e:
        raise Exception(f"Error loading configuration: {e}")
    return config


config = get_settings()
