'''
	Current Functionality:
		- Read given file
		- Tokenize that file, split up variables on each line
			- Identify function, registers, variables
		- Convert tokens of that line to machine code
		- Output to text, bin, or console

	Immediate ToDos:
		- Implement hexmode
		- Go through and fix the instruction conversions themselves
		- Update tests
'''

from riscv_assembler.instr_arr import *
from riscv_assembler.parse import *

__all__ = ['AssemblyConverter']

class AssemblyConverter:

	def __init__(self, output_mode = 'a', nibble_mode = False, hex_mode = False):
		self.__output_mode = self.__check_output_mode(output_mode)
		self.__nibble_mode = self.__check_nibble_mode(nibble_mode)
		self.__hex_mode = self.__check_hex_mode(hex_mode)

	def __str__(self):
		return "Output: {output_mode}, Nibble: {nibble_mode}, Hex: {hex_mode}".format(
			output_mode = self.__output_mode,
			nibble_mode = self.__nibble_mode,
			hex_mode = self.__hex_mode
		)

	def __repr__(self):
		return "Output: {output_mode}, Nibble: {nibble_mode}, Hex: {hex_mode}".format(
			output_mode = self.__output_mode,
			nibble_mode = self.__nibble_mode,
			hex_mode = self.__hex_mode
		)

	def clone(self):
		return AssemblyConverter(
			output_mode = self.__output_mode,
			nibble_mode = self.__nibble_mode,
			hex_mode = self.__hex_mode
		)

	def __check_output_mode(self, x):
		mod = ''.join(sorted(x.split()))
		assert mod in ['a', 'f', 'p', None], "Output Mode needs to be one of a(rray), f(ile), p(rint), or None."
		return x

	def __check_nibble_mode(self, x):
		assert type(x) == bool, "Nibble mode needs to be a boolean."
		return x

	def __check_hex_mode(self, x):
		assert type(x) == bool, "Hex mode needs to be a boolean."
		return x

	'''
		Property: the way to output machine code
			Options: 'a', 'f', 'p'
	'''
	@property
	def output_mode(self):
		return self.__output_mode

	@output_mode.setter
	def output_mode(self, x):
		self.__output_mode = x

	'''
		Property: whether to print in nibbles (only applicable for text or print)
			True = nibble
			False = full number
	'''
	@property
	def nibble_mode(self):
		return self.__nibble_mode

	@nibble_mode.setter
	def nibble_mode(self, x):
		self.__nibble_mode = x

	'''
	Property: whether to return as hex or not
		True = hex
		False = binary
	'''
	@property
	def hex_mode(self):
		return self.__hex_mode

	@hex_mode.setter
	def hex_mode(self, x):
		self.__hex_mode = x

	'''
		Put it all together. Need to modify for output type.

		Input is either a file name or string of assembly.
	'''
	def convert(self, input, file = None):
		output = Parser(input)

		assert len(output) > 0, "Provided input yielded nothing from parser. Check input."

		if self.__output_mode == 'a':
			return output
		elif self.__output_mode == 'f':
			assert file != None, "For output mode to file, need to provided file name."
			self.write_to_file(output, file)
			return
		elif self.__output_mode == 'p':
			print(output)
			return

		raise NotImplementedError()

	def write_to_file(self, output, file):
		if file[-4:] == '.bin':
			with open(file, 'wb') as f:
				for instr in output:
					byte_array = [instr[i:i+8] for i in range(0,len(instr),8)]
					byte_list = [int(b,2) for b in byte_array]
					f.write(bytearray(byte_list))

			return

		elif file[-4:] == '.txt':
			with open(file, 'w') as f:
				for instr in output:
					f.write(instr + "\n")

			return

		raise NotImplementedError()


