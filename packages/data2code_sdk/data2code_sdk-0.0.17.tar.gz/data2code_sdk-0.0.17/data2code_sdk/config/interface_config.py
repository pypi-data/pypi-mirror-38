from data2code_sdk.config.jsonable import JsonAble
from abc import abstractmethod


class IConfig(JsonAble):
    """
    所有配置文件的基类
    """

    @abstractmethod
    def is_valid(self):
        """
        配置是否有效
        子类必须实现
        :return:
        """
        pass

