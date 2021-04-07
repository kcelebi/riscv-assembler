.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#   If any file operation fails or doesn't read the proper number of bytes,
#   exit the program with exit code 1.
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
#
# If you receive an fopen error or eof, 
# this function exits with error code 50.
# If you receive an fread error or eof,
# this function exits with error code 51.
# If you receive an fclose error or eof,
# this function exits with error code 52.
# ==============================================================================
read_matrix:

    # Prologue
	addi sp, sp, -24
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)      
    sw ra, 20(sp)       


    addi s4, x0, -1     #EOF
    mv s0 a0            #filepath to s0
    mv s1 a1            #row pointer to s1
    mv s2 a2            #col pointer to s2

    mv a1 s0            #give a1 filepath
    addi a2 x0 0             #give a2 read permission
    jal ra fopen        #open file


    beq a0 s4, exit_fopen       #if fopen fails by eof
    beq a0  x0, exit_fopen       #fopen error

    mv s3 a0            #give file descriptor to s3

    #read first two integers to s1, s2

    #make buffer

    mv a1 s3            #give a1 file descriptor
    mv a2 s1         #give pointer to # of rows to a2
    li a3 4             #read 4 bytes
    jal ra fread

    mv s1 a2

    #lw a1 0(s1)
    #jal ra print_int
    #li a1 '\n'
    #jal ra print_char

    beq a0 s4, exit_fread       #eof
    beq a0 x0, exit_fread       #fread error

    mv a1 s3            #give a1 file descriptor
    mv a2 s2            #give pointer to # of cols to a2
    li a3 4             #read 4 bytes
    jal ra fread

    beq a0 s4, exit_fread       #eof
    beq a0 x0, exit_fread       #fread error

    #mv s2 a2       #do some printing
    #lw a1 0(s2)
    #jal ra print_int
    #li a1 '\n'
    #jal ra print_char

    #make the matrix pointer

    lw t1 0(s1)
    lw t2 0(s2)
    mul t3, t1 t2       #number of entries
    addi t4, x0, 4      #t4 = 4
    mul t3, t3, t4      #4 bytes * number of entries

    mv a0 t3
    jal ra malloc       #malloc new pointer to a0

    mv a1 s3            # give a1 file descriptor
    mv a2 a0            # give a2 the pointer to mat
    mv a3 t3            # number of bytes
    jal ra fread

    
    mv a1 s3            #give a1 the file descriptor
    jal ra fclose       #close file

    beq a0, s4, exit_fclose     #eof
    bne a0, x0, exit_fclose      #fclose error

    mv a0 a2            # give a0 the pointer to matrix
    # Epilogue

    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw ra, 20(sp)
    addi sp, sp, 24

    ret

exit_fopen:
    li a1 50
    j exit2       
exit_fread:
    li a1 51
    j exit2
exit_fclose:
    li a1 52
    j exit2