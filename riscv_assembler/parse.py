from instr_arr import *

__all__ = ['read_file']

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
	parsers = [Rp, Ip, Sp, SBp, Up ,UJp]
	for i in range(len(instr_sets)):
		if tk in instr_sets[i]:
			return parsers[i]
	raise BadInstructionError()