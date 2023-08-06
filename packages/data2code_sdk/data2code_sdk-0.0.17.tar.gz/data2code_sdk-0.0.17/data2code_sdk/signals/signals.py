from data2code_sdk.signals.signal import Signal
from rigger_singleton.singleton import singleton
from data2code_sdk.config.project_config import ProjectConfig
from typing import List
from data2code_sdk.plugin.output_data import OutputData


@singleton
class OnConfigLoadSignal(Signal):
    """
    配置加载完成的信号
    """
    def dispatch(self, configs: List[ProjectConfig]):
        super().dispatch(configs)


@singleton
class StartToProcessSignal(Signal):
    """
    通知开始进行处理（数据）的信号
    """
    pass


@singleton
class OnProcessFinishSignal(Signal):
    """
    (数据）处理完成的信号
    """
    def dispatch(self, results: List[OutputData]):
        super().dispatch(results)


@singleton
class OnAppExitSignal(Signal):
    """
    应用退出时的信号
    """
    pass


@singleton
class OnAppStartSignal(Signal):
    """
    应用启动时的信号
    """
    pass

