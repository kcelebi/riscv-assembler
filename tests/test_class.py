import pytest
from pathlib import Path
from riscv_assembler.convert import *
from riscv_assembler.utils import *
#TESTS

#test simple.s file, writes to txt and bin
def func0():
	#test convert, should return array
	cnv = AssemblyConverter()

	path = str(Path(__file__).parent / "assembly/test0.s")
	return cnv.convert(path)

def func1():
	#test convert
	cnv = AssemblyConverter()

	path = str(Path(__file__).parent / "assembly/test1.s")
	return cnv.convert(path)

def func2():
	#test get/set OutpuType
	outarr = []
	cnv = AssemblyConverter()

	outarr += [cnv.output_mode]
	cnv.output_mode = 'p'
	cnv.output_mode = 'f'
	outarr += [cnv.output_mode]

	return outarr

def func4():
	#test nibble form for convert
	cnv = AssemblyConverter(nibble=True)

	path = str(Path(__file__).parent / "assembly/test0.s")
	return cnv.convert(path)

def func5():
	#test nibbleForm for convert
	cnv = AssemblyConverter(nibble=True)

	path = str(Path(__file__).parent / "assembly/test1.s")
	return cnv.convert(path)

def func7():
	#test calcJump()
	path = str(Path(__file__).parent / "assembly/test2.s")

	cnv = AssemblyConverter(filename = path)

	return cnv.calcJump("loop",2) #3-1

def func8():
	#test hex
	out_arr = []
	cnv = AssemblyConverter(hexMode = True)

	path = Path(__file__).parent / "assembly/test0.s"
	out_arr.extend(cnv.convert(str(path)))

	path = Path(__file__).parent / "assembly/test1.s"
	out_arr.extend(cnv.convert(str(path)))

	return out_arr

#-----------------------------------------------------------------------------------------		
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def test_0():
	assert func0() == ['00000000000000000000000010110011']

def test_1():
	assert func1() == ['00000010000001000000001010010011']

def test_2():
	assert func2() == ["a", "f"]

def test_4():
	assert func4() == ['0000\t0000\t0000\t0000\t0000\t0000\t1011\t0011']

def test_5():
	assert func5() == ['0000\t0010\t0000\t0100\t0000\t0010\t1001\t0011']

'''def test_7():
	assert func7() == 4'''

def test_8():
	assert func8() == ['0x000000b3', '0x02040293']