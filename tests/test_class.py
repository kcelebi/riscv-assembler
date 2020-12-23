from convert_class import AssemblyConverter

#TESTS

def test0():

	cnv = AssemblyConverter("Assembly/simple.s", "t")

	cnv.convert()

	ans = "tests/simple/simple0.txt"
	a = open(ans,"r")
	a_line = a.readline()

	file = "output/text/simple0.txt"
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
