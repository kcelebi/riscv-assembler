.globl matmul
.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
#   The order of error codes (checked from top to bottom):
#   If the dimensions of m0 do not make sense, 
#   this function exits with exit code 2.
#   If the dimensions of m1 do not make sense, 
#   this function exits with exit code 3.
#   If the dimensions don't match, 
#   this function exits with exit code 4.
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# =======================================================
matmul:

    # Error checks


    # Prologue
    addi sp, sp, -36
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw s6, 24(sp)      #temp reg for i
    sw s7, 28(sp)       #temp reg for j
    sw ra, 32(sp)

    addi t5, x0, 1 		# for exit regidters
    addi t0, x0, 0      #i =0

    mv s0, a0       #store m0 to s0
    mv s1, a1       #store m0 rows
    mv s2, a2       #store m0 columns
    mv s3, a3       #store m1 to s3
    mv s4, a4       #store m1 rows
    mv s5, a5       #store m1 columns

    #m0 dimensions
    blt s1,t5 exit20
    blt s2, t5, exit20
    #m1 dimensions
    blt s4, t5, exit3
    blt s5, t5, exit3
    #matching dimensions
    bne s2, s4, exit4

    j outer_loop_start

exit20:
    li a1, 2
    j exit2
exit3:
    li a1, 3
    j exit2
exit4:
    li a1, 4
    j exit2

outer_loop_start:
    beq t0, s1, outer_loop_end
    addi t1, x0, 0      #j =0

    j inner_loop_start

inner_loop_start:
    beq t1, s5 inner_loop_end
    mv a0, s0       #point to ith row
    mv a1, s3       #points to jth col

    mv a2, s2          #length of vectors

    addi a3, x0, 0
    addi a3, x0, 1      #stride of m0
    
    addi a4, x0, 0
    add a4, x0, s5      #stride of m1

    addi s6, t0,0
    addi s7, t1,0
    jal ra dot

    
    addi t0, s6, 0
    addi t1, s7, 0
	
    #lw t4, 0(a0)
    sw a0, 0(a6)

    #mv a1, a0
    #jal ra print_int
    #li a1 '\n'
    #jal ra print_char

    addi a6, a6, 4  # go to next in d

    #get ready for next loop
    addi s3, s3, 4      #go to next column

    addi t1, t1, 1      # increment j
    j inner_loop_start
inner_loop_end:

    addi t3,x0, 4
    mul t2, t3, s2      #add 4* number of columns to get next row
    add s0, s0, t2      #go to next row
    
    addi t2, x0,-4
    mul t3, t2, s5
    add s3, s3, t3 	# decrement to go back to first column

    addi t0, t0, 1      #increment i

    j outer_loop_start


outer_loop_end:
    # Epilogue
    addi t4, x0, -4		#t4 = -4
    mul t3, s1,s5		#t3 = rows*cols
    mul t3, t3, t4		#t3 *= -4
    add a6, a6, t3		#decrement pointer by length of mat
    #add a6, a6, t4
    mv a0, a6
    
    
    #jal ra print_int
    #li a1 '\n'
    #jal ra print_char
    
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw s6, 24(sp)
    lw s7, 28(sp)
    lw ra, 32(sp)
    addi sp, sp, 36
    ret