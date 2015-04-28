__author__ = 'radimsky'


class WrongHeaderException(Exception):
    pass


class pngHandler():

    def __init__(self, path):
        with open(path, 'rb') as file:
            self.binaryData = file.read()

        self.createArray()


    def checkHeader(self, binaryData):
        if (binaryData[:8] != b'\x89PNG\r\n\x1a\n'):
            raise WrongHeaderException()
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

        for chunk in self.pngData:
            print(chunk['chunkType'])
            print(chunk['chunkData'])

    def createArray(self):
        self.checkHeader(self.binaryData)
        self.parseBinaryData()

