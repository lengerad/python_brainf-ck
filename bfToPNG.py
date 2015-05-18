__author__ = 'radimsky'
import zlib
import math

class createPNG:
    def __init__(self, inFileBF, option, outfile, pngHandler="", inFilePicture=""):
        with open(inFileBF, 'r') as bfFile:
            self.bfCode = bfFile.read()

        self.bfCode = ''.join(self.bfCode.split())
        # print(len(self.bfCode))
        self.option = option
        self.pictureData = []
        # print(outfile)

        # print(self.pictureData)
        with open(outfile, 'wb') as self.file:
            self.file.write(b'\x89PNG\r\n\x1a\n')
            # Pridam si dva slouce pro otaceni
            if (option == "loller"):
                self.height = math.ceil(math.sqrt(len(self.bfCode)))
                self.width = self.height + 2
                self.createArray(self.lolThatCode)
            elif (option == "copter"):
                self.pngData = pngHandler.pictureArray
                self.height = math.ceil(math.sqrt(len(self.bfCode)))
                self.width = self.height + 2
                self.createArray(self.copterThatCode)

            self.file.write(self.createIHDR())
            self.file.write(self.createIDAT())
            self.file.write(self.createIEND())

    def copterThatCode(self, char, i, j):
        # print(pixel)
        pixelValue = (-2 * self.pngData[i][j][0] + 3 * self.pngData[i][j][1] + self.pngData[i][j][2]) % 11
        if (char == '>'):
            tempVal = 0
        elif (char == '<'):
            tempVal = 1
        elif (char == '+'):
            tempVal = 2
        elif (char == '-'):
            tempVal = 3
        elif (char == '.'):
            tempVal = 4
        elif (char == ','):
            tempVal = 5
        elif (char == '['):
            tempVal = 6
        elif (char == ']'):
            tempVal = 7
        elif (char == 'right'):
            tempVal = 8
        elif (char == 'left'):
            tempVal = 9
        elif (char == 'nop'):
            tempVal = 10

        blueColor = (self.pngData[i][j][2] - (11 - (tempVal - pixelValue) % 11))
        if (blueColor < 0):
            blueColor += 11

        return (self.pngData[i][j][0], self.pngData[i][j][1], blueColor)


    def lolThatCode(self, char, i=0, j=0):
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

    def createArray(self, translator):
        self.pictureArray = [[0 for i in range(self.width)] for i in range(self.height)]
        charPointer = 0;
        direction = 1
        i = 0
        j = 0
        while (1):
            if (j == self.width - 1):
                if (i == self.height - 1):
                    self.pictureArray[i][j] = translator("nop", i, j)
                    break
                self.pictureArray[i][j] = translator("right", i, j)
                i += 1;
                self.pictureArray[i][j] = translator("right", i, j)
                direction = -1
                j += direction
                continue
            if (j == 0 and i != 0):
                if (i == self.height - 1):
                    self.pictureArray[i][j] = translator("nop", i, j)
                    break
                self.pictureArray[i][j] = translator("left", i, j)
                i += 1;
                self.pictureArray[i][j] = translator("left", i, j)
                direction = 1
                j += direction
                continue
            if (charPointer >= len(self.bfCode)):
                self.pictureArray[i][j] = translator("nop", i, j)
            else:
                self.pictureArray[i][j] = translator(self.bfCode[charPointer], i, j)
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