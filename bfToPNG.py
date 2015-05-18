__author__ = 'radimsky'
import zlib
import math

class createPNG:
    def __init__(self, inFile, option, outfile):
        with open(inFile, 'r') as bfFile:
            self.bfCode = bfFile.read()

        self.bfCode = ''.join(self.bfCode.split())
        # print(len(self.bfCode))
        self.option = option
        self.pictureData = []

        if option == 'loller':
            self.lolThatCode()
            # print(self.pictureData)
            with open(outfile, 'wb') as self.file:
                self.file.write(b'\x89PNG\r\n\x1a\n')
                # self.width = len(self.bfCode)
                #self.height = 1
                # Pridam si dva slouce pro otaceni
                self.height = math.ceil(math.sqrt(len(self.bfCode)))
                self.width = self.height + 2
                self.file.write(self.createIHDR())
                self.file.write(self.createIDAT())
                self.file.write(self.createIEND())
                # with open(outfile, 'rb') as self.file:
                #   print(self.file.read())
        if option == 'copter':
            self.copterThatCode()


    def lolThatCode(self):
        #print(self.bfCode)
        i = 0
        for char in self.bfCode:
            char = char
            if (char == '>'):
                self.pictureData += (255, 0, 0)
            elif (char == '<'):
                self.pictureData += (128, 0, 0)
            elif (char == '+'):
                self.pictureData += (0, 255, 0)
            elif (char == '-'):
                self.pictureData += (0, 128, 0)
            elif (char == '.'):
                self.pictureData += (0, 0, 255)
            elif (char == ','):
                self.pictureData += (0, 0, 128)
            elif (char == '['):
                self.pictureData += (255, 255, 0)
            elif (char == ']'):
                self.pictureData += (128, 128, 0)
            elif (char == 'left'):
                self.pictureData += (0, 128, 128)
            elif (char == 'right'):
                self.pictureData += (255, 255, 0)
            elif (char == 'nop'):
                self.pictureData += (0, 0, 0)

    def createIHDR(self):
        chunkType = b'IHDR'
        chunkData = bytes(
            self.width.to_bytes(4, byteorder='big') + self.height.to_bytes(4, byteorder='big') + bytes([8]) + bytes(
                [2]) + bytes([0]) + bytes([0]) + bytes([0]))
        chunkLength = len(chunkData)
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))

        return bytes(
            chunkLength.to_bytes(4, byteorder='big') + chunkType + chunkData + chunkCRC.to_bytes(4, byteorder='big'))

    def createIDAT(self):
        chunkType = b'IDAT'
        chunkData = bytearray()
        chunkData += b'\x00'

        for item in self.pictureData:
            # print(item)
            chunkData.append(item)

        chunkData = zlib.compress(chunkData)
        chunkLength = len(chunkData)
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))

        return bytes(
            chunkLength.to_bytes(4, byteorder='big') + chunkType + chunkData + chunkCRC.to_bytes(4, byteorder='big'))

    def createIEND(self):
        chunkType = b'IEND'
        chunkData = bytes()
        chunkLength = len(chunkData)
        chunkCRC = zlib.crc32(bytes(chunkType + chunkData))

        return b'\x00\x00\x00\x00IEND\xaeB`\x82'


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
