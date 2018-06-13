from model import OriginalFileInfoModel


class HDQWallsModel:
    """
    hdqwalls数据对象
    """

    def __init__(self, create_timestamp, update_timestamp):
        self.create_timestamp = create_timestamp
        self.update_timestamp = update_timestamp
        pass

    # 名称
    name = ""
    # 详情页地址
    detail_url = ""
    # 分类列表
    category_list = []
    # 拥有者
    author = ""
    # 拥有者主页id
    author_link = ""
    # 原始分辨率
    original_resolution = ""
    # 源文件信息（需要将OriginalFileInfoModel数据对象转成dict然后赋值）
    original_file_info = OriginalFileInfoModel()
    # 数据创建时间
    create_timestamp = 0
    # 数据更新时间
    update_timestamp = 0
