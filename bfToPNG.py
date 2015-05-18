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
            # print(self.pictureData)
            with open(outfile, 'wb') as self.file:
                self.file.write(b'\x89PNG\r\n\x1a\n')
                # self.width = len(self.bfCode)
                #self.height = 1
                # Pridam si dva slouce pro otaceni
                self.height = math.ceil(math.sqrt(len(self.bfCode)))
                self.width = self.height + 2
                self.createArray()
                self.file.write(self.createIHDR())
                self.file.write(self.createIDAT())
                self.file.write(self.createIEND())
                # with open(outfile, 'rb') as self.file:
                #   print(self.file.read())
        if option == 'copter':
            self.copterThatCode()


    def lolThatCode(self, char):
        #print(self.bfCode)
        if (char == '>'):
            return (255, 0, 0)
        elif (char == '<'):
            return (128, 0, 0)
        elif (char == '+'):
            return (0, 255, 0)
        elif (char == '-'):
            return (0, 128, 0)
        elif (char == '.'):
            return (0, 0, 255)
        elif (char == ','):
            return (0, 0, 128)
        elif (char == '['):
            return (255, 255, 0)
        elif (char == ']'):
            return (128, 128, 0)
        elif (char == 'left'):
            return (0, 128, 128)
        elif (char == 'right'):
            return (0, 255, 255)
        elif (char == 'nop'):
            return (0, 0, 0)

    def createArray(self):
        self.pictureArray = [[0 for i in range(self.width)] for i in range(self.height)]
        charPointer = 0;
        direction = 1
        i = 0
        j = 0

        while (1):
            if (j == self.width - 1):
                if (i == self.height - 1):
                    self.pictureArray[i][j] = self.lolThatCode("nop")
                    break
                self.pictureArray[i][j] = self.lolThatCode("right")
                i += 1;
                self.pictureArray[i][j] = self.lolThatCode("right")
                direction = -1
                j += direction
                continue
            if (j == 0 and i != 0):
                if (i == self.height - 1):
                    self.pictureArray[i][j] = self.lolThatCode("nop")
                    break
                self.pictureArray[i][j] = self.lolThatCode("left")
                i += 1;
                self.pictureArray[i][j] = self.lolThatCode("left")
                direction = 1
                j += direction
                continue
            if (charPointer >= len(self.bfCode)):
                self.pictureArray[i][j] = self.lolThatCode("nop")
            else:
                self.pictureArray[i][j] = self.lolThatCode(self.bfCode[charPointer])
            j += direction
            charPointer += 1;


            # print(self.height, self.width)
            #print(i,j)

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
        # print(self.pictureArray)
        for row in self.pictureArray:
            chunkData += b'\x00'
            for column in row:
                chunkData.append(column[0])
                chunkData.append(column[1])
                chunkData.append(column[2])
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
                return 1
            if (char == '<'):
                return 2
            if (char == '+'):
                return 3
            if (char == '-'):
                return 4
            if (char == '.'):
                return 5
            if (char == ','):
                return 6
            if (char == '['):
                return 7
            if (char == ']'):
                return 8
