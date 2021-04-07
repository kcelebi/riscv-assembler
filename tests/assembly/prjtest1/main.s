.import read_matrix.s
.import write_matrix.s
.import matmul.s
.import dot.s
.import relu.s
.import argmax.s
.import utils.s
.import classify.s

.globl main

# This is a dummy main function which imports and calls the classify function.
# While it just exits right after, it could always call classify again.
main:
    jal classify
    jal exit
