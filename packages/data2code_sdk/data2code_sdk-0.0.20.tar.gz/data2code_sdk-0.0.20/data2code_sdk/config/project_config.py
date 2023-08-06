from data2code_sdk.config.interface_config import IConfig


class ProjectConfig(IConfig):
    """
    项目配置类
    """
    __slots__ = (
        "project_name",
        "data_dir",
        "server_dir",
        "client_dir",
        "server_language",
        "client_language"
    )

    def __init__(self):
        self.project_name = None
        self.data_dir = None
        self.server_dir = None
        self.client_dir = None
        self.server_language = None
        self.client_language = None

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
            "server_dir": obj.server_dir,
            "client_dir": obj.client_dir,
            "server_language": obj.server_language,
            "client_language": obj.client_language
        }

    @staticmethod
    def from_dict(dict):
        obj = ProjectConfig()
        obj.project_name = dict["project_name"]
        obj.data_dir = dict["data_dir"]
        obj.server_dir = dict["server_dir"]
        obj.client_dir = dict["client_dir"]
        obj.server_language = dict["server_language"]
        obj.client_language = dict["client_language"]

        return obj

