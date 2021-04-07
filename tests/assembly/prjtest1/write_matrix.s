.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
#   If any file operation fails or doesn't write the proper number of bytes,
#   exit the program with exit code 1.
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
#
# If you receive an fopen error or eof, 
# this function exits with error code 53.
# If you receive an fwrite error or eof,
# this function exits with error code 54.
# If you receive an fclose error or eof,
# this function exits with error code 55.
# ==============================================================================
write_matrix:

    # Prologue
    addi sp, sp, -32
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw s6, 24(sp)
    sw ra, 28(sp)

    addi s5  x0 -1              #EOF
    mv s0 a0                    #filename to s0
    mv s1 a1                    #matrix pointer to s1
    mv s2 a2                    #row number to s2
    mv s3 a3                    #col number to s3

    #Open file

    mv a1 s0                    #filename to a1
    li a2 4                     #permission w+ (4) to a2
    jal ra fopen

    mv s4 a0                    #file descriptor to s4

    beq s4 s5, exit_fopen       #eof
    beq s4 x0, exit_fopen       #fopen error

    #Write file
    #make pointer for buffer

    li a0 4
    jal ra malloc
    mv s6 a0                    #give s6 pointer

    sw s2 0(s6)

    mv a1 s4                    #file descriptor
    mv a2 s6                    #write row
    li a3 1                     #1 item
    li a4 4                     #4 bytes
    jal ra fwrite 

    blt a0 a3, exit_fwrite
    #flush the fd?

    sw s3 0(s6)

    mv a1 s4                    #file descriptor
    mv a2 s6                    #write col 
    li a3 1                     #1 item
    li a4 4                     #4 bytes
    jal ra fwrite 

    blt a0 a3, exit_fwrite

    mv a1 s4                    #file descriptor
    mv a2 s1                    #write matrix
    mul t1 s2 s3                # row * col items
    addi a3, t1, 0
    #li a3 9
    li a4 4                     # 4 bytes per item
    jal ra fwrite

    #addi a1 a0 0
    #jal ra print_int
    #addi a1 a0 0
    #jal ra print_int


    blt a0 a3, exit_fwrite

    #flush?

    #close file
    mv a1 s4
    jal ra fclose               #close the file

    beq a0 s5, exit_fclose

    mv a0 s6
    jal ra free                 #free pointer

    # Epilogue
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw s6 24(sp)
    lw ra 28(sp)
    addi sp, sp, 32

    ret

exit_fopen:
    li a1 53
    j exit2
exit_fwrite:
    li a1 54
    j exit2
exit_fclose:
    li a1 55
    j exit2