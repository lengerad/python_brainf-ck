__author__ = 'radimsky'


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
            print(self.pictureData)

        if option == 'copter':
            self.copterThatCode()

    def createFileWithHeadder(self):
        with open("createdPNG.png", 'wb') as self.file:
            self.file.write(b'\x89PNG\r\n\x1a\n')

    def lolThatCode(self):
        print(self.bfCode)
        for char in self.bfCode:
            char = chr(char)
            if (char == '>'):
                self.pictureData += (255, 0, 0)
            if (char == '<'):
                self.pictureData += (128, 0, 0)
            if (char == '+'):
                self.pictureData += (0, 255, 0)
            if (char == '-'):
                self.pictureData += (0, 128, 0)
            if (char == '.'):
                self.pictureData += (0, 0, 255)
            if (char == ','):
                self.pictureData += (0, 0, 128)
            if (char == '['):
                self.pictureData += (255, 255, 0)
            if (char == ']'):
                self.pictureData += (128, 128, 0)

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
