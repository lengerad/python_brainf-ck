#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

class BrainFuck:
    def __init__(self, data, memoryPointer, memoryField, test=0):
        self.memory = memoryField
        # print("----------------------------------------")
        self.memory_pointer = int(memoryPointer)
        self.data = data
        self.test = test
        self.output = bytearray()
        self.logFileNumber = 1
        index = self.data.find('!')
        self.input = []
        if index != -1:
            self.input = (self.data[index + 1:])
            self.data = self.data[:index]
        #print(self.memory)


    def interpretBrainfuck(self, data):
        # Method pointer
        # cannot mix self.memory_pointer and current pointer
        pointer = 0

        while pointer < len(data):
            if data[pointer] == '+':
                # Overflow detection
                #print(self.memory[self.memory_pointer])
                if (self.memory[self.memory_pointer] == 256):
                    self.memory[self.memory_pointer] = 0
                self.memory[self.memory_pointer] += 1
            if data[pointer] == '-':
                # Overflow detection
                if (self.memory[self.memory_pointer] == -0):
                    self.memory[self.memory_pointer] = 0
                else:
                    self.memory[self.memory_pointer] -= 1
                    #print(self.memory[self.memory_pointer])

            # Move memory pointer for one position right
            # In case that field is not big enough, allocate new space
            if data[pointer] == '>':
                self.memory_pointer += 1
                if (len(self.memory) == self.memory_pointer):
                    self.memory.append(0)

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
                self.output.append(self.memory[self.memory_pointer])

            if data[pointer] == ',':
                if (len(self.input) != 0):
                    # print("sem")
                    self.memory[self.memory_pointer] = ord(self.input[0])
                    self.input = self.input[1:]
                else:
                    self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

            if data[pointer] == '#':
                self.fileLogging()

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

    def fileLogging(self):
        fileName = "debug_" + "{:0>2d}".format(self.logFileNumber) + ".log"
        with open(fileName, "w") as file:
            sys.stdout = file
            print("# program data" + "\n" + ''.join(self.data.split()) + "\n" + "\n", end='')
            print("# memory" + "\n" + str(bytes(self.memory)) + "\n", end='')
            print("\n" + "# memory pointer" + "\n" + str(self.memory_pointer) + "\n" + "\n", end='')
            print("# output" + "\n" + str(bytes(self.output)) + "\n\n", end='')
        self.logFileNumber += 1
        sys.stdout = sys.__stdout__


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
    import argparse, traceback

    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-l", "--lc2f", nargs="+", dest="pictureToInput",
                      help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-f", "--f2lc", action="store_true", dest="textToPNG",
                      help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-i", "--input", nargs='+', dest="inputFile", help="Source file with brainfuck code")
    parser.add_argument("-o", "--output", dest="outputFile", help="Destination of file to be created")
    parser.add_argument("-t", "--test", action="store_true", dest="testLogging", help="Adding of test output")
    parser.add_argument("-p", "--mpointer", dest="memoryPointer", help="Set memory pointer to specified position")
    parser.add_argument("-m", "--memory", dest="memoryState", help="Set default memory state")
    parser.add_argument("FILE", nargs='?', help="No argument, just input file")

    if ( len(sys.argv) == 1):
        #print("Please input a brainfuck code. Given code will be executed (or at least, I will try)")
        inputStream = sys.stdin.read()
        #print("\nGiven code in brainfuck:")
        brainFuck = BrainFuck(inputStream)

    args = parser.parse_args()

    defaultPointer = 0
    defaultMemory = bytearray(b'\x00')
    test = 0

    if args.memoryPointer:
        defaultPointer = args.memoryPointer.encode('utf-8')

    if args.memoryState:
        # print(args.memoryState)
        defaultMemory = bytearray()
        args.memoryState = args.memoryState.replace('\'', '')
        test = args.memoryState.split('\\x')
        number = ""
        for char in test:
            if (char != 'b'):
                number = int(char, 16)
                defaultMemory.append(number)
                #        print("WHAT")

    if args.testLogging:
        test = 1

    if args.FILE:
        #print(args.FILE)
        #print(defaultMemory)
        #print(defaultPointer)
        if ".b" in args.FILE:
            #print("Brainfuck code given in source file", args.FILE, "will be interpreted.")
            with open(args.FILE, 'r') as file:
                brainFuck = BrainFuck(file.read(), defaultPointer, defaultMemory, test)
                #print(brainFuck.data)
                brainFuck.interpretBrainfuck(brainFuck.data)


        elif ".png" in args.FILE:
            from myPNGlibrary import pngHandler as handler
            handler = handler(args.FILE)

            if (handler.pictureType == "loler"):
                #print("Brainfuck code given in source file", args.FILE,"will be interpreted and is recogized as Brainloller.")
                brainLoler = Brainloller(handler.pictureArray)
                brainFuck = BrainFuck(brainLoler.brainFuckCode, defaultPointer, defaultMemory, test)
                brainFuck.interpretBrainfuck(brainFuck.data)
                #print("\n")

            if (handler.pictureType == "koptera"):
                #print("Brainfuck code given in source file", args.FILE,"will be interpreted and is recogized as Braincopter.")
                brainCopter = Braincopter(handler.pictureArray)
                brainFuck = BrainFuck(brainCopter.brainFuckCode, defaultPointer, defaultMemory, test)
                brainFuck.interpretBrainfuck(brainFuck.data)
                #print("\n")
        elif "\"" in args.FILE:
            args.FILE = args.FILE.replace("\"", "")
            brainFuck = BrainFuck(args.FILE, defaultPointer, defaultMemory, test)
            brainFuck.interpretBrainfuck(brainFuck.data)

        else:
            import myPNGlibrary

            try:
                raise myPNGlibrary.PNGWrongHeaderError
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(4)
        if (args.testLogging):
            brainFuck.fileLogging()

    if args.pictureToInput:

        inputPicture = args.pictureToInput[0]
        outputFile = args.pictureToInput[1]
        # print(inputPicture, outputFile)
        #print("With option: --lc2f starting translation from picture", inputPicture,"to brainfuck code.\nBrainfuck code will be saved to", outputFile, ".")
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

    if args.textToPNG:
        if (len(args.inputFile) == 1):
            from bfToPNG import createPNG as handler

            handler = handler(args.inputFile[0], 'loller', args.outputFile)
        elif (len(args.inputFile) == 2):
            # print(args.inputFile[0])
            #print(args.inputFile[1])
            from myPNGlibrary import pngHandler
            pngHandler = pngHandler(args.inputFile[1])

            from bfToPNG import createPNG
            handler = createPNG(args.inputFile[0], 'copter', args.outputFile, pngHandler, args.inputFile[1])




