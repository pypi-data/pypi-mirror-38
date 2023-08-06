from abc import abstractmethod
from data2code_sdk.plugin.interface_plugin import IPlugin
from typing import List
from data2code_sdk.plugin.raw_data import RawData
from data2code_sdk.plugin.plugin_type import PluginType


class ILoaderPlugin(IPlugin):
    @staticmethod
    def get_plugin_type():
        return PluginType.LOADER

    @abstractmethod
    def process(self, path: chr, results: List[RawData]):
        """
        加载指定文件，并转换成 RawData数据类型，方便后续处理
        :param path: 文件路径,包含文件名
        :param results:[RawData]
        :return:
        """
        pass
