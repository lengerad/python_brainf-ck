__author__ = 'radimsky'
import zlib
import math


class CreatePNG:
    def __init__(self, in_file_bf, option, outfile, png_handler=""):
        with open(in_file_bf, 'r') as bfFile:
            self.bfCode = bfFile.read()

        self.bfCode = ''.join(self.bfCode.split())
        # print(len(self.bfCode))
        self.option = option
        self.pictureData = []
        self.name = outfile
        # print(outfile)

        # print(self.pictureData)
        with open(outfile, 'wb') as self.file:
            self.file.write(b'\x89PNG\r\n\x1a\n')
            # Pridam si dva slouce pro otaceni
            if option == "loller":
                self.imageHeight = math.ceil(math.sqrt(len(self.bfCode)))
                self.imageWidth = self.imageHeight + 2
                self.create_array(self.lol_that_code)
            elif option == "copter":
                # pngHandler.createArray()
                self.pngData = png_handler.pictureArray
                self.imageHeight = png_handler.imageHeight
                self.imageWidth = png_handler.imageWidth
                # print(self.imageHeight, self.imageWidth)
                self.create_array(self.copter_that_code)

            self.file.write(self.create_ihdr())
            self.file.write(self.create_idat())
            self.file.write(self.create_iend())

    def copter_that_code(self, char, i, j):
        # print(pixel)
        temp_val = 10
        pixel_value = (-2 * self.pngData[i][j][0] + 3 * self.pngData[i][j][1] + self.pngData[i][j][2]) % 11
        if char == '>':
            temp_val = 0
        elif char == '<':
            temp_val = 1
        elif char == '+':
            temp_val = 2
        elif char == '-':
            temp_val = 3
        elif char == '.':
            temp_val = 4
        elif char == ',':
            temp_val = 5
        elif char == '[':
            temp_val = 6
        elif char == ']':
            temp_val = 7
        elif char == 'right':
            temp_val = 8
        elif char == 'left':
            temp_val = 9
        elif char == 'nop':
            temp_val = 10

        blue_color = self.pngData[i][j][2] - (11 - (temp_val - pixel_value) % 11)
        if blue_color < 0:
            blue_color += 11

        return self.pngData[i][j][0], self.pngData[i][j][1], blue_color

    def lol_that_code(self, char):
        # print(self.bfCode)
        if char == '>':
            return 255, 0, 0
        elif char == '<':
            return 128, 0, 0
        elif char == '+':
            return 0, 255, 0
        elif char == '-':
            return 0, 128, 0
        elif char == '.':
            return 0, 0, 255
        elif char == ',':
            return 0, 0, 128
        elif char == '[':
            return 255, 255, 0
        elif char == ']':
            return 128, 128, 0
        elif char == 'left':
            return 0, 128, 128
        elif char == 'right':
            return 0, 255, 255
        elif char == 'nop':
            return 0, 0, 0

    def create_array(self, translator):
        self.pictureArray = [[0 for i in range(self.imageWidth)] for i in range(self.imageHeight)]
        char_pointer = 0
        direction = 1
        i = 0
        j = 0
        while 1:
            if j == self.imageWidth - 1:
                if i == self.imageHeight - 1:
                    self.pictureArray[i][j] = translator("nop", i, j)
                    break
                self.pictureArray[i][j] = translator("right", i, j)
                i += 1
                self.pictureArray[i][j] = translator("right", i, j)
                direction = -1
                j += direction
                continue
            if j == 0 and i != 0:
                if i == self.imageHeight - 1:
                    self.pictureArray[i][j] = translator("nop", i, j)
                    break
                self.pictureArray[i][j] = translator("left", i, j)
                i += 1
                self.pictureArray[i][j] = translator("left", i, j)
                direction = 1
                j += direction
                continue
            if char_pointer >= len(self.bfCode):
                self.pictureArray[i][j] = translator("nop", i, j)
            else:
                self.pictureArray[i][j] = translator(self.bfCode[char_pointer], i, j)
            j += direction
            char_pointer += 1

    def create_ihdr(self):
        chunk_type = b'IHDR'
        chunk_data = bytes(
            self.imageWidth.to_bytes(4, byteorder='big') + self.imageHeight.to_bytes(4, byteorder='big') + bytes(
                [8]) + bytes([2]) + bytes([0]) + bytes([0]) + bytes([0]))
        chunk_length = len(chunk_data)
        chunk_crc = zlib.crc32(bytes(chunk_type + chunk_data))

        return bytes(chunk_length.to_bytes(4, byteorder='big') +
                     chunk_type + chunk_data + chunk_crc.to_bytes(4, byteorder='big'))

    def create_idat(self):
        chunk_type = b'IDAT'
        chunk_data = bytearray()
        # print(self.pictureArray)
        for row in self.pictureArray:
            chunk_data += b'\x00'
            for column in row:
                chunk_data.append(column[0])
                chunk_data.append(column[1])
                chunk_data.append(column[2])
        chunk_data = zlib.compress(chunk_data)
        chunk_length = len(chunk_data)
        chunk_crc = zlib.crc32(bytes(chunk_type + chunk_data))

        return bytes(
            chunk_length.to_bytes(4, byteorder='big') + chunk_type + chunk_data + chunk_crc.to_bytes(4,
                                                                                                     byteorder='big'))

    def create_iend(self):
        # chunk_type = b'IEND'
        # chunk_data = bytes()
        # chunkLength = len(chunk_data)
        #chunkCRC = zlib.crc32(bytes(chunk_type + chunk_data))
        return b'\x00\x00\x00\x00IEND\xaeB`\x82'