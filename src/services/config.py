import json
import os

from src.services.logger import Logger

logger = Logger(name="Config Service").get_logger()


class Config:
    def __init__(self, config_file=None):
        """
        Args:
            config_file (str): path to JSON file with configuration.
        """
        self.config = {
            "llm_api_key": "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",
            "vdb_collection": "examples_vectorstore",
            "vdb_api_url": "http://qdrant:6333",
        }
        if config_file:
            self.load_from_file(config_file)
        # TODO: load from env file?

    def load_from_file(self, config_file):
        """
        Load configrations from JSON file

        Args:
            config_file (str): path to JSON file with configuration.
        """
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except FileNotFoundError:
            logger.warning(
                f"Config file not found: {config_file}. Using default configuration."
            )
        except json.JSONDecodeError:
            logger.warning(f"Error decoding the configuration file {config_file}.")

    def load_from_env(self):
        """
        From environment variables
        # TODO: implement all config variables
        """
        env_config = {"llm_api_key": os.getenv("llm_api_key")}
        self.config.update({k: v for k, v in env_config.items() if v is not None})

    def get(self, key):
        """
        Given a config key, return the value

        Args:
            key (str): configuration key

        Returns:
            configuration value
        """
        if key in self.config:
            return self.config[key]
        else:
            logger.warning(f"Configuration key {key} not found.")
        return None

    def current(self):
        """
        Return current configuration

        """
        return self.config

    def set(self, key, value):
        """
        Set a config value

        Args:
            key (str): Config key
            value: value to set
        """
        self.config[key] = value

    def __str__(self):
        """
        Return a string representation of the configuration
        """
        return json.dumps(self.config, indent=4)
