from data2code_sdk.plugin.interface_plugin import IPlugin
from abc import abstractmethod
from data2code_sdk.plugin.output_data import OutputData
from typing import List
from data2code_sdk.plugin.parsed_result import BaseParsedData


class IProcessorPlugin(IPlugin):
    @abstractmethod
    def process(self, parsed_data: BaseParsedData, params: any, results: List[OutputData]):
        """
        数据处理插件
        :param parsed_data: 分析后的数据（可能无，如果没有分析插件）
        :param params: 参数
        :param results: 处理结果集
        :return:
        """
        pass

