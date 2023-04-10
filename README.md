[![kcelebi](https://circleci.com/gh/kcelebi/riscv-assembler.svg?style=svg)](https://circleci.com/gh/kcelebi/riscv-assembler)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![example](references/mdimg.png)
# riscv-assembler Documentation
RISC-V Assembly code assembler package. [View the full documentation here](https://www.riscvassembler.org)

This package contains tools and functions that can convert **RISC-V Assembly code to machine code**. The whole process is implemented using Python purely for understandability, less so for efficiency in computation. These tools can be used to **convert given lines of code or [whole files](#convert) to machine code**. For conversion, output file types are binary, text files, and printing to console. The supported instruction types are **R, I, S, SB, U, and UJ**. Almost all standard instructions are supported, most pseudo instructions are also supported.

Feel free to open an issue or contact me at [kayacelebi17@gmail.com](mailto:kayacelebi17@gmail.com?subject=[GitHub]%20riscv-assembler) with any questions/inquiries.

# Installation
The package can be installed using pip:

    $ pip install riscv-assembler

If issues arise try:

    $ python3 -m pip install riscv-assembler

It's possible tha the ``bitstring`` dependency might not install correctly. If this occurs, you can simply pip install it separately:

    $ pip install bitstring
