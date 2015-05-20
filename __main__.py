#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


class BrainFuck:
    def __init__(self, data, memory_pointer, memory_field, test_flag=0):
        self.memory = memory_field
        self.memory_pointer = int(memory_pointer)
        self.data = data
        self.test_flag = test_flag
        self.output = bytearray()
        self.log_file_number = 1
        self.input_index = self.data.find('!')
        self.input = []
        if self.input_index != -1:
            self.input = (self.data[self.input_index + 1:])
            self.data = self.data[:self.input_index]

    def interpret_brainfuck(self, data):
        # Method pointer
        # cannot mix self.memory_pointer and current pointer
        pointer = 0
        while pointer < len(data):
            if data[pointer] == '+':
                # Overflow detection
                #print(self.memory[self.memory_pointer])
                if self.memory[self.memory_pointer] == 256:
                    self.memory[self.memory_pointer] = 0
                self.memory[self.memory_pointer] += 1
            if data[pointer] == '-':
                # Overflow detection
                if self.memory[self.memory_pointer] == -0:
                    self.memory[self.memory_pointer] = 0
                else:
                    self.memory[self.memory_pointer] -= 1
                    #print(self.memory[self.memory_pointer])

            # Move memory pointer for one position right
            # In case that field is not big enough, allocate new space
            if data[pointer] == '>':
                self.memory_pointer += 1
                if len(self.memory) == self.memory_pointer:
                    self.memory.append(0)

            # Move memory pointer for one position left
            # until the pointer is at the beginning of the field
            if data[pointer] == '<':
                if self.memory_pointer != 0:
                    self.memory_pointer -= 1

            if data[pointer] == '[':
                loop_data = self.get_loop(data[pointer:])
                while self.memory[self.memory_pointer] != 0:
                    self.interpret_brainfuck(loop_data)

                pointer += len(loop_data) + 1

            if data[pointer] == '.':
                sys.stdout.write(chr(self.memory[self.memory_pointer]))
                sys.stdout.flush()
                self.output.append(self.memory[self.memory_pointer])

            if data[pointer] == ',':
                if len(self.input) != 0:
                    #print("sem")
                    self.memory[self.memory_pointer] = ord(self.input[0])
                    self.input = self.input[1:]
                else:
                    self.memory[self.memory_pointer] = ord(sys.stdin.read(1))

            if data[pointer] == '#':
                self.file_logging()

            pointer += 1

    # Method recieves data from the first opening bracket '['
    # Then it moves with pointer until it finds all closing brackets
    # in case that there is more than one
    # It returns code between these brackets '[...]'

    def get_loop(self, data):
        end_of_loop = 1
        while data[0:end_of_loop].count('[') != data[0:end_of_loop].count(']'):
            end_of_loop += 1

        # code inside brackets
        return data[1:end_of_loop - 1]

    def file_logging(self, png=0, data=[]):
        file_name = "debug_" + "{:0>2d}".format(self.log_file_number) + ".log"
        with open(file_name, "w") as log_file:
            sys.stdout = log_file
            print("# program data" + "\n" + ''.join(self.data.split()) + "\n" + "\n", end='')
            print("# memory" + "\n" + str(bytes(self.memory)) + "\n", end='')
            print("\n" + "# memory pointer" + "\n" + str(self.memory_pointer) + "\n" + "\n", end='')
            print("# output" + "\n" + str(bytes(self.output)) + "\n\n", end='')
            if png:
                print("# RGB input" + "\n" + "[" + "\n", end='')
                for i in data:
                    print("    " + str(i) + ",\n", end='')
                print("]" + "\n\n", end='')
        self.log_file_number += 1
        sys.stdout = sys.__stdout__


class Braincopter:
    def __init__(self, picture_data):
        self.pictureData = picture_data
        self.rows = len(self.pictureData)
        self.columns = len(self.pictureData[0])
        self.brainFuckCode = ''
        self.movingTwice = list()
        self.movingTwice.append(0)
        self.movingTwice.append(1)
        self.get_that_fuck()
        # print("I am gonna copter your ass.")

    def get_that_fuck(self):
        row_pointer = 0
        column_pointer = 0
        #print(self.rows,self.columns)
        while row_pointer < self.rows and column_pointer < self.columns and row_pointer >= 0 and column_pointer >= 0:
            self.decode_color(self.pictureData[row_pointer][column_pointer])
            row_pointer += self.movingTwice[0]
            column_pointer += self.movingTwice[1]
            #print(rowPointer,columnPointer)

        # print(self.brainFuckCode)

    def decode_color(self, pixel):
        mod = (-2 * pixel[0] + 3 * pixel[1] + pixel[2]) % 11

        if mod == 0:
            self.brainFuckCode += '>'
        if mod == 1:
            self.brainFuckCode += '<'
        if mod == 2:
            self.brainFuckCode += '+'
        if mod == 3:
            self.brainFuckCode += '-'
        if mod == 4:
            self.brainFuckCode += '.'
        if mod == 5:
            self.brainFuckCode += ','
        if mod == 6:
            self.brainFuckCode += '['
        if mod == 7:
            self.brainFuckCode += ']'
        if mod == 8:
            self.turn_changers('right')
        if mod == 9:
            self.turn_changers("left")

    def turn_changers(self, direction):
        if direction == 'right':
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = -self.movingTwice[0]
                self.movingTwice[0] = 0
                return
        if direction == 'left':
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = -self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = self.movingTwice[0]
                self.movingTwice[0] = 0
                return


