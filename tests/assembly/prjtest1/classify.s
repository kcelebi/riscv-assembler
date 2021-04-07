.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # 
    # If there are an incorrect number of command line args,
    # this function returns with exit code 49.
    #
    # Usage:
    #   main.s -m -1 <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>


    addi sp, sp, -40
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw s6, 24(sp)
    sw s7, 28(sp)
    sw s8, 32(sp)
    sw ra, 36(sp)


    addi t0, x0, 5
    bne a0, t0, exit_args               #wrong # of args
	# =====================================
    # LOAD MATRICES
    # =====================================

    lw s0, 4(a1)                        #give m0 path to s0
    lw s1, 8(a1)                        #give m1 path to s1
    lw s2, 12(a1)                       #give input path to s2
    lw s3, 16(a1)                       #give output path to s3


    # Load pretrained m0
    li a0 20                             #malloc row pointer
    jal ra malloc
    mv s4 a0                            #move pointer to s4

    li a0 20                             #malloc column pointer
    jal ra malloc
    mv s5 a0                            #move pointer to s5

    addi t1, x0, -1                     #row m0
    addi t2, x0, -1                     #col m0
    sw t1 0(s4)                         #put int values to pointer
    sw t2 0(s5) 

    mv a0 s0
    mv a1 s4
    mv a2 s5

    jal ra read_matrix

    mv s6, a0                           #give m0 to s6

   

    # Load pretrained m1

    addi s4, s4, 4
    addi s5, s5 4

    addi t1, x0, -1                     #row m1
    addi t2, x0, -1                     #col m1
    sw t1 0(s4)
    sw t2 0(s5)

    mv a0 s1
    mv a1 s4
    mv a2 s5

    jal ra read_matrix

    mv s7, a0                           #give m1 to s7

    
    # Load input matrix

    addi s4, s4, 4
    addi s5, s5, 4

    addi t1, x0, -1                     #row input
    addi t2, x0, -1                     #col input
    
    sw t1 0(s4)
    sw t2 0(s5)

    mv a0 s2
    mv a1 s4
    mv a2 s5

    jal ra read_matrix

    mv s8, a0                           #give input matrix to s8

    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)



    addi s4,s4, -8
    addi s5, s5 -8 


    #hidden layer
    lw t1 0(s4)
    lw t2 8(s5)

    addi t4, x0, 4
    mul s0 t1 t2        #row m0 * col input

    mul t5, s0, t4
    addi a0 t5 0
    jal ra malloc

    mv a6 a0

    mv a0 s6            #setup matmul
    lw a1 0(s4)
    lw a2 0(s5)
    mv a3 s8
    lw a4 8(s4)
    lw a5 8(s5)

    jal ra matmul


    #mv s8 a6            #store in s8
    mv s8 a0

    #ReLU
    mv a0 s8
    addi a1 s0 0
    jal ra relu

    #mv s8 a0            #store relu output to s8

    #mv a0 s8
    #lw a1 0(s4)
    #lw a2 8(s5)
    #jal ra print_int_array

    lw t1 4(s4)
    lw t2 8(s5)

    mul s0 t1 t2        #row m1 * col m0*input

    addi t4, x0, 4
    mul t5 s0 t4
    addi a0 t5 0
    jal ra malloc

    mv a6 a0

    mv a0 s7            #give m1
    lw a1 4(s4)            #m1 row
    lw a2 4(s5)            #m1 col
    mv a3 s8            #m0*input
    lw a4 0(s4)            #m0 * input row
    lw a5 8(s5)            #m0 *input col

    jal ra matmul

    mv s8 a0

    #mv a0 s8
    #lw a1 4(s4)
    #lw a2 8(s5)
    #jal ra print_int_array

    #lw a1 0(s8)
    #jal ra print_int
    #mv s8 a6            #store in s8


    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Write output matrix

    mv a0 s3                    #give output path
    mv a1 s8                    #give mat to write
    lw a2 4(s4)                    #row num
    lw a3 8(s5)                    #col num

    jal ra write_matrix

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax
    mv a0 s8        #move array to a0
    mv a1 s0        # num of elems


    jal ra argmax

    # Print classification
    mv a1 a0
    jal ra print_int

    # Print newline afterwards for clarity
    li a1 '\n'
    jal ra print_char

    mv a0 s4
    jal ra free
    mv a0 s5
    jal ra free

    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw s6 24(sp)
    lw s7 28(sp)
    lw s8 32(sp)
    lw ra 36(sp)
    addi sp, sp 40
    ret

exit_args:
    li a1 49
    j exit2



