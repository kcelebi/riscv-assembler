'''
	Current Functionality:
		- Read given file
		- Tokenize that file, split up variables on each line
			- Identify function, registers, variables
		- Convert tokens of that line to machine code
		- Output to text, bin, or console


	Questions:
		- Do we want the object to save the code?
		- 

	Immediate ToDos:
		- Add decorators + properties
		- Add checks & helper methods
'''

from instr_arr import *
from parse import *

class AssemblyConverter:

	def __init__(self, output_mode = 'b', nibble_mode = False, hex_mode = False):
		self.output_mode = __check_output_mode(output_mode)
		self.nibble_mode = __check_nibble_mode(nibble_mode)
		self.hex_mode = __check_hex_mode(hex_mode)

	def __str__(self):
		return "Output: {output_mode}, Nibble: {nibble_mode}, Hex: {hex_mode}".format(
			output_mode = self.output_mode,
			nibble_mode = self.nibble_mode,
			hex_mode = self.hex_mode
		)

	def __repr__(self):
		return "Output: {output_mode}, Nibble: {nibble_mode}, Hex: {hex_mode}".format(
			output_mode = self.output_mode,
			nibble_mode = self.nibble_mode,
			hex_mode = self.hex_mode
		)

	def clone(self):
		return AssemblyConverter(
			output_mode = self.output_mode,
			nibble_mode = self.nibble_mode,
			hex_mode = self.hex_mode
		)

	@staticmethod
	def __check_output_mode(x):
		assert x in ['b', 't', 'p', None], "Output Mode needs to be one of b(inary), t(ext), p(rint), or None."
		return x

	@staticmethod
	def __check_nibble_mode(x):
		assert type(x) == bool, "Nibble mode needs to be a boolean."
		return x

	@staticmethod
	def __check_hex_mode(x):
		assert type(x) == bool, "Hex mode needs to be a boolean."
		return x

	'''
		Property: whether to return as hex or not
			True = hex
			False = binary
	'''
	@property
	def hex_mode(self):
		return self.hex_mode

	'''
		Property: the way to output machine code
			Options: 'b', 't', 'p'
	'''
	@property
	def output_mode(self):
		return self.output_mode

	'''
		Property: whether to print in nibbles (only applicable for text or print)
			True = nibble
			False = full number
	'''
	@property
	def nibble_mode(self):
		return self.nibble_mode

	@staticmethod
	def parse(file):
		...

	'''
		Put it all together
	'''
	def convert(self, file):
		...

