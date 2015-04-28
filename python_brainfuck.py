__author__ = 'radimsky'

import sys


class BrainFuck:
    def __init__(self, data, memoryInit=b'\x00'):
        self.memory = bytearray(memoryInit)
        self.memory_pointer = 0

        if ".b" in data:
            try:
                with open(data, 'r') as file:
                    self.data = file.read()
                    self.interpretBrainfuck(self.data)
            except EnvironmentError:
                pass
        elif ".png" in data:
            self.interpretPNG(data)


        else:
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
                self.memory[self.memory_pointer] -= 1

                # Overflow detection
                if (self.memory[self.memory_pointer] == -1):
                    self.memory[self.memory_pointer] = 0


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

    def interpretPNG(self, filename):
        from myPNGlibrary import PNGhandler as handler

        handler(filename)


# Test run
if __name__ == '__main__':
    if ( len(sys.argv) < 2):
        data = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
        bfCode = BrainFuck(data)
    else:
        bfCode = BrainFuck(sys.argv[1])