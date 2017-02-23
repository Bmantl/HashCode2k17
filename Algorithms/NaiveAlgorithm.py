
def getKey(item):
    return item[3]

class NaiveAlgorithm:
    def __init__(self):
        pass

    # def lol(self):
    #     scoreTuples = self.scoreTuples(caches, videos, endpoints)
    #     maxScoreTuples = sorted(scoreTuples, key=getKey)
    #     maxScoreTuples.reverse()
    #
    #     for endpointIndex, videoIndex, cacheIndex, score in maxScoreTuples:
    #         if caches[cacheIndex].remainingSpace < videos[videoIndex].size or \
    #             videoIndex in caches[cacheIndex].videos:
    #             continue
    #
    #         caches[cacheIndex].remainingSpace = \
    #             caches[cacheIndex].remainingSpace - videos[videoIndex].size
    #         caches[cacheIndex].videos.append(videoIndex)
    #         endpoints[endpointIndex].videoRequests.pop(videoIndex, None)

    def main(self, caches, videos, endpoints):
        scoreTuples = self.scoreTuples(caches, videos, endpoints)
        lastLen = 0

        while len(scoreTuples) != lastLen and len(scoreTuples) != 0:
            print len(scoreTuples)
            lastLen = len(scoreTuples)

            maxScoreTuples = sorted(scoreTuples, key=getKey)
            maxScoreTuples.reverse()
            maxScoreTuples = maxScoreTuples[:50]

            for endpointIndex, videoIndex, cacheIndex, score in maxScoreTuples:
                if caches[cacheIndex].remainingSpace < videos[videoIndex].size or\
                    videoIndex in caches[cacheIndex].videos:
                    continue

                caches[cacheIndex].remainingSpace = \
                    caches[cacheIndex].remainingSpace - videos[videoIndex].size
                caches[cacheIndex].videos.append(videoIndex)

                endpoints[endpointIndex].videoRequests.pop(videoIndex, None)

            scoreTuples = self.scoreTuples(caches, videos, endpoints)


    def scoreTuples(self, caches, videos, endpoints):
        requestsScore = []
        endpointIndex = 0

        for endpoint in endpoints:
            for videoIndex, requests in endpoint.videoRequests.iteritems():
                cacheIndex, latency = \
                    self.maxCacheForRequest(endpoint, videos[videoIndex].size, caches)

                if cacheIndex is None:
                    continue

                requestsScore.append(
                    (endpointIndex, videoIndex, cacheIndex,
                     requests * (endpoint.dataCenterLatency - latency)))

            endpointIndex += 1

        return requestsScore

    def maxCacheForRequest(self, endpoint, videoSize, caches):
        cacheIndices = endpoint.cacheServersLatency.keys()

        validCachesIndices = filter(lambda cacheIndex:
            caches[cacheIndex].remainingSpace >= videoSize, cacheIndices)

        if len(validCachesIndices) == 0:
            return None, None

        cachesTuple = [(cacheIndex, endpoint.cacheServersLatency[cacheIndex]) \
                for cacheIndex in validCachesIndices]

        maxTuple = reduce((lambda currentMaxCacheTuple, cacheTuple:
            currentMaxCacheTuple if currentMaxCacheTuple[1] > cacheTuple[1]
            else cacheTuple), cachesTuple)

        return maxTuple


