.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
#
# If the length of the vector is less than 1, 
# this function exits with error code 8.
# ==============================================================================
relu:
    # Prologue
    addi sp, sp, -4
    sw s0, 0(sp)
    ble a1, x0, exit8

    addi t0, x0, 1
    blt a1, t0, exit8
    j loop_start

exit8:
    li a1, 8
    j exit2
    
loop_start:
   addi t1,x0, 0 # i = 0
   addi t2, x0, 0

loop_continue:
    beq t1, a1, loop_end

    #mul t2, t2, t1
    add a0, a0, t2 #go up to next index (+4)
    lw s0, 0(a0)
    addi, t2, x0, 4
    
    ble s0,x0, neg
    addi t1, t1, 1 #increment in
    j loop_continue

neg:
    add, s0,x0,x0
    sw s0, 0(a0) #store 0 into array
    addi t1, t1, 1 #increment
    j loop_continue

loop_end:
    # Epilogue
    lw s0, 0(sp)
    addi sp, sp, 4
    
	ret