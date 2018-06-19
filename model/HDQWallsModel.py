class HDQWallsModel:
    """
    hdqwalls数据对象
    """

    def __init__(self, create_timestamp):
        self.create_timestamp = create_timestamp
        self.title = ""
        self.detail_url = ""
        self.category_list = []
        self.category_list_cn = []
        self.author = ""
        self.author_link = ""
        self.original_resolution = ""
        self.original_file_info = {}
        self.update_timestamp = 0
        pass

    # 名称
    title = ""
    # 详情页地址
    detail_url = ""
    # 分类列表
    category_list = []
    # 分类列表-中文
    category_list_cn = []
    # 拥有者
    author = ""
    # 拥有者主页id
    author_link = ""
    # 原始分辨率
    original_resolution = ""
    # 源文件信息
    original_file_info = {}
    # 数据创建时间
    create_timestamp = 0
    # 数据更新时间
    update_timestamp = 0
