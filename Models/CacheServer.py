

class CacheServer:
    def __init__(self, MAX_SIZE):
        self.MAX_SIZE = MAX_SIZE
        self.endpoints = {}
        self.videos = []
        self.remainingSpace = MAX_SIZE