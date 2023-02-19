__all__ = ['reg_map', 'instr_map']
def register_map():
	path = Path(__file__).parent / "data/reg_map.dat"
	rmap = {}

	f = open(path, "r")
	line = f.readline()
	while line != "":
		e = read_line(line)
		rmap[e[0]] = e[1] 
		line = f.readline()
	f.close()

	return rmap

def instruction_map():
	path = Path(__file__).parent / "data/instr_data.dat"
	imap = {}

	f = open(path, "r")
	line = f.readline()
	while line != "":
		e = read_line(line)
		imap[e[0]] = e[1:]
		line = f.readline()
	f.close()

	return imap

def read_line(x):
	return line.split(" ")

def valid_line(x, allow_colon = False):
	if x[0][0] == "#" or x[0][0] == "\n" or x[0][0] == "" or x[0][0] == ".":
		return False

	if not allow_colon and x[0][-1] == ":" :
		return False
	return True

def read_file(file):
	code = []
	file = open(file, "r")

	line = file.readline()
	while line != "":
		line = line.strip()
		if line == "" or not valid_line(line, True):
			line = file.readline()
			continue
		...


reg_map = register_map()
instr_map = instruction_map()