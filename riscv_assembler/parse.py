from riscv_assembler.instr_arr import *

__all__ = ['Parser']

class _Parser:

	'''
		Procedure:
			- Call read_file()
				- Strip the line and check valid_line()
				- interpret() the line
					- handle_inline_comments()
					- determine_type() of instruction
						- returns appropriate function
					- return parsed version of line
				- combine the interpreted lines together
				- Return
	'''

	def __call__(self, *args):
		if self.is_file(*args):
			return self.read_file(*args)
		return [self.interpret(x) for x in args[0].split("\n")]

	def is_file(self, x):
		return True if '.s' in x or '/' in x else False

	'''
		In read_file(), Check if the inputted line is appropriate before
		parsing it.
	'''
	def valid_line(self, x, allow_colon = False):
		if x[0][0] == "#" or x[0][0] == "\n" or x[0][0] == "" or x[0][0] == ".":
			return False

		if not allow_colon and x[0][-1] == ":" :
			return False
		return True

	'''
		In interpret(), remove any comments in the line.
	'''
	def handle_inline_comments(self, x):
		if "#" in x:
			pos = x.index("#")
			if pos != 0 and pos != len(x)-1:
				return x[0:pos]
		return x

	'''
		Read the .s file provided and parse it completely.
	'''
	def read_file(self, file):
		code = []
		file = open(file, "r")

		line = file.readline()
		while line != "":
			line = line.strip()
			if len(line) > 0 and self.valid_line(line, True):
				code += [self.interpret(line)]
				line = file.readline()
		return code

	'''
		In read_file(), parse and return the machine code.
	'''
	def interpret(self, line):
		tokens = self.handle_inline_comments(line).split()
		f = self.determine_type(tokens[0])
		return f(tokens)

	'''
		In interpret(), determine which instruction set is being used
		and return the appropriate parsing function.
	'''
	def determine_type(self, tk):
		instr_sets = [R_instr, I_instr, S_instr, SB_instr, U_instr, UJ_instr]
		parsers = [Rp, Ip, Sp, SBp, Up ,UJp]
		for i in range(len(instr_sets)):
			if tk in instr_sets[i]:
				return parsers[i]
		raise BadInstructionError()

Parser = _Parser()