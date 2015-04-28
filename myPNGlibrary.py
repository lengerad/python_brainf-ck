__author__ = 'radimsky'
import zlib
import sys


class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass


class pngHandler():

    def __init__(self, path):
        with open(path, 'rb') as file:
            self.binaryData = file.read()

        # print(self.binaryData)
        self.createArray()


    def checkHeader(self, binaryData):
        if (binaryData[:8] != b'\x89PNG\r\n\x1a\n'):
            raise PNGWrongHeaderError()
            sys.exit(4)
        else:
            self.binaryData = binaryData[8:]
            return self


    def parseBinaryData(self):
        pointer = 0
        dataLength = 0;
        self.pngData = []

        while pointer < len(self.binaryData):
            dataLength = int.from_bytes(self.binaryData[pointer:pointer + 4], byteorder='big', signed='False')
            # print (dataLength)
            pointer += 4
            self.pngData += [{'chunkType': self.binaryData[pointer:pointer + 4],
                              'chunkData': self.binaryData[pointer + 4:pointer + 4 + dataLength]}]
            pointer += 8 + dataLength

    def decodeIHDR(self):
        for chunk in self.pngData:
            if chunk['chunkType'] == b'IHDR':
                self.imageLength = int.from_bytes(chunk['chunkData'][0:4], byteorder='big', signed='False')
                self.imageHeight = int.from_bytes(chunk['chunkData'][4:8], byteorder='big', signed='False')
                controlBytes = byteDepth = int.from_bytes(chunk['chunkData'][9:13], byteorder='big', signed='False')

        if controlBytes != 33554432:
            raise PNGNotImplementedError
            sys.exit(8)

    def getIDATData(self):
        self.decompressedData = []
        for chunk in self.pngData:
            if chunk['chunkType'] == b'IDAT':
                self.decompressedData += zlib.decompress(chunk['chunkData'])

    def filterMeDude(self, filterType, pixel):
        if filterType == 0:
            return pixel
        if filterType == 1:
            pass
        if filterType == 2:
            pass

        if filterType == 3:
            pass

        if filterType == 4:
            pass


    def createArray(self):
        self.checkHeader(self.binaryData)
        self.parseBinaryData()
        self.decodeIHDR()
        self.getIDATData()
        print(self.decompressedData)

        self.pictureArray = [[0 for i in range(self.imageLength)] for i in range(self.imageHeight)]
        width = 0;
        height = 0;
        pointer = 0;

        for i in range(0, self.imageHeight):
            filter = self.decompressedData[pointer]
            pointer += 1
            for j in range(0, self.imageLength):
                pixel = (
                self.decompressedData[pointer], self.decompressedData[pointer + 1], self.decompressedData[pointer + 2])
                self.pictureArray[i][j] = self.filterMeDude(filter, pixel)
                pointer += 3

        print(self.pictureArray)
