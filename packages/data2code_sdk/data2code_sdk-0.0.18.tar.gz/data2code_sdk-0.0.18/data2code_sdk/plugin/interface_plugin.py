from rigger_plugin_framework.plugin import Plugin
from abc import abstractmethod
from data2code_sdk.config.interface_config import IConfig


class IPlugin(Plugin):
    def __init__(self):
        self.__config = None

    @abstractmethod
    def plugin_type(self):
        pass

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def set_config(self, config: IConfig):
        self.__config = config

    def get_config(self):
        return self.__config



