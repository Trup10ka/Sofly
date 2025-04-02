import os
import shutil

from abc import abstractmethod, ABC

from loguru import logger

from src.config.sofly_config import SoflyConfig


class ConfigLoader(ABC):
    """
    Abstract class for loading configuration files. This class cannot be instantiated directly.

    Each subclass **must** implement the `load_config` method to load the configuration file
    """
    def __new__(cls, *args, **kwargs):
        """
        The class is not instantiated if:
            - The class is ``ConfigLoader`` (abstract class).
            - The number of arguments is not ``1``.
            - The argument passed is not a ``string``.
        Parameters
        ----------
        args
        kwargs
        """
        if cls is ConfigLoader:
            raise TypeError("ConfigLoader is an abstract class and cannot be instantiated directly.")
        if len(args) != 1:
            raise TypeError("ConfigLoader requires a single argument: the path to the configuration file.")
        if not isinstance(args[0], str):
            raise TypeError("The path to the configuration file must be a string.")

        return super().__new__(cls)

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def copy_default_confi_if_not_exists(self) -> bool:
        """
        Copy the default configuration file to the specified path if it does not already exist.
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        default_config_path = os.path.join(project_root, ".data", "default_config.conf")

        if not os.path.exists(default_config_path):
            logger.critical("The default configuration file does not exist.")
            return False

        if not os.path.exists(self.config_file_path):
            shutil.copy(default_config_path, self.config_file_path)
            return True
        return False

    @abstractmethod
    def load_config(self) -> SoflyConfig:
        pass