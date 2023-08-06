from tests.signal_test import SignalTest


def handle_func(a, b):
    print(f"common func ==> a:{a}, b:{b}")


class A:
    @staticmethod
    def static_handler(a, b):
        print(f"static handler:a: {a}, b:{b}")

    def __init__(self, v):
        self.__v = v

    def handler(self, a, b):
        print(f"member handler, {self.__v} ==> a:{a}, b:{b}")


sig: SignalTest = SignalTest()
sig.on(handle_func)
sig.on(A.static_handler)

inst = A(">in class Signal Test<")
sig.on(inst.handler)

sig1: SignalTest = SignalTest()
sig1.dispatch("str a", "str b")

print("+++++++ now off some ++++++")

sig2: SignalTest = SignalTest()
sig2.off(handle_func)
sig1.off(A.static_handler)
# sig.off(inst.handler)

sig.dispatch("second a", "second b")





