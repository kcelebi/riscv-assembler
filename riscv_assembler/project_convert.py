from convert import AssemblyConverter
import os

__all__ = ['ProjectConverter']

class NoAssemblyDirectory( Exception ):
	def __init__(self, message = "The provided directory has no Assembly (.s) files in it"):
		self.message = message
		super().__init__(self.message)

class ProjectConverter:

	def __init__(self, root = '', output_type='b', nibble = False, hexMode = False):
		self.root = root #should be relative path from python script using pkg
		if root == '':
			self.root = os.getcwd()

		self.converter = AssemblyConverter(output_type=output_type, nibble=nibble, hexMode=hexMode)

		self.files = [x for x in os.listdir(self.root) if x[-2:] == '.s'] #need to raise error just in case
		if len(self.files) == 0:
			raise NoAssemblyDirectory()
		#take only .s files

	def __str__(self):
		return "**\n  	ProjectConverter(output_type={}, nibble={}, hexmode={})\n\t- root: {}\n\t- Files: {}\n**".format(
			self.converter.output_type, self.converter.nibble,
			self.converter.hexMode, self.root,
			self.files
		)

	#convert the whole project to machine
	#def convert(self):

	
	##-----------PROJECT ASSEMBLY PROTOCOLS-----------##

	# - main idea is to track variables/funcs/filenames through diff files
	# - branching is important
	# - hierarchy of files: ie what is utils, what is used where
	# - func that searches thru files and finds instances, def instance
	# - make as new file? 