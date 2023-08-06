class OutputData:
    """
    输出数据的说明
    """
    def __init__(self):
        # 处理者
        # 应用可能根据处理者进行不同的操作，如最终文件的导出路径
        self.processor = None
        # 文件名
        self.file_name = None
        # 文件内容
        self.content = ""
