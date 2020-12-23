from convert_class import AssemblyConverter

#TESTS

#test simple.s file, writes to txt and bin
def test0():
	cnv = AssemblyConverter("tests/assembly/simple.s", "tb")

	cnv.convert()

	#need to make expected outputs
	'''ans = "tests/expected/simple/txt/simple.txt"
	a = open(ans,"r")
	a_line = a.readline()

	file = "output/simple/txt/simple.txt"
	f = open(file,"r")
	f_line = f.readline()'''

test0()
