from spider import DataParseSpider, DownloadSpider, TranslateSpider, UploadSpider

# 入口
if __name__ == "__main__":
    print("开始解析数据")
    DataParseSpider.parse_paging(DataParseSpider.START_PAGING_INDEX, True)
    print("开始翻译分类名次")
    TranslateSpider.collection_word()
    print("开始下载壁纸")
    DownloadSpider.download_file()
    print("开始上传数据到bmob")
    UploadSpider.page_upload(UploadSpider.START_PAGE, UploadSpider.MAX_BATCH)
    print("开始上传壁纸到oss")
    UploadSpider.upload_file()
    print("数据处理完成")
    pass
