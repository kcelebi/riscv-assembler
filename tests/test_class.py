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
from riscv_assembler.convert import *
#TESTS

#test simple.s file, writes to txt and bin
def func0():
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test0.s"
	return cnv.convert_ret(path)

def func1():
	cnv = AssemblyConverter()

	path = Path(__file__).parent / "assembly/test1.s"
	return cnv.convert_ret(path)

def func2():
	outarr = []
	cnv = AssemblyConverter()

	outarr.append(cnv.getOutputType())
	cnv.setOutputType("p")
	cnv.setOutputType("bt")
	outarr.append(cnv.getOutputType())

	return outarr

def test_0():
	assert func0() == ['01100110000000000000000010000000']

def test_1():
	assert func1() == ['00000010000001000000001010010011']

def test_2():
	assert func2() == ["b", "bt"]
