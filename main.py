import sys

from Parser.parser import Parser
from Algorithms.NaiveAlgorithm import NaiveAlgorithm

if __name__ == '__main__':
    parser = Parser()

    for filename in sys.argv[1:]:
        caches, videos, endpoints = parser.parseFile(sys.argv[1])

        # print caches
        # print [video.endpointsRequests for video in videos]
        # print [endpoint.videoRequests for endpoint in endpoints]

        algorithm = NaiveAlgorithm()
        algorithm.main(caches, videos, endpoints)

        with open(filename + '_result', 'w') as file:
            cachesWithVideo = filter(lambda cache: len(cache.videos) != 0, caches)

            file.write(str(len(cachesWithVideo)) + '\n')
            cacheIndex = 0
            for cache in cachesWithVideo:
                if len(cache.videos) == 0:
                    cacheIndex += 1
                    continue

                file.write(str(cacheIndex))

                for videoIndex in cache.videos:
                    file.write(' ' + str(videoIndex))

                file.write('\n')
                cacheIndex += 1

