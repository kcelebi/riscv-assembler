'''
TASKS

[] fix __all__
[] make getOutputType tests and other functions
[] get rid of 2.7 suport
[] push to add requirements
[] addPseudo function
'''

from riscv_assembler.convert import AssemblyConverter
#TESTS

#test simple.s file, writes to txt and bin
def func0():
	cnv = AssemblyConverter()

	return cnv.convert_ret()

def test0():
	assert func0() == []
test0()
