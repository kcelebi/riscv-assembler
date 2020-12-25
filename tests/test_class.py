'''
TASKS

[] fix __all__
[] make getOutputType tests and other functions
[] get rid of 2.7 suport
[] push to add requirements
[] addPseudo function
'''
import pytest
from pathlib import Path
from riscv_assembler.convert import AssemblyConverter
#TESTS

#test simple.s file, writes to txt and bin
def func0():
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test0.s"
	return cnv.convert_ret(str(path))

def func1():
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test1.s"
	return cnv.convert_ret(str(path))

def func2():
	outarr = []
	cnv = AssemblyConverter()

	outarr.append(cnv.getOutputType())
	cnv.setOutputType("p")
	cnv.setOutputType("bt")
	outarr.append(cnv.getOutputType())

	return outarr

def func3():
	outarr = []
	cnv = AssemblyConverter()

	outarr.append(cnv.instructionExists("add"))
	outarr.append(cnv.instructionExists("rabu"))
	outarr.append(cnv.instructionExists("bapu"))
	outarr.append(cnv.instructionExists("sub"))
	outarr.append(cnv.instructionExists("xori"))

	return outarr

def func4():
	cnv = AssemblyConverter(nibble=True)

	path = Path(__file__).parent / "assembly/test0.s"
	return cnv.convert_ret(str(path))

def func5():
	cnv = AssemblyConverter(nibble=True)

	path = Path(__file__).parent / "assembly/test1.s"
	return cnv.convert_ret(str(path))

def test_0():
	assert func0() == ['00000000000000000000000010110011']

def test_1():
	assert func1() == ['00000010000001000000001010010011']

def test_2():
	assert func2() == ["b", "bt"]

def test_3():
	assert func3() == [True, False, False, True, True]

def test_4():
	assert func4() == ['0000	0000	0000	0000	0000	0000	1011	0011']

def test_5():
	assert func5() == ['0000	0010	0000	0100	0000	0010	1001	0011']
