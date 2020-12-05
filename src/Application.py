import sys
import os
import re

from bitarray import bitarray


class MicroController:
    def __init__(self):
        self.programStatusWord = {
            'CY': bitarray('0'),
            'AC': bitarray('0'),
            'F0': bitarray('0'),
            'RS1': bitarray('0'),
            'RS0': bitarray('0'),
            'OV': bitarray('0'),
            '-': bitarray('0'),
            'P': bitarray('0'),
        }

        self.A = bitarray('00000000')

        self.registerBanks = [
            {'R0':bitarray('00000000'),
             'R1':bitarray('00000000'),
             'R2':bitarray('00000000'),
             'R3':bitarray('00000000'),
             'R4':bitarray('00000000'),
             'R5':bitarray('00000000'),
             'R6':bitarray('00000000'),
             'R7':bitarray('00000000')
            },
            {'R0':bitarray('00000000'),
             'R1':bitarray('00000000'),
             'R2':bitarray('00000000'),
             'R3':bitarray('00000000'),
             'R4':bitarray('00000000'),
             'R5':bitarray('00000000'),
             'R6':bitarray('00000000'),
             'R7':bitarray('00000000')
            },
            {'R0':bitarray('00000000'),
             'R1':bitarray('00000000'),
             'R2':bitarray('00000000'),
             'R3':bitarray('00000000'),
             'R4':bitarray('00000000'),
             'R5':bitarray('00000000'),
             'R6':bitarray('00000000'),
             'R7':bitarray('00000000')
            },
            {'R0':bitarray('00000000'),
             'R1':bitarray('00000000'),
             'R2':bitarray('00000000'),
             'R3':bitarray('00000000'),
             'R4':bitarray('00000000'),
             'R5':bitarray('00000000'),
             'R6':bitarray('00000000'),
             'R7':bitarray('00000000')
            }
        ]
        pass

    def _reset(self):
        pass

    def execute(self, program):
        pass

    def __repr__(self):

        s = '\n****************************** 8051\'s memory********************************\n'
        s += 'PSW : '
        for key, val in self.programStatusWord.items():
            s += key + ' ' + val.to01() + '  '
        s += '\n'

        s += 'A : '
        s += hex(int(self.A.to01(), 2))[2:]
        s += '\n'

        s += 'RegisterBank 0 : '
        for key, val in self.registerBanks[0].items():
            s += key + ':' + hex(int(val.to01(), 2))[2:] + '\t'
        s += '\n'

        s += 'RegisterBank 1 : '
        for key, val in self.registerBanks[1].items():
            s += key + ':' + hex(int(val.to01(), 2))[2:] + '\t'
        s += '\n'

        s += 'RegisterBank 2 : '
        for key, val in self.registerBanks[2].items():
            s += key + ':' + hex(int(val.to01(), 2))[2:] + '\t'
        s += '\n'

        s += 'RegisterBank 3 : '
        for key, val in self.registerBanks[3].items():
            s += key + ':' + hex(int(val.to01(), 2))[2:] + '\t'
        s += '\n'


        return s



class Program:
    def __init__(self, source):
        self.source = source
        self.isCompiled = False


    def _parseLine(line):

        syntax = {'mov': re.compile(r'(MOV) \s*(A|R0|R1|R2|R3|R4|R5|R6|R7|)\s*,\s*(A|R0|R1|R2|R3|R4|R5|R6|R7|#[0-9a-fA-F]*H)\s*'),
                 }



        if re.fullmatch(r'\s*', line):
            return {}


        for key, val in syntax.items():
            match = re.fullmatch(val, line)
            if match:
                print(match.groups())
                command = match.group(1)
                # print(line)
                return {line}
            else:
                return None





    def compile(self):

        self.executions = []

        for line in self.source.split('\n'):

            parsed = Program._parseLine(line)

            if parsed == None:
                self.isCompiled = False
                return

            if not len(parsed) == 0:
                self.executions.append(parsed)

        self.isCompiled = True
        pass



    def __repr__(self):
        s = '\n****************************** Program ************************************\n'


        s += 'Source Code :'
        s += '\n-----------\n'
        s += self.source
        s += '\n-----------\n'


        s += '\nCompilation :'
        s += '\n-----------\n'
        s += 'Compilation Status: ' + str(self.isCompiled)
        s += '\n-----------\n'

        return s




def main():

    # initial input format checking
    if not len(sys.argv) == 2:
        print('usage: python application.py source.s')
        sys.exit()

    sourcePath = sys.argv[1]

    if not os.path.isfile(sourcePath):
        print('usage: python application.py source.s')
        sys.exit() 

    # Extract Program Source String
    with open(sourcePath, 'r') as src:
        source = src.read()

    # Create the MicroController
    chip = MicroController()

    # Create the Program
    program = Program(source)
    program.compile()
    # print(program)

    # run the Program on the MicroController
    chip.execute(program)

    # Display MicroController's memory
    # print(chip)


    # print(program.executions)
    # print(program.isCompiled)


if __name__=='__main__':
    main()

    