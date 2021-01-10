# 8051_Coding_dummy

This small python App will simulate running assembly code on the 8051 micro controller.</br>

This code isn't meant to be correct or complete; just a simple tool to practice beginner level assembly coding with :)
### Requirements and how to use
To use this App all you need is python 3 and the modules listed in `requirements.txt` which is only the bitarray module</br>

then you can head into src folder and run `python Application.py code.s` in which `code.s` is the assembly code you wish to run.</br>

### Examples
for examle you can take a look at some of the code samples already in `/src`. for instance let's take a look at `code5.s` and run it, here is the code in `code5.s`

```
MOV R4,#baH
CJNE R4, #bbH, HERE
MOV R0, #ffH
HERE: MOV R1, #ffH
```

which is just 2 MOV commands and one jump command. first we move #ba hex value into R4 register then we compare the value of R4 with #bb and if they're not equal (which they aren't) the program will jump to the HERE label and move #ff into R1, leaving R0 unchanged.</br>

we can run with command with `python Application.py code5.s` when inside the `/src` folder.

```
(venv) C:\DEV\8051_Coding_dummy\src>python Application.py code5.s

****************************** Program ************************************
Source Code :
-----------
MOV R4,#baH
CJNE R4, #bbH, HERE
MOV R0, #ffH
HERE: MOV R1, #ffH
-----------
Compilation Status: True
-----------

runnig _mov ('R4', '#baH')
runnig _cjne ('R4', '#bbH', 'HERE')
runnig _mov ('R1', '#ffH')

****************************** 8051's memory********************************
PSW : CY 1  AC 0  F0 0  RS1 0  RS0 0  OV 0  - 0  P 0
A : 0
RegisterBank 0 : R0:0   R1:ff   R2:0    R3:0    R4:ba   R5:0    R6:0    R7:0
RegisterBank 1 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
RegisterBank 2 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
RegisterBank 3 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
```


 the output is somewhat long but self explanatory, let's walkthrought the output. first is the source code of the program. then a status flag for compilation is printed. if there is any syntax error the compilation will fail and no code will be ran (the memory values will stay at their default value of 0) the compilation status will also print False.</br>

 given that program compiled successfully next is a squence of all commands executed, this will be useful when creating loops and branches, too see what exactly ran and how many times.</br>

 The final step is a visual of the register banks and PSW of the micro controller after the program has been executed. as you can see R1 = ff,  R0 = 0 which means the jump has happened as desired and that the carry flag CY = 1 in accordance with the specification of the CJNE opcode.</br>

### Compilation process

the steps taken to execute the program is as follows: 
* the source code is read as text and each line is checked for matching syntax.
* if match found, a command will be added to the list of commands to be executed and if no match is found or if there is a problem with the syntax nothing will run and `Compilation Status` will be False along with a print of the line where the first error happened. for example for this code : 

```
MOV R4,#baH
CJNE R4, #bbH, HERE
MOV R0, #ffH
NOT AN OPCODE
HERE: MOV R1, #ffH
```

the output will be :

```
(venv) C:\DEV\8051_Coding_dummy\src>python Application.py code5.s
Error : Compilation Error at line ( NOT AN OPCODE )

****************************** Program ************************************
Source Code :
-----------
MOV R4,#baH
CJNE R4, #bbH, HERE
MOV R0, #ffH
NOT AN OPCODE
HERE: MOV R1, #ffH
-----------
Compilation Status: False
-----------

Program is not compiled successfully!

****************************** 8051's memory********************************
PSW : CY 0  AC 0  F0 0  RS1 0  RS0 0  OV 0  - 0  P 0
A : 0
RegisterBank 0 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
RegisterBank 1 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
RegisterBank 2 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
RegisterBank 3 : R0:0   R1:0    R2:0    R3:0    R4:0    R5:0    R6:0    R7:0
```

* then the squence of commands are ran inside a loop and each command will determine the next command to be executed, this way jumps and labels are handled.

* finally each command is associated with an internal function which does the work of that opcode.

### Errors

there are 2 kinds of errors

* syntax errors are related to parsing of each line and will result in Compilation faliure and nothing will be ran.
* runtime errors are related to incorrect values and labels and will raise exceptions with related error message.

### supported opcodes and small details

first of all 2 kind of addressing is allowed : 
* register names
* immediate values

(meaning that memory location addressing is not supported)</br>

all of the opcode and the H at the end of hex values need to be uppercase.</br>
here is a list of all supported opcodes:
```
MOV A, #f3H
MOV A, R4
MOV R7, #e5H

NOP

INC A
INC R5

DEC A
DEC R0

CLR A
CLR C
CLR AC
CLR F0
CLR RS1
CLR RS0

SETB C
SETB AC
SETB F0
SETB RS1
SETB RS0

SJMP label

JZ label
JNZ lebel

DJNZ R4, label
DJNZ A, label

JC label
JNC label

CJNE A, #34H, label
CJNE R6, #34H, label

ANL A, #f2H
ANL A, R5

ORL A, #f2H
ORL A, R5

XRL A, #f2H
XRL A, R5

RR A

RL A

RRC A

RLC A

SWAP A

XCH A, R0

ADD A, R4

ADD A, #34H

```

this list will be updated as i add more and more opcodes.</br>

### the usecase and the future

i hope this will be a useful tool for anyone learning to program the 8051 micro controller and is still a beginner looking for a tool to practice programming.</br>

this project is imagined for the final project of my "introduction to microprocessor" class and i hope it  will be a useful tool for my teacher and classmates.</br>

i will be adding more and more featues as time allows




</br>*this is a work in progress*</br>

```
TOOD:
    * _add  DONE
    * _addc
    * _subb
    * B register
    * _mul
    * _div
    * stack
    ...
```
