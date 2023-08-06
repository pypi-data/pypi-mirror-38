from abc import abstractmethod


class JsonAble:
    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(dic):
        pass
