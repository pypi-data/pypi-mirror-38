class Request:

    def __init__(self):
        self.headers = None
        self.rawData = None
        self.path = None
        self.timeout = None
        self.service = None
        self.function = None
        self.pathParts = None
        self.data = None
        pass

    def Validate(self):
        if self.headers is None:
            return False
        self.rawData = self.data
        self.data = self.rawData.data
        headers = dict()
        for i in self.headers.headers:
            name, value = i
            headers[name.decode("utf-8")] = value.decode("utf-8")
        self.headers = headers
        self.pathParts = self.headers[":path"].split("/")[1:]
        self.path = self.headers[":path"]
        self.timeout = self.headers["grpc-timeout"]
        self.getServiceAndFunction()
        return True
    
    def getServiceAndFunction(self):
        self.service = self.pathParts[0].split(".")[-1]
        self.function = self.pathParts[-1]
        pass