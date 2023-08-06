class PluginType:
    """
    插件类型的定义
    """
    LOADER = "LOADER"   # 加载数据的插件，必需
    PARSER = "PARSER"   # 对数据进行分析的插件
    PROCESSOR = "PROCESSOR"  # 对数据进行最终处理的插件, 但一般不会直接使用此标记

