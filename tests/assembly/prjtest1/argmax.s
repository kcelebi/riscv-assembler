.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
#
# If the length of the vector is less than 1, 
# this function exits with error code 7.
# =================================================================
argmax:

   addi sp, sp, -12
   sw s0, 0(sp)
   sw s1, 4(sp) #loaded val
   sw s2, 8(sp) #max index

   addi t0, x0, 1
   blt a1, t0, exit7
    j loop_start

exit7:
    li a1, 7
    j exit2

loop_start:
    addi t0, x0,0 #i =0
    addi t1, x0, 0, #max val
    addi t2, x0, 0 #iteration comp

    j loop_continue
loop_continue:
    beq t0, a1, loop_end

    add a0, a0, t2     #increment index
    lw s1, 0(a0)        #load index
    addi t2, x0, 4      #ready to get next value

    bgt s1, t1, newmax  #see if num is larger than max

    addi t0, t0, 1
    j loop_continue

newmax:
    addi t1, s1, 0      #set new max value
    addi s2, t0, 0     #set max index
   	
    addi t0,t0,1
    j loop_continue
loop_end:
    # Epilogue
    mv a0, s2

    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    addi sp, sp, 12

    ret