.globl classify

.text

addi x7, x0, 17
addi x8, x0, 5
	add x9, x8, x7
	sub x9, x9, x8
#hello this is a test
	#hello here's another test

jal ra func

func:
	sw x0 0(sp)
	sw s1 4(sp)

lui 52 s2
beq x0 x5 func
jal a0, func

loop:
	addi x8, x8, 2
	mv x8 s2
	j loop