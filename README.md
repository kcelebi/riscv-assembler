# riscv-assembler
RISC-V Assembly code assembler package.

This package contains tools and functions that can convert RISC-V Assembly code to machine code. The whole process is implemented using Python purely for understandability, less so for efficiency in computation. These tools can be used to convert given lines of code or whole files. For conversion, output file types are binary and text files.

# Installation

The package can be installed using pip:

`$ pip install riscv_assembler`

No other actions necessary.

# Usage

The package works through an `AssemblyConverter` class. We would first need to import this class:

`from riscv_interpreter.convert import AssemblyConverter`

We can now instantiate an object. The constructor requires a string that specifies the output file as either binary, text, or both. Here are acceptable usages:

    cnv = AssemblyConverter("bt") #binary and text
    cnv = AssemblyConverter("b") #just binary
    cnv = AssemblyConverter("t") #just text
    cnv = AssemblyConverter() #binary by default

### Convert
With this object we can apply our most powerful function : `convert()`. This function takes in a file name (with .s extension) from the local directory and converts it to the output file of your choice, specified by the object construction. Let's convert the file `simple.s`:

`cnv.convert("simple.s")`

Any empty files, fully commented files, or files without `.s` extension will not be accepted. The function creates a directory by truncating the extension of the file along with two subdirectories called `bin` and `txt` for the respective output files (for `simple.s` the directory would be `simple`). 
