########
# Author : Parham Mohammad Panahi
# Date : Fall, Winter 2020
########

import sys
import os
import re

from bitarray import bitarray


##############################################
# MicroController
##############################################
class MicroController:


##############################################
    # internal memory structure
  
    def _reset(self):
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


    def __init__(self):
        self._reset()
    

    def _getRegisterBank(self):
        
        if self.programStatusWord['RS1'] == bitarray('0'):
            if self.programStatusWord['RS0'] == bitarray('0'):
                return 0
            else:
                return 1
        else:
            if self.programStatusWord['RS0'] == bitarray('0'):
                return 2
            else:
                return 3



##############################################
    # generic getter and setter for memory

    def _readRegister(self, name):
        if not (name in self.registerBanks[0].keys()  or name == 'A'):
            raise ValueError('Incorrect Register name {}'.format(name))

        rb = self._getRegisterBank()

        if name == 'A':
            data = self.A
        else:
            data = self.registerBanks[rb][name]

        data = str(hex(int(data.to01(), 2))[2:])

        data = '#' + data

        data = data.upper()

        return data


    def _writeRegister(self, name, value):
        if not (name in self.registerBanks[0].keys()  or name == 'A'):
            raise ValueError('Incorrect Register name {}'.format(name))

        data = value
        if data[0] == '#':
            data = data[1:]

        if data[-1] == 'H' or data[-1] == 'h':
            data = data[:-1]

        data = data.lower()
        data = int(data, 16)
        data = bin(data)
        data = data[2:]
        data = data.zfill(8)
        data = bitarray(data)

        rb = self._getRegisterBank()

        if name == 'A':
            self.A = data
        else:
            self.registerBanks[rb][name] = data



    def _readPSW(self, name):
        if not (name in self.programStatusWord.keys()):
            raise ValueError('Incorrect PSW name {}'.format(name))

        data = self.programStatusWord[name]
        data = data.to01()

        return data


    def _writePSW(self, name, value):
        if not (name in self.programStatusWord.keys()):
            raise ValueError('Incorrect PSW name {}'.format(name))

        if not (value == 1 or value == 0 or value == '1' or value == '0'):
            raise ValueError('Incorrect bit value {} for {}'.format(value, name))

        data = str(value)
        data = bitarray(data)
        self.programStatusWord[name] = data

##############################################
    # commands

    def _nop(self, args):
        print('runnig {}'.format(MicroController._nop.__name__))


    def _mov(self, args):
        print('runnig {} {}'.format(MicroController._mov.__name__, args))

        if not len(args) == 2:
            raise ValueError('incorrect args for _mov')

        dst, src = args

        if src[0] == '#':
            self._writeRegister(dst, src)
        else:
            self._writeRegister(dst, self._readRegister(src))
        


##############################################
    # direct command executions

    def _exec(self, command, args=None, labelTable=None):


        fn = getattr(MicroController, '_'+command)
        jmp = fn(self, args)


        if not jmp:
            return -1
        else:
            if not jmp in labelTable.keys():
                raise ValueError('Incorrect label {}'.format(jmp))
            return labelTable[jmp]


##############################################
    # execution unit level execution

    def execute(self, execUnit):

        # code execution
        # print(execUnit)

        seq = self._exec(execUnit['command'], args=execUnit['args'], labelTable=self.labelTable)

        # sequence 
        if seq < 0:
            return execUnit['sequenceNumber'] + 1
        else:
            return seq

        


##############################################
    # program level execution
    def run(self, program):
        if not program.isCompiled:
            print('Program is not compiled successfully!')
            return

        # temporarily save labelTable
        self.labelTable = program.labelTable


        # main loop for running the program
        sequence = program.executions[0]['sequenceNumber']
        while sequence < len(program.executions):
            # print(program.executions[sequence])
            sequence = self.execute(program.executions[sequence])



        del self.labelTable
        pass



##############################################
    # printing

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
##############################################
# MicroController END
##############################################



##############################################
# MicroController Program
##############################################
class Program:

    # syntax for opcodes
    syntax = {'mov': re.compile(r'(MOV) \s*(A|R0|R1|R2|R3|R4|R5|R6|R7|)\s*,\s*(A|R0|R1|R2|R3|R4|R5|R6|R7|#[0-9a-fA-F]*H)\s*'),
              'nop': re.compile(r'(NOP)\s*'),
            }


    def __init__(self, source):

        self.source = source
        self.isCompiled = False

##############################################
    # single line parsing

    def _parseLine(line):

        executionUnit = {}

        # check for emtpy line
        if re.fullmatch(r'\s*', line):
            return executionUnit

        # check for labels
        labelRegex = re.compile(r'(\w+)\s*:\s*(.*)')
        match = re.fullmatch(labelRegex, line)

        if match:
            command = match.groups()[1]
            executionUnit['label'] = match.groups()[0]

        else:
            command = line
   

        # check for opcodes
        for key, val in Program.syntax.items():
            match = re.fullmatch(val, command)
            if match:
                executionUnit['command'] = key
                executionUnit['args'] = match.groups()[1:]
                return executionUnit
            else:
                continue
        
        print("Error : Compilation Error at line ( {} )".format(line))
        return None



##############################################
    # code compilation

    def compile(self):

        self.executions = []
        self.labelTable = {}

        for line in self.source.split('\n'):

            # parse each line
            parsed = Program._parseLine(line)

            # emtpy line or syntax error
            if parsed == None:
                self.isCompiled = False
                return

            # ok line
            if not len(parsed) == 0:
                # add sequence number
                parsed['sequenceNumber'] = len(self.executions)

                # add labels to labelTable
                if 'label' in parsed.keys():
                    # check for duplicate labels
                    if parsed['label'] in self.labelTable.keys():
                        self.isCompiled = False
                        print("Error : duplicate lablel ( {} )".format(parsed['label']))
                        return

                    self.labelTable[parsed['label']] = parsed['sequenceNumber']

                self.executions.append(parsed)

        self.isCompiled = True
        pass


##############################################
    # printing

    def __repr__(self):
        s = '\n****************************** Program ************************************\n'


        s += 'Source Code :'
        s += '\n-----------\n'
        s += self.source
        s += '\n-----------\n'

        s += 'Compilation Status: ' + str(self.isCompiled)
        s += '\n-----------\n'

        return s
##############################################
# MicroController Program END
##############################################



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
    print(program)

    # run the Program on the MicroController
    chip.run(program)

    # Display MicroController's memory
    print(chip)


    # print(program.executions)
    # print(program.labelTable)
    # print(program.isCompiled)

    # chip._exec('nop')
    # chip._mov(('R0', '#ff'))
    # chip._mov(('R3', 'R0'))
    # chip._mov(('R4', 'R1'))
    # chip._mov(('R4', '#0E2'))
    # chip._mov(('R4', '#02'))
    # chip._mov(('A', '#A2'))
    # chip._mov(('R6', 'A'))

    # print(chip._readRegister('R0'))

    # print(chip)

    # print(chip._readPSW('RS1'))
    # chip._writePSW('RS1', '0')
    # print(chip._readPSW('RS1'))



if __name__=='__main__':
    main()

    