class Brainloller:
    def __init__(self, picture_data):
        self.pictureData = picture_data
        self.rows = len(self.pictureData)
        self.columns = len(self.pictureData[0])
        self.brainFuckCode = ''
        self.movingTwice = list()
        self.movingTwice.append(0)
        self.movingTwice.append(1)
        # print(self.pictureData)
        self.get_that_fuck()

    def get_that_fuck(self):
        row_pointer = 0
        column_pointer = 0
        while row_pointer < self.rows and column_pointer < self.columns and row_pointer >= 0 and column_pointer >= 0:
            self.decode_color(self.pictureData[row_pointer][column_pointer])
            # print(self.brainFuckCode)
            row_pointer += self.movingTwice[0]
            column_pointer += self.movingTwice[1]
            #print(rowPointer,columnPointer)

    def decode_color(self, pixel):
        if pixel == (255, 0, 0):
            self.brainFuckCode += '>'
        if pixel == (128, 0, 0):
            self.brainFuckCode += '<'
        if pixel == (0, 255, 0):
            self.brainFuckCode += '+'
        if pixel == (0, 128, 0):
            self.brainFuckCode += '-'
        if pixel == (0, 0, 255):
            self.brainFuckCode += '.'
        if pixel == (0, 0, 128):
            self.brainFuckCode += ','
        if pixel == (255, 255, 0):
            self.brainFuckCode += '['
        if pixel == (128, 128, 0):
            self.brainFuckCode += ']'
        if pixel == (0, 255, 255):
            self.turn_changers('right')
        if pixel == (0, 128, 128):
            self.turn_changers("left")

    def turn_changers(self, direction):
        if direction == 'right':
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = -self.movingTwice[0]
                self.movingTwice[0] = 0
                return
        if direction == 'left':
            if self.movingTwice[0] == 0:
                self.movingTwice[0] = -self.movingTwice[1]
                self.movingTwice[1] = 0
                return
            else:
                self.movingTwice[1] = self.movingTwice[0]
                self.movingTwice[0] = 0
                return


def create_pnm(picture_input):
    # pictureData = picture_input
    #print(picture_input.pictureArray)
    pictureData = bytearray()
    for row in picture_input.pictureArray:
        for column in row:
            for pixelPart in column:
                #print(pixelPart)
                pictureData.append(pixelPart)

    print(picture_input.name)
    with open(picture_input.name.split('.')[0] + ".ppm", "w") as ppmFile:
        ppmFile.write("P6\n\n" + str(picture_input.imageWidth) + "  " + str(picture_input.imageHeight) +
                      "\n\n255\n")
    with open(picture_input.name.split('.')[0] + ".ppm", "ab") as ppmFile:
        ppmFile.write(bytes(pictureData))

        # with open(picture_input.name.split('.')[0] + ".ppm", "rb") as ppmFile:
        # print(ppmFile.read())

