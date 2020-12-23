from convert_class import AssemblyConverter
#TESTS

#test simple.s file, writes to txt and bin
def test0():
	cnv = AssemblyConverter("tests/assembly/simple.s", "tb")

	cnv.convert()

test0()
