from typing import List
from data2code_sdk.plugin.raw_data import RawData


class ProcessPluginDescriptor:
    def __init__(self, plugin_tag: str):
        self.__plugin_tag: str = plugin_tag
        self.__plugin_params: any = None

    @property
    def plugin_tag(self):
        return self.__plugin_tag

    @property
    def plugin_params(self):
        return self.__plugin_params

    @plugin_params.setter
    def plugin_params(self, params: any):
        self.__plugin_params = params


class BaseParsedData:
    def __init__(self, raw_data: RawData):
        # self.__data_name: str = data_name
        self.__raw_data: RawData = raw_data
        self.__processor_plugins: List[ProcessPluginDescriptor] = []

    @property
    def data_name(self):
        return self.raw_data.data_name

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def processor_plugins(self):
        return self.__processor_plugins

    @processor_plugins.setter
    def processor_plugins(self, plugins: List[ProcessPluginDescriptor]):
        self.__processor_plugins = plugins


# 唯一键描述符
class KVDescriptor:
    keys: List[str]
    value_index: int

    def __init__(self):
        self.keys = []
        self.value_index = None


# 合并键描述符
class MergeKVDescriptor:
    def __init__(self):
        # 合并键的索引列表
        self.key_indexs: List[int] = []
        # 合并的行索引，是一个二维数组
        self.value_indexs: List[List[int]] = []


class DefaultParsedData(BaseParsedData):
    """
    分析后的数据，应用本身不处理此数据，由后续插件处理，因此也可以用其它的数据格式表示分析后的数据
    如果没有分析插件，则没有此数据
    """
    def __init__(self, raw_data: RawData):
        super().__init__(raw_data)

        self.file_name: str = None
        self.types: List[str] = []
        # 键的描述列表: True: 唯一键, False: 不是任何键, 任何字符串: 合并键标签，具有同样标签的键可以合并
        self.key_descriptors: List[bool or str] = []
        self.field_names: List[str] = []
        self.field_comments: List[str] = []
        self.field_values: List[List[str]] = []
        # 唯一键列表（索引)
        self.unique_keys: List[int] = []
        # 合并键映射，以合并tag为键
        self.merge_kv_descriptor_map = dict()  # {"merge_tag": str, "merge_kv_descriptor": MergeKVDescriptor}
        # self.keys: List[str] = []
