from abc import abstractmethod, ABC

from src.config.config import SoflyConfig


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

    @abstractmethod
    def load_config(self) -> SoflyConfig:
        pass