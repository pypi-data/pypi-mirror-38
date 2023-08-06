class Signal:
    """
    一个简单的信号类
    子类一般建议用单例模式
    """
    __slots__ =(
        "__handlers",
    )

    def __init__(self):
        self.__handlers = []

    def on(self, handler):
        self.__handlers.append(handler)

    def off(self, handler):
        """
        移除回调，如果有多个，则一次只移除一个
        :param handler:
        :return:
        """
        temp = []
        has_done = False
        for h in self.__handlers:
            if h != handler:
                temp.append(h)
            else:
                if has_done:
                    temp.append(h)
                else:
                    has_done = False

        self.__handlers = temp

    def dispatch(self, *args):
        """
        派发信号
        :param args:
        :return:
        """
        for handler in self.__handlers:
            handler(*args)
