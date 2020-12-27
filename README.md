[![Build Status](https://travis-ci.org/kcelebi/riscv-assembler.svg?branch=main)](https://travis-ci.org/kcelebi/riscv-assembler)
[![Gitter](https://badges.gitter.im/riscv-assembler/community.svg)](https://gitter.im/riscv-assembler/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# riscv-assembler Documentation
RISC-V Assembly code assembler package.

This package contains tools and functions that can convert **RISC-V Assembly code to machine code**. The whole process is implemented using Python purely for understandability, less so for efficiency in computation. These tools can be used to **convert given lines of code or [whole files](#convert) to machine code**. For conversion, output file types are binary, text files, and printing to console. The supported instruction types are **R, I, S, SB, U, and UJ**. Almost all standard instructions are supported, most pseudo instructions are also supported (see [helper functions](#helper-functions) about adding pseudo/missing instructions).

Feel free to open an issue or contact me at [kayacelebi17@gmail.com](mailto:kayacelebi17@gmail.com?subject=[GitHub]%20riscv-assembler) with any questions/inquiries.

# Table of Contents

Use the links below to jump to sections of the documentation:

- [Installation](#installation)
- [Usage](#usage)
    - [Convert](#convert)
    - [Instruction Format Functions](#instruction-format-functions)
    - [Helper Functions](#helper-functions)
- [How it Works](#how-it-works)
- [Future Plans](#future-plans)

# Installation

The package can be installed using pip:

`$ pip install riscv-assembler`

If issues arise try:

`$ python3 -m pip install riscv-assembler`

No other actions necessary.

# Usage

The package works through an `AssemblyConverter` class. We would first need to import this class and all other functions:

`from riscv_assembler.convert import *`

We can now instantiate an object. The constructor is initialized as so:

    AssemblyConverter(output_type = "b", nibble = False, filename = "", hexMode = False)
    
`output_type` refers to whether a converted file should be outputted to a binary file ("b"), a text file ("t"), or to console ("p"). The three of these options can be used in any sort of combination. Here are acceptable usages:
    
    cnv = AssemblyConverter(output_type = "btp") #binary and text and printing
    cnv = AssemblyConverter(output_type = "pbt") #works same as above ^
    cnv = AssemblyConverter(output_type = "b") #just binary
    cnv = AssemblyConverter(output_type = "t") #just text
    cnv = AssemblyConverter(output_type = "p") #just printing
    cnv = AssemblyConverter() #binary by default
    
`nibble` refers to whether (for text file and console outputs) the binary representations should be split in nibbles or kept as an unbroken string. An example output for `nibble = True` would be:

    `1101    0110    0000   0000 ...`
## Convert
With this object we can apply our most powerful function : `convert()`. This function takes in a file name (with .s extension) from the local directory and converts it to the output file of your choice, specified by the object construction. Let's convert the file `simple.s`:

`cnv.convert("simple.s")`

Any empty files, fully commented files, or files without `.s` extension will not be accepted. The function creates a directory by truncating the extension of the file along with two subdirectories called `bin` and `txt` for the respective output files (for `simple.s` the directory would be `simple`). Output files will be stored there for usage and/or printed to console.

## Instruction Format Functions

This package also offers instruction format-specific functions for individual lines of assembly. The instruction types supported are R, I, S, SB, U, and UJ. The machine code is returned as a bitstring that can be printed to console. Check out the examples below for each instruction type:

### R_type()

This functions converts individual lines of assembly with R type instructions to machine code. The function usage is:

`R_type(operation, rs1, rs2, rd)`

Here is an example of translating `add x0 s0 s1`

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter()   
    instr = cnv.R_type("add","x0","s0","s1") #convert the instruction
    
    print(instr) 

Note that the registers are being written as strings. The package maps them correctly to their respective binary values (ex. `s0` maps to `x8`).

### I_type()

This functions converts individual lines of assembly with I type instructions to machine code. The function usage is:

`I_type(operation, rs1, imm, rd)`

Here is an example of translating `addi x0 x0 32`

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    instr = cnv.I_type("addi","x0","32","x0") #convert the instruction
    
    print(instr)

Note that the immediate is a string, not just a number. This was implemented this way for seamless integration with the convert() function, there is an easy workaround for using it on its own. 

### S_type()

This functions converts individual lines of assembly with S type instructions to machine code. The function usage is:

`S_type(operation, rs1, rs2, imm)`

Here is an example of translating `sw x0 0(sp)`

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    instr = cnv.S_type("sw","x0","sp","0") #convert the instruction
    
    print(instr)
    
### SB_type()

This functions converts individual lines of assembly with SB type instructions to machine code. The function usage is:

`SB_type(operation, rs1, rs2, imm)`

Here is an example of translating `beq x0 x1 loop`:

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    instr = cnv.SB_type("beq","x0","x1","loop") #convert the instruction
    
    print(instr)

Note that the jump is written as a string, the appropriate instruction jump is calculated by the package.

### U_type()

This functions converts individual lines of assembly with U type instructions to machine code. The function usage is:

`U_type(operation, imm, rd)`

Here is an example of converting `lui x0 10`:

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    instr = cnv.U_type("lui","x0","10") #convert the instruction
    
    print(instr)
    
### UJ_type()

This functions converts individual lines of assembly with UJ type instructions to machine code. The function usage is:

`UJ_type(operation, imm, rd)`

Here is an example of converting `jal a0 func`:

    from riscv_assembler.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    instr = cnv.UJ_type("jal","func","a0") #convert the instruction
    
    print(instr)
    
## Helper Functions

Here are a few functions that might be useful:

### getOutputType()

This function simply prints the output type that has been initially selected. Example usage:

    cnv = AssemblyConverter("bt") #initially write to binary and text file
    output_type = cnv.getOutputType()
    
    print(output_type)

This will print to console:
    
    bt

### setOutputType()

This function allows the option to change the output type after initialization. Example usage:

    cnv = AssemblyConverter("bt") #initially write to binary and text file
    cnv.setOutputType("p") #now only print to console

### instructionExists()

This function returns a boolean for whether a provided instruction exists in the system. Example usage:

    cnv = AssemblyConverter()
    cnv.instructionExists("add") #yields true
    cnv.instructionExists("hello world") #yields false
    
<!-- ### addPseudo()-->
For functions that do not exist in the system that are used often, feel free to contact me to have it implemented. Most functions are readily available, however, with a growing library it is possible that a pseudo instruction or two slipped past. I intend on implementing functions that allow for the user to bypass any shortfalls like this (see [future plans](#future-plans) )

# How it Works

This package works by parsing through given `.s` files, filtering through comments and empty space to find instructions, categorizing them by their instruction type, then constructing the machine code. These tools have been tested quite thoroughly and work well for individual files. Files grouped in projects have not been implemented yet, but should be [soon](#future-plans).

This package was designed with the intention of helping with CPU architecture engineering (see [future plans](#future-plans) ). Machine code is difficult to interpret which can make it difficult to create efficient tests by hand. Simple software like this can help generate testing material and help debug CPU systems. 

# Future Plans

I created this package purely to provide an extra set of tools for a difficult job and also to display my understanding of Computer Architecture systems in RISC-V. This package was first released when I was a 2nd-year student in college, and I intend to keep improving it overtime in a professional manner. I have many ideas for new implementations which I will update this README.md with. For any questions or inquiries, please feel free to contact me at [kayacelebi17@gmail.com](mailto:kayacelebi17@gmail.com?subject=[GitHub]%20riscv-assembler).

## Project Files

One of the bigger problems I intend to tackle is dealing with multiple files in a project. Currently, this package can only handle files that exist on their own. This implementation will be coming soon. 

## Adding Custom Instructions
A function that I intend to implement is `addPseudo()` which gives users the opportunity to add their own custom functions or fill in functions that might be missing from the package data. 

## Machine Code Decoder
The next logical project to tackle would be to create the reverse system: decoding machine code to create `.s` files. This is much more ambitious and can be achieved down the line. 
