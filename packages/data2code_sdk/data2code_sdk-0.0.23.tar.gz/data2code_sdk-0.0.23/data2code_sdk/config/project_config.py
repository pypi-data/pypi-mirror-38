from data2code_sdk.config.interface_config import IConfig


class ProjectConfig(IConfig):
    """
    项目配置类
    """
    __slots__ = (
        "project_name",
        "data_dir",
        "plugin_configs",
    )

    def __init__(self):
        self.project_name = None
        self.data_dir = None
        self.plugin_configs = dict()

    @property
    def is_valid(self):
        if self.project_name is None:
            raise Exception("project name could not be None")

        return True

    @staticmethod
    def to_dict(obj):
        print("extra:", obj)
        return {
            "project_name": obj.project_name,
            "data_dir": obj.data_dir,
            "plugin_configs": obj.plugin_configs
        }

    @staticmethod
    def from_dict(dic: dict):
        obj = ProjectConfig()
        obj.project_name = dic["project_name"]
        obj.data_dir = dic["data_dir"]
        obj.plugin_configs = dic["plugin_configs"]

        return obj

