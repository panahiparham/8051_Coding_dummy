SETB C
MOV A,#0H

JC HERE

MOV A,#1H
SJMP EXIT

HERE: MOV A,#2H

EXIT: NOP