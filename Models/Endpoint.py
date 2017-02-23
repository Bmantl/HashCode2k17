

class Endpoint:
    def __init__(self, dataCenterLatency):
        self.dataCenterLatency = dataCenterLatency
        self.cacheServersLatency = {}
        self.videoRequests = {}