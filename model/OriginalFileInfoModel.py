class OriginalFileInfoModel:
    """
    原始文件信息
    """

    def __init__(self, original_download_url):
        self.original_download_url = original_download_url
        pass

    # 原始图片下载地址
    original_download_url = ""
    # 原始图片宽度
    original_width = 0
    # 原始图片高度
    original_height = 0
    # 原始图片文件大小
    original_file_size = 0
    # 原始图片格式
    original_file_format = ""
