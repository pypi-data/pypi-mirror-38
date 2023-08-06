from data2code_sdk.signals.signal import Signal
from rigger_singleton.singleton import singleton


@singleton
class SignalTest(Signal):
    pass

