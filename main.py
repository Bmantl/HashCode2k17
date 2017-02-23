import sys

from Parser.parser import Parser

if __name__ == '__main__':
    parser = Parser()

    caches, videos, endpoints = parser.parseFile(sys.argv[1])

    print caches
    print [video.endpointsRequests for video in videos]
    print [endpoint.videoRequests for endpoint in endpoints]