from data2code_sdk.config.interface_config import IConfig


class TestConfig(IConfig):
    @property
    def is_valid(self):
        return True

    def to_dict(self):
        pass

    def from_dict(dic):
        pass


dic = dict()
dic["test1"] = "haha"
dic["test2"] = "haha2"
for k, v in dic.items():
    print("k:" + k + ", v:" + v)
    # print("k:" + k )

