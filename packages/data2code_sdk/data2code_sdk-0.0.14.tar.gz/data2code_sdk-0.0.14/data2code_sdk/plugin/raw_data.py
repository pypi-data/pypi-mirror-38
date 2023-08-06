
class RawData:
    def __init__(self, data_name: str):
        self.__datas = []
        self.__data_name = data_name

    @property
    def data_name(self):
        return self.__data_name

    @data_name.setter
    def data_name(self, data_name: str):
        self.__data_name = data_name

    @property
    def length(self):
        return len(self.__datas)

    def get(self, idx: int):
        if self.length <= idx:
            return None

        return self.__datas[idx]

    def append(self, data):
        self.__datas.append(data)