# Test run
if __name__ == '__main__':
    import argparse
    import traceback

    parser = argparse.ArgumentParser(description="Arguments")

    parser.add_argument("-l", "--lc2f", nargs="+", dest="pictureToInput",
                        help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-f", "--f2lc", action="store_true", dest="textToPNG",
                        help="Translation from given picture (BC and BL) to output or file")
    parser.add_argument("-i", "--input", nargs='+', dest="inputFile", help="Source file with brainfuck code")
    parser.add_argument("-o", "--output", dest="outputFile", help="Destination of file to be created")
    parser.add_argument("-t", "--test", action="store_true", dest="testLogging", help=" Adding of test output")
    parser.add_argument("-p", "--mpointer", dest="memoryPointer", help="Set memory pointer to specified position")
    parser.add_argument("-m", "--memory", dest="memoryState", help="Set default memory state")
    parser.add_argument("--ppm", "--pbm", action="store_true", dest="doPPM", help="Set default memory state")
    parser.add_argument("FILE", nargs='?', help="No argument, just input file")

    defaultPointer = 0
    defaultMemory = bytearray(b'\x00')
    testFlag = 0
    takingPicturesOfYou = 0

    if len(sys.argv) == 1:
        inputStream = sys.stdin.read()
        brainFuck = BrainFuck(inputStream, defaultPointer, defaultMemory)

    args = parser.parse_args()

    if args.memoryPointer:
        defaultPointer = args.memoryPointer.encode('utf-8')

    if args.memoryState:
        #print(args.memoryState)
        defaultMemory = bytearray()
        args.memoryState = args.memoryState.replace('\'', '')
        test = args.memoryState.split('\\x')
        number = ""
        for char in test:
            if char != 'b':
                number = int(char, 16)
                defaultMemory.append(number)
                # print("WHAT")

    if args.testLogging:
        testFlag = 1

    if args.FILE:
        if ".b" in args.FILE:
            #print("Brainfuck code given in source file", args.FILE, "will be interpreted.")
            with open(args.FILE, 'r') as file:
                brainFuck = BrainFuck(file.read(), defaultPointer, defaultMemory, testFlag)
                #print(brainFuck.data)
                brainFuck.interpret_brainfuck(brainFuck.data)

        elif ".png" in args.FILE:
            from myPNGlibrary import pngHandler as pngHandler

            picture_handler = pngHandler(args.FILE)

            if picture_handler.pictureType == "loler":
                brainLoler = Brainloller(picture_handler.pictureArray)
                brainFuck = BrainFuck(brainLoler.brainFuckCode, defaultPointer, defaultMemory, testFlag)
                brainFuck.interpret_brainfuck(brainFuck.data)
                takingPicturesOfYou = 1
                #print("\n")

            if picture_handler.pictureType == "koptera":
                brainCopter = Braincopter(picture_handler.pictureArray)
                brainFuck = BrainFuck(brainCopter.brainFuckCode, defaultPointer, defaultMemory, testFlag)
                brainFuck.interpret_brainfuck(brainFuck.data)
                takingPicturesOfYou = 1
                #print("\n")
        elif "\"" in args.FILE:
            args.FILE = args.FILE.replace("\"", "")
            brainFuck = BrainFuck(args.FILE, defaultPointer, defaultMemory, testFlag)
            brainFuck.interpret_brainfuck(brainFuck.data)

        else:
            import myPNGlibrary
            try:
                raise myPNGlibrary.PNGWrongHeaderError
            except:
                traceback.print_exc(file=sys.stderr)
                sys.exit(4)
        if args.testLogging:
            if takingPicturesOfYou:
                brainFuck.file_logging(takingPicturesOfYou, picture_handler.pictureArray)
            else:
                brainFuck.file_logging(int(takingPicturesOfYou))

    if args.pictureToInput:
        # lc2f
        inputPicture = args.pictureToInput[0]
        if len(args.pictureToInput) > 1:
            outputFile = args.pictureToInput[1]

            from myPNGlibrary import pngHandler as pngHandler

            picture_handler = pngHandler(inputPicture)

            if picture_handler.pictureType == "loler":
                brainLoler = Brainloller(picture_handler.pictureArray)
                with open(outputFile, 'w') as file:
                    file.write(brainLoler.brainFuckCode)

            if picture_handler.pictureType == "koptera":
                brainCopter = Braincopter(picture_handler.pictureArray)
                with open(outputFile, 'w') as file:
                    file.write(brainCopter.brainFuckCode)

        else:
            from myPNGlibrary import pngHandler as pngHandler

            picture_handler = pngHandler(inputPicture)

            if picture_handler.pictureType == "loler":
                brainLoler = Brainloller(picture_handler.pictureArray)
                print(brainLoler.brainFuckCode)

            if picture_handler.pictureType == "koptera":
                brainCopter = Braincopter(picture_handler.pictureArray)
                print(brainCopter.brainFuckCode)

        if args.doPPM:
            create_pnm(picture_handler)

    if args.textToPNG:
        # f2lc
        if len(args.inputFile) == 1:
            from bfToPNG import createPNG as createPNG
            handler = createPNG(args.inputFile[0], 'loller', args.outputFile)
            if args.doPPM:
                create_pnm(handler)
        elif len(args.inputFile) == 2:
            # print(args.inputFile[0])
            #print(args.inputFile[1])
            from myPNGlibrary import pngHandler

            png_handler = pngHandler(args.inputFile[1])
            from bfToPNG import createPNG

            handler = createPNG(args.inputFile[0], 'copter', args.outputFile, png_handler, args.inputFile[1])
            if args.doPPM:
                create_pnm(handler)
                create_pnm(png_handler)