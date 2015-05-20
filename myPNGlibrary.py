__author__ = 'radimsky'
import zlib
import traceback
import sys


class PNGWrongHeaderError(Exception):
    pass


class PNGNotImplementedError(Exception):
    pass


class PngHandler():
    def __init__(self, path):
        with open(path, 'rb') as file:
            self.binaryData = file.read()

        # print(self.binaryData)
        self.png_data = []
        self.imageWidth = 0
        self.imageHeight = 0
        self.pictureType = 'none'
        self.a = (0, 0, 0)
        self.b = (0, 0, 0)
        self.c = (0, 0, 0)
        self.decompressedData = []
        self.name = path
        self.pictureArray = [[0 for i in range(self.imageWidth)] for i in range(self.imageHeight)]
        self.create_array()
        self.recognize_picture()

    def check_header(self, binary_data):
        if binary_data[:8] != b'\x89PNG\r\n\x1a\n':
            try:
                raise PNGNotImplementedError()
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(8)
        else:
            self.binaryData = binary_data[8:]
            return self

    def recognize_picture(self):
        for i in range(0, self.imageHeight):
            for j in range(0, self.imageWidth):
                for x in range(0, 3):
                    if (self.pictureArray[i][j][x] != 255 and self.pictureArray[i][j][x] != 128 and
                                self.pictureArray[i][j][x] != 0):
                        self.pictureType = "koptera"
                        return
        self.pictureType = "loler"

    def parse_binary_data(self):
        pointer = 0

        while pointer < len(self.binaryData):
            data_length = int.from_bytes(self.binaryData[pointer:pointer + 4], byteorder='big', signed='False')
            # print (data_length)
            pointer += 4
            self.png_data += [{'chunkType': self.binaryData[pointer:pointer + 4],
                               'chunkData': self.binaryData[pointer + 4:pointer + 4 + data_length]}]
            pointer += 8 + data_length

    def decode_ihdr(self):
        control_bytes = 0
        for chunk in self.png_data:
            if chunk['chunkType'] == b'IHDR':
                self.imageWidth = int.from_bytes(chunk['chunkData'][0:4], byteorder='big', signed='False')
                self.imageHeight = int.from_bytes(chunk['chunkData'][4:8], byteorder='big', signed='False')
                control_bytes = int.from_bytes(chunk['chunkData'][9:13], byteorder='big', signed='False')

        if control_bytes != 33554432:
            try:
                raise PNGNotImplementedError()
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(8)

    def get_idat_data(self):
        temp_data = b''
        for chunk in self.png_data:
            if chunk['chunkType'] == b'IDAT':
                temp_data += chunk['chunkData']
        self.decompressedData = zlib.decompress(temp_data)

    def reconstruct_pixel(self, filter_type, pixel):
        if filter_type == 0:
            self.a = pixel
            return pixel
        if filter_type == 1:
            self.a = self.sum_bytes(pixel, self.a)
            return self.a
        if filter_type == 2:
            return self.sum_bytes(pixel, self.b)
        if filter_type == 3:
            self.a = self.sum_bytes(pixel, self.sum_bytes(self.a, self.b) / 2)
            return self.a
        if filter_type == 4:
            self.a = self.sum_bytes(pixel, self.paeth_predictor(self.a, self.b, self.c))
            return self.a

    def sum_bytes(self, pixel, pixel2):
        return (pixel[0] + pixel2[0]) % 256, (pixel[1] + pixel2[1]) % 256, (pixel[2] + pixel2[2]) % 256

    def paeth_predictor(self, pixel_a, pixel_b, pixel_c):
        new_a = self.paeth(pixel_a[0], pixel_b[0], pixel_c[0])
        new_b = self.paeth(pixel_a[1], pixel_b[1], pixel_c[1])
        new_c = self.paeth(pixel_a[2], pixel_b[2], pixel_c[2])
        return new_a, new_b, new_c

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

    def create_array(self):
        self.check_header(self.binaryData)
        self.parse_binary_data()
        self.decode_ihdr()
        self.get_idat_data()
        self.pictureArray = [[0 for i in range(self.imageWidth)] for i in range(self.imageHeight)]
        pointer = 0
        for i in range(0, self.imageHeight):
            self.a = (0, 0, 0)
            self.b = (0, 0, 0)
            self.c = (0, 0, 0)
            filter_type = self.decompressedData[pointer]
            pointer += 1
            for j in range(0, self.imageWidth):
                if i > 0:
                    self.b = self.pictureArray[i - 1][j]
                if i > 0 and j > 0:
                    self.c = self.pictureArray[i - 1][j - 1]
                pixel = (
                    self.decompressedData[pointer], self.decompressedData[pointer + 1],
                    self.decompressedData[pointer + 2])
                self.pictureArray[i][j] = self.reconstruct_pixel(filter_type, pixel)
                pointer += 3
