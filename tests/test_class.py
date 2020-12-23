from convert_class import AssemblyConverter

#TESTS

#test simple.s file, writes to txt and bin
def test0():
	cnv = AssemblyConverter("tests/assembly/simple.s", "tb")

	cnv.convert()

	ans = "tests/expected/simple/txt/simple.txt"
	a = open(ans,"r")
	a_line = a.readline()

	file = "output/simple/txt/simple.txt"
	f = open(file,"r")
	f_line = f.readline()

	i =0
	while a_line != "":
		if a_line != f_line:
			print("{}: {}".format(i, a_line))
			print("{}: {}".format(i, f_line))
		assert a_line == f_line, "Check file"
		f_line = f.readline()
		a_line = a.readline()
		i+=1

test0()
