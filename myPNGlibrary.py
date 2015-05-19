__author__ = 'radimsky'
import zlib, traceback, sys

class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass


class pngHandler():
    def __init__(self, path):
        with open(path, 'rb') as file:
            self.binaryData = file.read()

        # print(self.binaryData)
        self.imageWidth = 0
        self.imageHeight = 0
        self.pictureType = 'none'
        self.a = (0, 0, 0)
        self.b = (0, 0, 0)
        self.c = (0, 0, 0)
        self.createArray()
        self.decompressedData = []
        self.recognizePicture()


    def checkHeader(self, binaryData):
        if binaryData[:8] != b'\x89PNG\r\n\x1a\n':
            try:
                raise PNGNotImplementedError()
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(8)
        else:
            self.binaryData = binaryData[8:]
            return self

    def recognizePicture(self):
        for i in range(0, self.imageHeight):
            for j in range(0, self.imageWidth):
                for x in range(0, 3):
                    if (self.pictureArray[i][j][x] != 255 and self.pictureArray[i][j][x] != 128 and
                                self.pictureArray[i][j][x] != 0):
                        self.pictureType = "koptera"
                        return
        self.pictureType = "loler"


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
                self.imageWidth = int.from_bytes(chunk['chunkData'][0:4], byteorder='big', signed='False')
                self.imageHeight = int.from_bytes(chunk['chunkData'][4:8], byteorder='big', signed='False')
                controlBytes = int.from_bytes(chunk['chunkData'][9:13], byteorder='big', signed='False')

        if controlBytes != 33554432:
            try:
                raise PNGNotImplementedError()
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(8)

    def getIDATData(self):
        tempData = b''
        for chunk in self.pngData:
            if chunk['chunkType'] == b'IDAT':
                tempData += chunk['chunkData']
        self.decompressedData = zlib.decompress(tempData)

    def reconstructPixel(self, filterType, pixel):
        if filterType == 0:
            self.a = pixel;
            return pixel
        if filterType == 1:
            self.a = self.sumBytes(pixel, self.a)
            return self.a
        if filterType == 2:
            return self.sumBytes(pixel, self.b)
        if filterType == 3:
            self.a = self.sumBytes(pixel, self.sumBytes(self.a, self.b) / 2)
            return self.a
        if filterType == 4:
            self.a = self.sumBytes(pixel, self.paethPredictor(self.a, self.b, self.c))
            return self.a

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
        # print(self.decompressedData)

        self.pictureArray = [[0 for i in range(self.imageWidth)] for i in range(self.imageHeight)]
        pointer = 0;
        for i in range(0, self.imageHeight):
            self.a = (0, 0, 0)
            self.b = (0, 0, 0)
            self.c = (0, 0, 0)
            filter = self.decompressedData[pointer]
            pointer += 1
            for j in range(0, self.imageWidth):
                if i > 0:
                    self.b = self.pictureArray[i - 1][j]
                if i > 0 and j > 0:
                    self.c = self.pictureArray[i - 1][j - 1]
                pixel = (
                    self.decompressedData[pointer], self.decompressedData[pointer + 1],
                    self.decompressedData[pointer + 2])
                self.pictureArray[i][j] = self.reconstructPixel(filter, pixel)
                pointer += 3
