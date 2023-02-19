from instr_arr import *

__all__ = ['reg_map', 'instr_map', 'read_file']

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

def handle_inline_comments(x):
	if "#" in x:
		pos = x.index("#")
		if pos != 0 and pos != len(x)-1:
			return x[0:pos]
	return x

def read_file(file):
	code = []
	file = open(file, "r")

	line = file.readline()
	while line != "":
		line = line.strip()
		if len(line) > 0 and valid_line(line, True):
			code += [interpret_line(line)]
			line = file.readline()

	return code

def interpret_line(line):
	tokens = handle_inline_comments(line).split()
	f = determine_type(tokens[0])
	return f(tokens)

def determine_type(tk):
	instr_sets = [R_instr, I_instr, S_instr, SB_instr, U_instr, UJ_instr]
	#funcs = [R, I, S, SB, U, UJ]
	parsers = [Rp, Ip, Sp, SBp, Up ,UJp]
	for i in range(len(instr_sets)):
		if tk in instr_sets[i]:
			return parsers[i]
	raise BadInstructionError()

class Parser:
	def organize(self, *args):
		raise NotImplementedError()

	def __call__(self, *args):
		return self.organize()

class _R_parse(Parser):
	def organize(tokens):
		instr, rs1, rs2, rd = tokens[0], reg_map[tokens[2]], reg_map[tokens[3]], reg_map[tokens[1]]
		return R(instr, rs1, rs2, rd)

class _I_parse(Parser):
	def organize(tokens):
		instr, rs1, imm, rd = tokens[0], None, None, None
		if instr == "jalr":
			if len(tokens) == 4:
				rs1, imm, rd = reg_map[tokens[2]], JUMP(tokens[3]), reg_map[tokens[1]]
			else:
				rs1, imm, rd = reg_map[tokens[1]], 0, reg_map["x1"]
		elif instr == "lw":
			rs1, imm, rd = reg_map[tokens[3]], tokens[2], reg_map[tokens[1]]
		else:
			rs1, imm, rd = reg_map[tokens[2]], tokens[3], reg_map[tokens[1]]

		return I(instr, rs1, imm, rd)

class _S_parse(Parser):
	def organize(tokens):
		instr, rs1, rs2, imm = tokens[0], None, None, None
		


reg_map = register_map()
instr_map = instruction_map()
Rp, Ip, Sp, SBp, Up, UJp = _R_parse(), _I_parse(), _S_parse(), _SB_parse(), _U_parse(), _UJ_parse()