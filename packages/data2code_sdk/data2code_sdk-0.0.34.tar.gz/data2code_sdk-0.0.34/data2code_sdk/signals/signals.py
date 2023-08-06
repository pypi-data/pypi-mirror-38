from data2code_sdk.signals.signal import Signal
from rigger_singleton.singleton import singleton
from data2code_sdk.config.project_config import ProjectConfig
from typing import List
from data2code_sdk.plugin.output_data import OutputData
from data2code_sdk.plugin.interface_plugin import IPlugin


@singleton
class ConfigLoadedSignal(Signal):
    """
    配置加载完成的信号
    """
    def dispatch(self, configs: List[ProjectConfig]):
        super().dispatch(configs)


@singleton
class SaveConfigSignal(Signal):
    """
    请求保存配置的信号
    收到此信号后，APP会保存传递的配置
    """
    def dispatch(self, config: ProjectConfig):
        super().dispatch(config)


@singleton
class SaveConfigFinishedSignal(Signal):
    """
    保存配置完成时的信号
    """
    def dispatch(self, config: ProjectConfig):
        super().dispatch(config)


@singleton
class RemoveConfigSignal(Signal):
    def dispatch(self, config_name: str):
        super().dispatch(config_name)


@singleton
class RemoveConfigFinishedSignal(Signal):
    def dispatch(self, config_name: str):
        super().dispatch(config_name)


@singleton
class UpdateConfigsSignal(Signal):
    """
    配置有更新时的信号
    """
    def dispatch(self, configs: List[ProjectConfig]):
        super().dispatch(configs)


@singleton
class StartToProcessSignal(Signal):
    """
    通知开始进行处理（数据）的信号
    """
    def dispatch(self, project_name: str=None):
        super().dispatch(project_name)


@singleton
class ProcessFinishedSignal(Signal):
    """
    (数据）处理完成的信号
    """
    def dispatch(self, results: List[OutputData]):
        super().dispatch(results)


@singleton
class AppExitSignal(Signal):
    """
    应用退出时的信号
    """
    pass


@singleton
class AppStartSignal(Signal):
    """
    应用启动时的信号
    """
    pass


@singleton
class RequestToInstallPluginSignal(Signal):
    """
    请求安装指定插件
    """
    def dispatch(self, path: str):
        super().dispatch(path)


@singleton
class InstallPluginFinishedSignal(Signal):
    def dispatch(self, plugin: IPlugin):
        super().dispatch()


@singleton
class PluginInfoUpdateSignal(Signal):
    """
    插件信息更新的信号
    会传送当前所有的插件信息
    """
    def dispatch(self, plugin_classes: List, plugin_instances: List[IPlugin]):
        super().dispatch(plugin_classes, plugin_instances)


# @singleton
# class LackOfNecessaryPlugin(Signal):
#     """
#     应用缺少必要插件时的信号
#     """
#     def dispatch(self, plugin_tye):
#         super().dispatch(plugin_tye)


@singleton
class ExceptionSignal(Signal):
    """
    出现异常时的信号
    """
    def dispatch(self, error_code: int, *params):
        super().dispatch(error_code, *params)

    # def on(self, handler):
    #     raise Exception("you should use on_")

    # def on_exception(self, error_code, caller):
    #     pass

