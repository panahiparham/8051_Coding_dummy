import sys
import os


class MicroController:
    def __init__(self):
        pass

    def _reset(self):
        pass

    def execute(self, program):
        pass



class Program:
    def __init__(self, source):
        self.source = source

    def compile(self):
        pass




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
    chip.execute(program)

    # Display MicroController's memory
    print(chip)


if __name__=='__main__':
    main()

    