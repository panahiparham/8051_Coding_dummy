# 8051_Coding_dummy

This small python App will simulate running assembly code on the 8051 micro controller.</br>
Simulating some of the 8051 micro controller to run simple assembly code and see the memory values

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


</br>*this is a work in progress*</br>