from Models.CacheServer import CacheServer
from Models.Video import Video
from Models.Endpoint import Endpoint


class Parser:
    def __init__(self):
        pass

    def parseFile(self, filename):
        with open(filename) as f:
            content = [map(int, l.split()) for l in f.readlines()]

            videos, endpointsNum, requestsNum, cachesNum, cachesSize = content[0]

            self.caches = self.initCaches(cachesNum, cachesSize)
            self.videos = self.initVideos(content[1])
            self.endpoints, startLine = self.initEndpoints(endpointsNum, content)
            self.initRequests(content, requestsNum, startLine)

            return self.caches, self.videos, self.endpoints

    def initCaches(self, cachesNum, size):
        return map(lambda x: CacheServer(size), xrange(cachesNum))

    def initVideos(self, videosSizes):
        return [Video(vSize) for vSize in videosSizes]

    def initEndpoints(self, endpointsNum, content):
        endpoints = []
        endpointIndex = 0
        nextStartLine = 2
        for endpointsNum in xrange(endpointsNum):
            endpoint, nextStartLine = \
                self.initEndpoint(nextStartLine, content, endpointIndex)
            endpointIndex += 1
            endpoints.append(endpoint)

        return endpoints, nextStartLine + 1

    def initEndpoint(self, endpointStartLine, content, endpointIndex):
        dataCenterLatency, cachesNum = content[endpointStartLine]

        endpoint = Endpoint(dataCenterLatency)

        for cache in xrange(cachesNum):
            endpointStartLine += 1
            cacheIndex, cacheLatency = content[endpointStartLine]
            endpoint.cacheServersLatency[cacheIndex] = cacheLatency
            self.caches[cacheIndex].endpoints[endpointIndex] = cacheLatency

        return endpoint, endpointStartLine + 1

    def initRequests(self, content, requestsNum, startLine):
        requestLine = startLine
        for _ in xrange(requestsNum - 1):
            videoIndex, endpointIndex, requestAmount = content[requestLine]

            self.videos[videoIndex].endpointsRequests[endpointIndex] = \
                requestAmount
            self.endpoints[endpointIndex].videoRequests[videoIndex] = requestAmount

            requestLine += 1
