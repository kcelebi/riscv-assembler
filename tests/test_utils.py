from riscv_assembler.utils import *
from pathlib import Path
import pytest

def func0():
	return nibbleForm("000011110000010100001111",'\t')

def test_0():
	assert func0() == "0000\t1111\t0000\t0101\t0000\t1111"