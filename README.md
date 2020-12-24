# riscv-assembler
RISC-V Assembly code assembler package.

This package contains tools and functions that can convert RISC-V Assembly code to machine code. The whole process is implemented using Python purely for understandability, less so for efficiency in computation. These tools can be used to convert given lines of code or whole files. For conversion, output file types are binary and text files.

# Table of Contents

Use the links below to jump to sections of the documentation:

- [Installation](#installation)
- [Usage](#usage)
    - [Convert](#convert)
    - [Instruction Format Functions](##instruction-format-functions)
        - [R Format](#r_type)
        - [I Format](#i_type)
        - [S Format](#s_type)
        - [SB Format](#sb_type)
        - [U Format](#u_type)
        - [UJ Format](#uj_type)
    - [Helper Functions](#helper-functions)
- 
# Installation

The package can be installed using pip:

`$ pip install riscv_assembler`

No other actions necessary.

# Usage

The package works through an `AssemblyConverter` class. We would first need to import this class:

`from riscv_interpreter.convert import AssemblyConverter`

We can now instantiate an object. The constructor requires a string that specifies the output file as any combination of binary, text, or printing to console. Here are acceptable usages:
    
    cnv = AssemblyConverter("btp") #binary and text and printing
    cnv = AssemblyConverter("pbt") #works same as above ^
    cnv = AssemblyConverter("b") #just binary
    cnv = AssemblyConverter("t") #just text
    cnv = AssemblyConverter("p") #just printing
    cnv = AssemblyConverter() #binary by default
    

## Convert
With this object we can apply our most powerful function : `convert()`. This function takes in a file name (with .s extension) from the local directory and converts it to the output file of your choice, specified by the object construction. Let's convert the file `simple.s`:

`cnv.convert("simple.s")`

Any empty files, fully commented files, or files without `.s` extension will not be accepted. The function creates a directory by truncating the extension of the file along with two subdirectories called `bin` and `txt` for the respective output files (for `simple.s` the directory would be `simple`). Output files will be stored there for usage and/or printed to console.

## Instruction Format Functions

This package also offers instruction format-specific functions for individual lines of assembly. The instruction types supported are R, I, S, SB, U, and UJ. The outputs to these are written to text or binary files or printed to console, depending on how the constructor was initialized. For the below examples, they are being outputted to binary files.

### R_type

This functions converts individual lines of assembly with R type instructions to machine code. The function usage is:

`R_type(operation, rs1, rs2, rd)`

Here is an example of translating `add x0 s0 s1`

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.R_type("add","x0","s0","s1") #convert the instruction

Note that the registers are being written as strings. The package maps them correctly to their respective binary values (ex. `s0` maps to `x8`).

### I_type

This functions converts individual lines of assembly with I type instructions to machine code. The function usage is:

`I_type(operation, rs1, imm, rd)`

Here is an example of translating `addi x0 x0 32`

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.I_type("addi","x0","32","x0") #convert the instruction

Note that the immediate is a string, not just a number. This was implemented this way for seamless integration with the convert() function, there is an easy workaround for using it on its own. 

### S_type

This functions converts individual lines of assembly with S type instructions to machine code. The function usage is:

`S_type(operation, rs1, rs2, imm)`

Here is an example of translating `sw x0 0(sp)`

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.S_type("sw","x0","sp","0") #convert the instruction
    
### SB_type

This functions converts individual lines of assembly with SB type instructions to machine code. The function usage is:

`SB_type(operation, rs1, rs2, imm)`

Here is an example of translating `beq x0 x1 loop`:

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.SB_type("beq","x0","x1","loop") #convert the instruction

Note that the jump is written as a string, the appropriate instruction jump is calculated by the package.

### U_type

This functions converts individual lines of assembly with U type instructions to machine code. The function usage is:

`U_type(operation, imm, rd)`

Here is an example of converting `lui x0 10`:

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.U_type("lui","x0","10") #convert the instruction
    
### UJ_type

This functions converts individual lines of assembly with UJ type instructions to machine code. The function usage is:

`UJ_type(operation, imm, rd)`

Here is an example of converting `jal a0 func`:

    from riscv_interpreter.convert import AssemblyConverter
    
    cnv = AssemblyConverter() #output to binary   
    cnv.UJ_type("jal","func","a0") #convert the instruction
    
## Helper Functions

Here are a few functions that might be useful:

### getOutputType()

This function simply prints the output type that has been initially selected. Example usage:

    cnv = AssemblyConverter("bt") #initially write to binary and text file
    cnv.getOutputType()

This will print to console:
    
    Writing to binary file
    Writing to text file

### setOutputType()

This function allows the option to change the output type after initialization. Example usage:

    cnv = AssemblyConverter("bt") #initially write to binary and text file
    cnv.setOutputType("p") #now only print to console

### instructionExists()

This function returns a boolean for whether a provided instruction exists in the system. Example usage:

    instructionExists("add") #yields true
    instructionExists("hello world") #yields false
    
<!-- ### addPseudo()-->
