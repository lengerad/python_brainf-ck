__author__ = 'radimsky'
import zlib

class createPNG:
    def __init__(self, path, option):
        with open(path, 'rb') as bfFile:
            self.bfCode = bfFile.read()
        # print(self.bfCode)
        self.option = option
        self.createFileWithHeadder()
        self.pictureData = []

        if option == 'loller':
            self.lolThatCode()
            # print(self.pictureData)
            self.file.write(self.createIHDR())
            self.file.write(self.createIDAT())
            self.file.write(self.createIEND())

        if option == 'copter':
            self.copterThatCode()

    def createFileWithHeadder(self):
        with open("createdPNG.png", 'wb') as self.file:
            self.file.write(b'\x89PNG\r\n\x1a\n')

    def lolThatCode(self):
        #print(self.bfCode)
        for char in self.bfCode:
            char = chr(char)
            if (char == '>'):
                self.pictureData += (0, (255, 0, 0))
            if (char == '<'):
                self.pictureData += (0, (128, 0, 0))
            if (char == '+'):
                self.pictureData += (0, (0, 255, 0))
            if (char == '-'):
                self.pictureData += (0, (0, 128, 0))
            if (char == '.'):
                self.pictureData += (0, (0, 0, 255))
            if (char == ','):
                self.pictureData += (0, (0, 0, 128))
            if (char == '['):
                self.pictureData += (0, (255, 255, 0))
            if (char == ']'):
                self.pictureData += (0, (128, 128, 0))


    def createIHDR(self):
        chunkType = b'IHDR'
        chunkData = bytes()
        chunkLength = len(chunkData)
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))

        return bytes(
            chunkLength.to_bytes(4, byteorder='big') + chunkType + chunkData + chunkCRC.to_bytes(4, byteorder='big'))

    def createIDAT(self):
        chunkType = b'IDAT'
        for item in self.pictureData:
            chunkData = bytes(item)
        chunkData = zlib.compress(self.chunkData)
        chunkLenght = len(self.chunkData)
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))

        return bytes(
            chunkLenght.to_bytes(4, byteorder='big') + chunkType + chunkData + chunkCRC.to_bytes(4, byteorder='big'))

    def createIEND(self):
        chunkType = b'IEND'
        chunkLenght = b'\x00\x00\x00\x00'
        chunkData = bytes()
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))
        
        return bytes(
            chunkLenght.to_bytes(4, byteorder='big') + chunkType + chunkData + chunkCRC.to_bytes(4, byteorder='big'))




    def copterThatCode(self):
        for char in self.bfCode:
            char = chr(char)
            if (char == '>'):
                self.pictureData += 1
            if (char == '<'):
                self.pictureData += 2
            if (char == '+'):
                self.pictureData += 3
            if (char == '-'):
                self.pictureData += 4
            if (char == '.'):
                self.pictureData += 5
            if (char == ','):
                self.pictureData += 6
            if (char == '['):
                self.pictureData += 7
            if (char == ']'):
                self.pictureData += 8
