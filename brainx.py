__author__ = 'radimsky'

import sys
import re

class BrainFuck:
    def __init__(self, data, memoryInit=b'\x00'):
        self.memory = bytearray(memoryInit)
        self.memory_pointer = 0
        # print(data)
        try:
            with open(data, 'r') as file:
                if ".b" in data:
                    self.data = file.read()
                    self.interpretBrainfuck(self.data)
                elif ".png" in data:
                    from myPNGlibrary import pngHandler as handler

                    pictureData = handler(data).pictureArray
                    # print(pictureData)
                    #brainLoller = Braincopter(pictureData)
                    brainLoller = Brainloller(pictureData)
                else:
                    print("Nic nedelam.")
                    pass
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
                sys.stdout.write(chr(self.memory[self.memory_pointer]))
                sys.stdout.flush()

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


class Braincopter:
    def __init__(self, pictureData):
        self.pictureData = pictureData
        self.rows = len(self.pictureData)
        self.columns = len(self.pictureData[0])
        self.brainFuckCode = ''
        self.movingTwice = list()
        self.movingTwice.append(0)
        self.movingTwice.append(1)
        self.getThatFuck()
        # print("I am gonna copter your ass.")


    def getThatFuck(self):
        rowPointer = 0
        columnPointer = 0
        #print(self.rows,self.columns)
        while (rowPointer < self.rows and columnPointer < self.columns and rowPointer >= 0 and columnPointer >= 0):
            self.decodeColor(self.pictureData[rowPointer][columnPointer])
            #print(self.brainFuckCode)
            rowPointer += self.movingTwice[0]
            columnPointer += self.movingTwice[1]
            #print(rowPointer,columnPointer)

        # print(self.brainFuckCode)
            # with open("lk.b", 'w') as file:
            #    file.write(self.brainFuckCode)
            #brainFuck = BrainFuck(self.brainFuckCode)

    def decodeColor(self, pixel):

        mod = (-2 * pixel[0] + 3 * pixel[1] + pixel[2]) % 11

        if (mod == 0):
            self.brainFuckCode += '>'
        if (mod == 1):
            self.brainFuckCode += '<'
        if (mod == 2):
            self.brainFuckCode += '+'
        if (mod == 3):
            self.brainFuckCode += '-'
        if (mod == 4):
            self.brainFuckCode += '.'
        if (mod == 5):
            self.brainFuckCode += ','
        if (mod == 6):
            self.brainFuckCode += '['
        if (mod == 7):
            self.brainFuckCode += ']'
        if (mod == 8):
            self.turnChangers('right')
        if (mod == 9):
            self.turnChangers("left")

    def turnChangers(self, direction):
        if (direction == 'right'):
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = -self.movingTwice[0]
                self.movingTwice[0] = 0
                return
        if (direction == 'left'):
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = -self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = self.movingTwice[0]
                self.movingTwice[0] = 0
                return

class Brainloller:
    def __init__(self, pictureData):
        self.pictureData = pictureData
        self.rows = len(self.pictureData)
        self.columns = len(self.pictureData[0])
        self.brainFuckCode = ''
        self.movingTwice = list()
        self.movingTwice.append(0)
        self.movingTwice.append(1)
        # print(self.pictureData)
        self.getThatFuck()


    def getThatFuck(self):
        rowPointer = 0
        columnPointer = 0
        while (rowPointer < self.rows and columnPointer < self.columns and rowPointer >= 0 and columnPointer >= 0):
            self.decodeColor(self.pictureData[rowPointer][columnPointer])
            # print(self.brainFuckCode)
            rowPointer += self.movingTwice[0]
            columnPointer += self.movingTwice[1]
            #print(rowPointer,columnPointer)

        # print(self.brainFuckCode)
        brainFuck = BrainFuck(self.brainFuckCode)

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
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = -self.movingTwice[0]
                self.movingTwice[0] = 0
                return
        if (direction == 'left'):
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = -self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = self.movingTwice[0]
                self.movingTwice[0] = 0
                return



# Test run
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-l", "--lc2f", nargs="+", dest="pictureToInput",
                      help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-f", "--f2lc", action="store_true", dest="textToPNG",
                      help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-i", "--input", nargs='+', dest="inputFile", help="Source file with brainfuck code")
    parser.add_argument("-o", "--output", dest="outputFile", help="Destination of file to be created")
    parser.add_argument("-t", "--test", dest="testLogging", help="Adding of test output")

    if ( len(sys.argv) == 1):
        print("Please input a brainfuck code. Given code will be executed (or at least, I will try)")
        inputStream = sys.stdin.read()
        print("\nGiven code in brainfuck:")
        brainFuck = BrainFuck(inputStream)
    if ( len(sys.argv) == 2):
        print(sys.argv[1])
        if ".b" in sys.argv[1]:
            print("Kedlubna")
        elif ".png" in sys.argv[1]:
            print("Brambora")
        else:
            print("What you just gave me? I don't know what to do with it!")
            exit(1)

    args = parser.parse_args()

    if args.pictureToInput:

        inputPicture = args.pictureToInput[0]
        outputFile = args.pictureToInput[1]
        # print(inputPicture, outputFile)
        print("With option: --lc2f starting translation from picture", inputPicture,
              "to brainfuck code.\nBrainfuck code will be saved to", outputFile, ".")
        from myPNGlibrary import pngHandler as handler

        handler = handler(inputPicture)
        if (handler.pictureType == "loler"):
            brainLoler = Brainloller(handler.pictureArray)
            with open(outputFile, 'w') as file:
                file.write(brainLoler.brainFuckCode)
        if (handler.pictureType == "koptera"):
            brainCopter = Braincopter(handler.pictureArray)
            with open(outputFile, 'w') as file:
                file.write(brainCopter.brainFuckCode)
        exit(0)

    if args.textToPNG:
        print(args.inputFile)
        print(args.outputFile)
