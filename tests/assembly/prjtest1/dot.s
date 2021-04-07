.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
#
# If the length of the vector is less than 1, 
# this function exits with error code 5.
# If the stride of either vector is less than 1,
# this function exits with error code 6.
# =======================================================
dot:
    addi sp, sp, -24
    sw s0, 0(sp)        #sum
    sw s1, 4(sp)        #loaded val v0
    sw s2, 8(sp)        #loaded val v1
    sw s3, 12(sp)       #product
    sw s4, 16(sp)       #stride v0
    sw s5, 20(sp)       #stride v1

    addi t5, x0, 1		#exit value
    blt a2, t5, exit5
    blt a3, t5, exit6
    blt a4, t5, exit6
    j loop_start

exit5:
    li a1, 5
    j exit2
exit6:
    li a1, 6
    j exit2

loop_start:
	addi s0, x0, 0		#set sum to 0
    addi t0, x0, 0      #i=0, to keep track of not going over vectorsize
    addi t1, x0, 0      #v0 iter = 0
    addi t2, x0, 0      #v1 iter = 0
    addi t3, x0, 4
    mul s4, a3, t3      #v0 stride
    mul s5, a4, t3       #v1 stride

    j loop_continue

loop_continue:
    beq t0, a2, loop_end  #loop statement

    lw s1, 0(a0)        #load v0
    lw s2, 0(a1)        #load v1

	add a0, a0, s4      #getting v0[i], increment by stride
    add a1, a1, s5      #getting v1[i], increment by stride
    
    mul s3, s1, s2      #get product

    add s0, s0, s3      #add to sum

    addi t0, t0, 1      #increment
    j loop_continue

loop_end:
    # Epilogue
    mv a0, s0           #give a0 return value

    lw s0, 0(sp)        #restore and end
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    addi, sp, sp, 24
    ret