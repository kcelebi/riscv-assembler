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

class AssemblyConverter:

	def __init__(self, output_mode = 'b', nibble_mode = False, hex_mode = False):
		self.output_mode = output_mode
		self.nibble_mode = nibble_mode
		self.hex_mode = hex_mode

	def __str__(self):
		...

	def __repr__(self):
		...

	def clone(self):
		...

	@staticmethod
	def __check_output_mode(x):
		...

	@staticmethod
	def __check_nibble_mode(x):
		...

	@staticmethod
	def __check_hex_mode(x):
		...

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





