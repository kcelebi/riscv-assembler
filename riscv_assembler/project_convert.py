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

		self.instr = {}
		self.failed = []
####--------------------------------------------------------------------------------------------------------
	def __str__(self):
		return "**\n  	ProjectConverter(output_type={}, nibble={}, hexmode={})\n\t- root: {}\n\t- Files: {}\n**".format(
			self.converter.output_type, self.converter.nibble,
			self.converter.hexMode, self.root,
			self.files
		)

	def __len__(self):
		return len(self.instr)

	'''def __add__(self, other):
		self.instr.extend(other.getInstructions())
		return self''' #fix this
####--------------------------------------------------------------------------------------------------------
	def setOutputType(self, x):
		self.converter.setOutputType(x)

	def getOutputType(self):
		return self.converter.getOutputType()

	def instructionExists(self, x):
		return self.converter.instructionExists(x)

	def setHex(self, x):
		self.converter.setHex(x)

	def getFiles(self):
		return self.files

	def getInstructions(self):
		return self.instr

	def getFailedConvert(self):
		return self.failed

	def addDict(self, f, x):
		if x != None:
			self.instr[f] = x
####--------------------------------------------------------------------------------------------------------
	#convert the whole project to machine
	def convert(self, files = []):
		self.failed = []
		if len(files) == 0: files = self.files
		if self.getOutputType() == 'r':
			g = [self.addDict(f, self.catch_convert(f)) for f in files]
			return self.instr
		no_ret = [catch_convert(f) for f in files]

	def catch_convert(self,f):
		try:
			return self.converter.convert(self.root + '/' + f)
		except:
			print("File " + f + " assembly failed")
			self.failed.append(f)
	
	##-----------PROJECT ASSEMBLY PROTOCOLS-----------##

	# - main idea is to track variables/funcs/filenames through diff files
	# - branching is important
	# - hierarchy of files: ie what is utils, what is used where
	# - func that searches thru files and finds instances, def instance
	# - make as new file? 