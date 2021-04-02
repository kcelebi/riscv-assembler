from convert import AssemblyConverter
import os

__all__ = ['ProjectConverter']

class ProjectConverter:

	def __init__(self, root = '', output_type='b', nibble = False, filename = "", hexMode = False):
		self.root = root #should be relative path from python script using pkg
		if root == '':
			self.root = os.getcwd()

		self.hexMode = hexMode
		self.nibble = nibble

		if "b" not in output_type and "t" not in output_type and "p" not in output_type:
			raise IncorrectOutputType()
		else:
			self.output_type = output_type

		self.files = [x for x in os.listdir(self.root) if x[-2:] == '.s'] #need to raise error just in case
		#take only .s files

	def __str__(self):
		return "**\n  	ProjectConverter(output_type={}, nibble={}, hexmode={})\n\t- root: {}\n\t- Files: {}\n**".format(
			self.output_type, self.nibble,
			self.hexMode,self.root,
			self.files
		)

	#convert the whole project to machine
	def convert(self):
		ac = AssemblyConverter()