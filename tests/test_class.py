import pytest
from pathlib import Path
from riscv_assembler.convert import *
#TESTS

#test simple.s file, writes to txt and bin
def func0():
	#test convert
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test0.s"
	return cnv.convert_ret(str(path))

def func1():
	#test convert
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test1.s"
	return cnv.convert_ret(str(path))

def func2():
	#test get/set OutpuType
	outarr = []
	cnv = AssemblyConverter()

	outarr.append(cnv.getOutputType())
	cnv.setOutputType("p")
	cnv.setOutputType("bt")
	outarr.append(cnv.getOutputType())

	return outarr

def func3():
	#test instructionExists
	outarr = []
	cnv = AssemblyConverter()

	outarr.append(cnv.instructionExists("add"))
	outarr.append(cnv.instructionExists("rabu"))
	outarr.append(cnv.instructionExists("bapu"))
	outarr.append(cnv.instructionExists("sub"))
	outarr.append(cnv.instructionExists("xori"))

	return outarr

def func4():
	#test nibble form for convert
	cnv = AssemblyConverter(nibble=True)

	path = Path(__file__).parent / "assembly/test0.s"
	return cnv.convert_ret(str(path))

def func5():
	#test nibbleForm for convert
	cnv = AssemblyConverter(nibble=True)

	path = Path(__file__).parent / "assembly/test1.s"
	return cnv.convert_ret(str(path))

def func6():
	#test R_type()
	out_arr = []

	cnv = AssemblyConverter()
	out_arr.append(cnv.R_type("add", "x0", "x0","x0"))
	out_arr.append(nibbleForm(cnv.R_type("add", "x0", "x0","x0")))

	return out_arr

def func7():
	#test calcJump()
	path = Path(__file__).parent / "assembly/test2.s"

	cnv = AssemblyConverter(filename = str(path))

	return cnv.calcJump("loop",2) #3-1


def test_0():
	assert func0() == ['00000000000000000000000010110011']

def test_1():
	assert func1() == ['00000010000001000000001010010011']

def test_2():
	assert func2() == ["b", "bt"]

def test_3():
	assert func3() == [True, False, False, True, True]

def test_4():
	assert func4() == ['0000\t0000\t0000\t0000\t0000\t0000\t1011\t0011']

def test_5():
	assert func5() == ['0000\t0010\t0000\t0100\t0000\t0010\t1001\t0011']

def test_6():
	assert func6() == ['00000000000000000000000000110011','0000\t0000\t0000\t0000\t0000\t0000\t0011\t0011']

def test_7():
	assert func7() == 4
