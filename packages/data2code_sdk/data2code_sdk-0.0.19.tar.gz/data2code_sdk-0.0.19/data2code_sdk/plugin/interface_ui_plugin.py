from data2code_sdk.plugin.interface_plugin import IPlugin
from abc import abstractmethod
from data2code_sdk.plugin.plugin_type import PluginType


class IUIPlugin(IPlugin):
    @staticmethod
    def get_plugin_type():
        return PluginType.UI

    def process(self):
        raise Exception("please use on_app_start")

    @abstractmethod
    def on_app_start(self, callback):
        pass
