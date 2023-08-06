from data2code_sdk.plugin.interface_plugin import IPlugin
from abc import abstractmethod


class IUIPlugin(IPlugin):
    def process(self):
        raise Exception("please use on_app_start")

    @abstractmethod
    def on_app_start(self, callback):
        pass
