class BatchRequest:
    """
    批量上传请求
    """

    def __init__(self):
        self.method = ""
        self.path = ""
        self.body = {}
        pass

    method = "POST"
    path = "/1/classes/"
    body = {}
