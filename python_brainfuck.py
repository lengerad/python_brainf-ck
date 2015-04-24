__author__ = 'radimsky'

class BrainFuck:
    def __init__(self, data, memoryinit=b'\x00'):
        self.memory = bytearray(memoryinit)
        self.data = data
        self.memory_pointer = 0

    def interpretBrainfuck(self, data, pointer = 0):

        while pointer < len(data):
            if data[pointer] == '+':
                self.memory[self.memory_pointer] += 1

            if data[pointer] == '-':
                self.memory[self.memory_pointer] -= 1

            if data[pointer] == '>':
                self.memory_pointer += 1
                if (len(self.memory) == self.memory_pointer):
                    self.memory.append(0x00)

            if data[pointer] == '<':
                if (self.memory_pointer == 0):
                    pass
                else :
                    self.memory_pointer -= 1

            if data[pointer] == '[' :
                loopData = self.getLoop(pointer, data)

            if data[pointer] == '.' :
                print(chr(self.memory[self.memory_pointer]))

            pointer += 1

    def getLoop(self, pointer, data):
        endOfLoop = pointer + 1;
        while(data[pointer:endOfLoop].count('[') != data[pointer:endOfLoop].count(']')):
            endOfLoop += 1
        self.interpretBrainfuck(data[pointer:endOfLoop])

# Pousteni v ramci testovani
if __name__ == '__main__':
    data = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
    bfCode = BrainFuck(data)
    bfCode.interpretBrainfuck(data)
