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
        self.a = (0, 0, 0)
        self.b = (0, 0, 0)
        self.c = (0, 0, 0)


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

    def reconstructPixel(self, filterType, pixel):
        if filterType == 0:
            return pixel
        if filterType == 1:
            return self.sumBytes(pixel, self.a)
        if filterType == 2:
            return self.sumBytes(pixel, self.b)
        if filterType == 3:
            return self.sumBytes(pixel, self.sumBytes(self.a, self.b) / 2)
        if filterType == 4:
            return self.sumBytes(pixel, self.paethPredictor(self.a, self.b, self.c))

    def sumBytes(self, pixel, pixel2):
        return ((pixel[0] + pixel2[0]) % 256, (pixel[1] + pixel2[1]) % 256, (pixel[2] + pixel2[2]) % 256)


    def paethPredictor(self, pixelA, pixelB, pixelC):
        newA = self.paeth(pixelA[0], pixelB[0], pixelC[0])
        newB = self.paeth(pixelA[1], pixelB[1], pixelC[1])
        newC = self.paeth(pixelA[2], pixelB[2], pixelC[2])
        return (newA, newB, newC)

    def paeth(self, a, b, c):
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        elif pb <= pc:
            return b
        else:
            return c

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
                self.pictureArray[i][j] = self.reconstructPixel(filter, pixel)
                pointer += 3

        print(self.pictureArray)
