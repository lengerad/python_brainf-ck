__author__ = 'radimsky'

import sys


def handleInput(data):
    if ".b" in data:
        bfCoe = BrainFuck(data)
    elif ".png" in data:
        from myPNGlibrary import pngHandler as handler

        pictureData = handler(data).pictureArray
        brainLoller = Brainloller(pictureData)
    else:
        pass

class BrainFuck:
    def __init__(self, data, memoryInit=b'\x00'):
        self.memory = bytearray(memoryInit)
        self.memory_pointer = 0
        try:
            with open(data, 'r') as file:
                self.data = file.read()
                self.interpretBrainfuck(self.data)
        except EnvironmentError:
            self.data = data
            self.interpretBrainfuck(self.data)


    def interpretBrainfuck(self, data):

        # Method pointer
        # cannot mix self.memory_pointer and current pointer
        pointer = 0

        while pointer < len(data):
            if data[pointer] == '+':
                self.memory[self.memory_pointer] += 1

                # Overflow detection
                if (self.memory[self.memory_pointer] == 256):
                    self.memory[self.memory_pointer] = 0

            if data[pointer] == '-':
                # Overflow detection
                if (self.memory[self.memory_pointer] == -0):
                    self.memory[self.memory_pointer] = 0
                else:
                    self.memory[self.memory_pointer] -= 1

            # Move memory pointer for one position right
            # In case that field is not big enough, allocate new space
            if data[pointer] == '>':
                self.memory_pointer += 1
                if (len(self.memory) == self.memory_pointer):
                    self.memory.append(0x00)

            # Move memory pointer for one position left
            # until the pointer is at the beginning of the field
            if data[pointer] == '<':
                if (self.memory_pointer != 0):
                    self.memory_pointer -= 1

            if data[pointer] == '[' :
                loopData = self.getLoop(data[pointer:])
                while (self.memory[self.memory_pointer] != 0):
                    self.interpretBrainfuck(loopData)

                pointer += len(loopData) + 1

            if data[pointer] == '.' :
                print(chr(self.memory[self.memory_pointer]))

            if data[pointer] == ',':
                self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

            pointer += 1

    # Method recieves data from the first opening bracket '['
    # Then it moves with pointer until it finds all closing brackets
    # in case that there is more than one
    # It returns code between these brackets '[...]'

    def getLoop(self,data):
        endOfLoop = 1;
        while(data[0:endOfLoop].count('[') != data[0:endOfLoop].count(']')):
            endOfLoop += 1

        # code inside brackets
        return (data[1:endOfLoop-1])


class Brainloller:
    def __init__(self, pictureData):
        self.pictureData = pictureData
        self.rows = len(self.pictureData)
        self.columns = len(self.pictureData[0])
        self.brainFuckCode = ''
        self.rowChange = 0
        self.columnChange = 1
        # print(self.pictureData)
        self.getThatFuck()


    def getThatFuck(self):
        rowPointer = 0
        columnPointer = 0
        while (rowPointer < self.rows and columnPointer < self.columns and rowPointer >= 0 and columnPointer >= 0):
            self.decodeColor(self.pictureData[rowPointer][columnPointer])
            print(self.brainFuckCode)
            rowPointer += self.rowChange
            columnPointer += self.columnChange

        print(self.brainFuckCode)
        # brainFuck = BrainFuck(self.brainFuckCode)

    def decodeColor(self, pixel):
        if (pixel == (255, 0, 0)):
            self.brainFuckCode += '>'
        if (pixel == (128, 0, 0)):
            self.brainFuckCode += '<'
        if (pixel == (0, 255, 0)):
            self.brainFuckCode += '+'
        if (pixel == (0, 128, 0)):
            self.brainFuckCode += '-'
        if (pixel == (0, 0, 255)):
            self.brainFuckCode += '.'
        if (pixel == (0, 0, 128)):
            self.brainFuckCode += ','
        if (pixel == (255, 255, 0)):
            self.brainFuckCode += '['
        if (pixel == (128, 128, 0)):
            self.brainFuckCode += ']'
        if (pixel == (0, 255, 255)):
            self.turnChangers('right')
        if (pixel == (0, 128, 128)):
            self.turnChangers("left")

    def turnChangers(self, direction):
        if (direction == 'right'):
            if (self.rowChange == 0 and self.columnChange == 1):
                self.rowChange = 1
                self.columnChange = 0
            if (self.rowChange == 1 and self.columnChange == 0):
                self.rowChange = 0
                self.columnChange = -1
            if (self.rowChange == -1 and self.columnChange == 0):
                self.rowChange = 0
                self.columnChange = 1
            if (self.rowChange == 0 and self.columnChange == -1):
                self.rowChange = -1
                self.columnChange = 0
        if (direction == 'left'):
            if (self.rowChange == 0 and self.columnChange == 1):
                self.rowChange = -1
                self.columnChange = 0
            if (self.rowChange == 1 and self.columnChange == 0):
                self.rowChange = 0
                self.columnChange = 1
            if (self.rowChange == -1 and self.columnChange == 0):
                self.rowChange = 0
                self.columnChange = -1
            if (self.rowChange == 0 and self.columnChange == -1):
                self.rowChange = 1
                self.columnChange = 0

# Test run
if __name__ == '__main__':
    if ( len(sys.argv) < 2):
        data = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
        bfCode = BrainFuck(data)
    else:
        handleInput(sys.argv[1])