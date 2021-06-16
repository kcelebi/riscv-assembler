from riscv_assembler.utils import *
from pathlib import Path
import pytest

def func0():
	return nibbleForm("000011110000010100001111",'\t')

def func1():
	tk = Toolkit()
	return tk.R_type('add', 'x0','x0','x0')

def test_0():
	assert func0() == "0000\t1111\t0000\t0101\t0000\t1111"

def test_1():
	assert func1() == '00000000000000000000000000110011'