"""Logger utility for recommendation application.
"""
import tomli as toml
from logging import config
import logging


class Logger:
    """Logger class for recommendation system.

    Attributes:
        toml_file_path (str): Path to project TOML file.
    """

    def __init__(self, toml_file_path: str):
        """
        Method initiliases toml file path.

        Args:
            toml_file_path (str, optional): Path to project TOML file.
        """
        try:
            self.toml_file_path = toml_file_path
        except Exception as e:
            raise e

    def setup(self):
        """Method uses project's TOML file to set logging configuration.

        Returns:
            Logger: Python Logging object.

        Raises:
            e: Raise in case of any exception.
        """
        try:
            with open(self.toml_file_path, "rb") as stream:
                toml_dict = toml.load(stream)

            tool_logging_dict = toml_dict.get("tool").get("logging")
            config.dictConfig(tool_logging_dict)
            return logging.getLogger("recosys")

        except Exception as e:
            raise e
