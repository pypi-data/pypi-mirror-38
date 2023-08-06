from data2code_sdk.plugin.interface_plugin import IPlugin
from abc import abstractmethod
from data2code_sdk.plugin.raw_data import RawData
from data2code_sdk.plugin.parsed_result import BaseParsedData
from typing import List


class IParserPlugin(IPlugin):
    """
    data2code 应用的分析插件的接口类，规定了必须要实现的接口
    """
    @abstractmethod
    def process(self, raw_data: RawData, results: List[BaseParsedData]):
        """

        :param raw_data: 加载后的原始数据
        :param results: 处理后的结果集
        :return:
        """
        pass






