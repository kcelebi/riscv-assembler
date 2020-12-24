import sys
import os
from bitstring import BitArray
import math as m
from pathlib import Path

__all__ = ['riscv-assembler',"riscv_assembler","AssemblyConverter","R_type","I_type","S_type","SB_type", "U_type", "UJ_type", "instructionExists", "getOutputType", "setOutputType"]
class WrongInstructionSize( Exception ):
	#raised when instruction size is not 32 bits
	def __init__(self, message = "Instruction is not 32 bits, possible assembly file error"):
		self.message = message
		super().__init__(self.message)

class NotBinaryNumber( Exception ):
	#raised when instructions contains non-binary elements
	def __init__(self, message = "Instruction is not binary"):
		self.message = message
		super().__init__(self.message)

class IncorrectOutputType( Exception ):
	def __init__(self, message = "Output type is used incorrectly, should be bt, b, or t"):
		self.message = message
		super().__init__(self.message)

class WrongFileType( Exception ):
	def __init__(self, message = "File must have .s extension for assembly code"):
		self.message = message
		super().__init__(self.message)

class EmptyFile( Exception ):
	def __init__(self, message = "File either doesn't exist, has no code, or all is commented out.\nInvestigate any tab/spacing syntax issues"):
		self.message = message
		super().__init__(self.message)
class AssemblyConverter:

	#	__flatten__ an array
	def __flatten(self,x):
		arr = []
		for e in x:
			if not isinstance(e, list):
				arr.append(e)
			else:
				arr.extend(e)
		return arr

	def __init__(self, output_type='b'):
		self.filename = ""
			
		self.code = []
		self.instructions = []
		self.r_map = {}
		self.instr_data = {}
		if "b" not in output_type and "t" not in output_type and "p" not in output_type:
			raise IncorrectOutputType()
		else:
			self.output_type = output_type

		#instr types
		self.R_instr = ["add","sub", "sll", "sltu", "xor", "srl", "sra", "or", "and", "addw", "subw", "sllw", "slrw", "sraw", "mul", "mulh", "mulu", "mulsu", "div", "divu", "rem", "remu"]
		self.I_instr = ["addi", "lb", "lw", "ld", "lbu", "lhu", "lwu", "fence", "fence.i", "slli", "slti", "sltiu", "xori", 
		"slri", "srai", "ori", "andi", "addiw", "slliw", "srliw", "sraiw", "jalr", "ecall", "ebreak", "CSRRW", "CSRRS",
		 "CSRRC", "CSRRWI", "CSRRSI", "CSRRCI"]
		self.S_instr = ["sw", "sb", "sh", "sd"]
		self.SB_instr = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
		self.U_instr = ["auipc", "lui"]
		self.UJ_instr = ["jal"]

		self.pseudo_instr = ["beqz", "bnez", "li", "mv", "j", "jr", "la", "neg", "nop", "not", "ret", "seqz", "snez", "bgt", "ble"]

		self.all_instr = self.__flatten([self.R_instr, self.I_instr, self.S_instr, self.SB_instr, self.U_instr, self.UJ_instr, self.pseudo_instr])
	#helper methods
	def __reg_map(self,x):
		return self.r_map[x]

	def __reg_to_bin(self,x):
		return self.__binary(int(x[1::]), 5)

	#for jumps, calculates hex address of func
	def calc_jump(self, x,line_num):
		#calc line number of func
		for i in range(len(self.code)):
			if x+":" == self.code[i]:
				return (i - line_num)*4 #how many instructions to jump ahead/behind
		#print("Address not found")
		return 0 #if not found

	def __binary(self, x, size):
		byte_num = m.ceil(size/8)
		b_num = x.to_bytes(byte_num, byteorder = 'big', signed = True)

		fin_bin = ''.join(format(byte, '08b') for byte in b_num)
		
		if byte_num*8 == size:
			return fin_bin
		return fin_bin[len(fin_bin)-size:len(fin_bin)]

	#checks if line is comment, empty space, or .global .text
	def __valid_line(self, x, allow_colon = False):
		if x[0][0] == "#" or x[0][0] == "\n" or x[0][0] == "" or x[0][0] == ".":
			return False

		if not allow_colon and x[0][-1] == ":" :
			return False
		return True

	#gets rid of inline comments
	def __handle_inline_comments(self,x):
		if "#" in x:
			pos = x.index("#")
			if pos != 0 and pos != len(x)-1:
				return x[0:pos]

		return x

	#change output type
	def setOutputType(self, x):
		self.output_type = x

	#return output type
	def getOutputType(self):
		for e in self.output_type:
			if e == "p":
				print("Printing to console")
			elif e == "b":
				print("Writing to binary file")
			elif e == "t":
				print("Writing to text file")
			else:
				print("Messed up output type")
				raise IncorrectOutputType(e)

	#checks whether instruction is in system
	def instructionExists(x):
		return x in self.all_instr


	#add custom pseudo instruction
	#to be implemented later
	'''
	def addPseudo(instr, op_arr):
		return ""
	'''
	
	#create instruction
	def R_type(self,instr, rs1, rs2, rd):
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.instr_data[instr][f7],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def I_type(self, instr, rs1, imm, rd):
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def S_type(self, instr, rs1, rs2, imm):
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12)[::-1][5:12][::-1],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__binary(int(imm),12)[::-1][0:5][::-1],
			self.instr_data[instr][opcode]
		])

	def SB_type(self, instr, rs1, rs2, imm):
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			"".join([self.__binary(int(imm),13)[::-1][12][::-1],self.__binary(int(imm),13)[::-1][5:11][::-1]]),
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			"".join([self.__binary(int(imm),13)[::-1][1:5][::-1],self.__binary(int(imm),13)[::-1][11][::-1]]),
			self.instr_data[instr][opcode]
		])


	def U_type(self, instr, imm, rd):
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),32)[::-1][12:32][::-1],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def UJ_type(self, instr, imm, rd):
		opcode = 0;f3 = 1;f7 = 2
		return  "".join([
			"".join([self.__binary(int(imm),21)[::-1][20][::-1],self.__binary(int(imm),21)[::-1][1:11][::-1],self.__binary(int(imm),21)[::-1][11][::-1],self.__binary(int(imm),21)[::-1][12:20][::-1]]),		
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])


	##Procedural functions

	#initializing mapping and instruction data
	def __pre(self):
		#register mapping
		#make dictionary
		rmap_path = Path(__file__).parent / "data/reg_map.dat"	
		r_map = {}
		
		f = open(rmap_path,"r")
		#f = open("riscinterpreter/data/reg_map.dat", "r")
		#f = open("src/data/reg_map.dat","r")
		line = f.readline()

		#assign mapping 
		while line != "":
			elems = line.split(" ")
			r_map[elems[0]] = elems[1] 
			line = f.readline()

		f.close()
		#index for instr_data
		opcode = 0
		f3 = 1
		f7 = 2

		#order is [opcode, f3, f7]
		instr_data = {}
		instr_path = Path(__file__).parent / "data/instr_data.dat"
		f = open(instr_path,"r")
		#f = open("riscinterpreter/data/instr_data.dat", "r")
		#f = open("src/data/instr_data.dat","r")
		line = f.readline()

		#assign data
		while line != "":
			elems = line.replace("\n","").split(" ")
			instr_data[elems[0]] = elems[1::]
			line = f.readline()
		f.close()

		return r_map,instr_data

	#READ FILE IN ADVANCE
	def __read_in_advance(self):
		code = []
		file = open(self.filename, "r")

		#store the lines in the arr
		line = file.readline()
		while line != "":
			line = line.strip()
			clean = self.__flatten([elem.replace("\n","").split(",") for elem in line.split(" ")])
			if line == "" or not self.__valid_line(clean, True):
				line = file.readline()
				continue
			code.append(line.strip())
			line = file.readline()

		return code

	#retrieve instructions
	def __get_instructions(self):
		#array to store instructions in
		instructions = [] 
		for i in range(len(self.code)):
			line = self.code[i]

			response = self.__interpret(line,i)
			if response != -1:
				instructions.append(response)

		return instructions

	#interpret each line and form instructions
	def __interpret(self,line,i):
		res = ""
		line = self.__handle_inline_comments(line)
		line = line.strip()
		#print(line)
		clean = self.__flatten([elem.replace("\n","").split(",") for elem in line.split(" ")])

		while "" in clean:
			clean.remove("")

		#check if line is comment, empty space, .global .text
		if not self.__valid_line(clean):
			return -1

		if clean[0] == "ecall":
			return -1

		if clean[0] == "sw" or clean[0] == "lw" or clean[0] == "lb" or clean[0] == "lh" or clean[0] == "sb" or clean[0] == "sh":
			#sw s0, 0(sp)
			w_spl = clean[2].split("(")
			clean[2] = w_spl[0]
			clean.append(w_spl[1].replace(")",""))

		if clean[0] in self.R_instr:
			res = self.R_type(clean[0], self.__reg_map(clean[2]), self.__reg_map(clean[3]), self.__reg_map(clean[1]))
			#print(res)
		elif clean[0] in self.I_instr:
			if clean[0] == "jalr":
				if len(clean) == 4:
					res = self.I_type(clean[0], self.__reg_map(clean[2]), self.calc_jump(clean[3],i),self.__reg_map(clean[1]))
				else:
					res = self.I_type(clean[0], self.__reg_map(clean[1]), "0", self.__reg_map("x1"))
			elif clean[0] == "lw":
				res = self.I_type(clean[0], self.__reg_map(clean[3]), clean[2], self.__reg_map(clean[1]))
			else:
				res = self.I_type(clean[0], self.__reg_map(clean[2]), clean[3], self.__reg_map(clean[1]))
			#print(res)
		elif clean[0] in self.S_instr:
			res = self.S_type(clean[0], self.__reg_map(clean[3]), self.__reg_map(clean[1]), clean[2])
			#print(res)
		elif clean[0] in self.SB_instr:
			res = self.SB_type(clean[0], self.__reg_map(clean[1]), self.__reg_map(clean[2]), self.calc_jump(clean[3],i))
			#print(res)
		elif clean[0] in self.U_instr:
			res = self.U_type(clean[0], clean[1], self.__reg_map(clean[2]))
			#print(res)
		elif clean[0] in self.UJ_instr:
			if len(clean) == 3:
				res = self.UJ_type(clean[0], self.calc_jump(clean[2],i), self.__reg_map(clean[1]))
			else:
				res = self.UJ_type(clean[0], self.calc_jump(clean[1],i), self.__reg_map("x1"))
			#print(res)
		elif clean[0] in self.pseudo_instr:
			#print(clean[0]  + " pseudo")

			if clean[0] == "li":
				res = self.I_type("addi",self.__reg_map(clean[1]), self.calc_jump(clean[2],i), self.__reg_map(clean[1]))
			elif clean[0] == "nop":
				res = self.I_type("addi", self.__reg_map("x0"), "0", self.__reg_map("x0"))
			elif clean[0] == "mv":
				res = self.I_type("addi", self.__reg_map(clean[2]), "0", self.__reg_map(clean[1]))
			elif clean[0] == "not":
				res = self.I_type("xori", self.__reg_map(clean[2]), "-1", self.__reg_map(clean[1]))
			elif clean[0] == "neg":
				res = self.R_type("sub", self.__reg_map("x0"), self.__reg_map(clean[2]), self.__reg_map(clean[1]))
			elif clean[0] == "la":
				res = self.U_type("auipc", self.calc_jump(clean[2],i), self.__reg_map(clean[1]))
			elif clean[0] == "j":
				res = self.UJ_type("jal", self.calc_jump(clean[1],i), self.__reg_map("x0"))
			elif clean[0] == "jr":
				res = self.I_type("jalr", self.__reg_map(clean[1]), "0", self.__reg_map("x0"))
			elif clean[0] == "ret":
				res = self.I_type("jalr", self.__reg_map("x1"), "0", self.__reg_map("x0"))
			elif clean[0] == "bgt":
				res = self.SB_type("blt", self.__reg_map(clean[2]), self.__reg_map(clean[1]), self.calc_jump(clean[3],i))
			elif clean[0] == "ble":
				res = self.SB_type("bge", self.__reg_map(clean[2]), self.__reg_map(clean[1]), self.calc_jump(clean[3], i))
		else:
			#debugging
			print("Error: " + line)

			#check for critical errors
			for e in res:
				if int(e) != 0 and int(e) != 1:
					raise Not__binaryNumber(res)
			if len(res) != 32:
				raise WrongInstructionSize(len(res))

		#return instruction
		return res

	#AFTER READING FILE	
	def __post(self):

		if len(self.instructions) == 0:
			raise EmptyFile
		if "b" in self.output_type:
			print("-----Writing to __binary file-----")
			#make it [their .s file name].bin
			fname = self.filename.split("/")[-1]
			print("Output file: " + fname[:-2] + ".bin")

			if not os.path.exists(fname[:-2]):
				os.system("mkdir {}".format(fname[:-2]))
				os.system("mkdir {}/bin".format(fname[:-2]))
			else:
				if not os.path.exists("bin"):
					os.system("mkdir {}/bin".format(fname[:-2]))

			#with open("output/"+fname[:-2]+"/bin/" + fname[:-2] + ".bin", "wb") as f:
			with open(fname[:-2]+"/bin/" + fname[:-2] + ".bin", "wb") as f:
				for elem in self.instructions:
					#split into bytes
					byte_array = [elem[i:i+8] for i in range(0,len(elem),8)]
					byte_list = [int(b,2) for b in byte_array]

					f.write(bytearray(byte_list))
				f.close()

		if "t" in self.output_type:
			print("------Writing to Text file------")
			#make it [their .s file name].txt

			fname = self.filename.split("/")[-1]
			print("Output file: " + fname[:-2] + ".txt")

			if not os.path.exists(fname[:-2]):
				os.system("mkdir {}".format(fname[:-2]))
				os.system("mkdir {}/txt".format(fname[:-2]))
			else:
				if not os.path.exists("txt"):
					os.system("mkdir {}/txt".format(fname[:-2]))

			#with open("output/"+fname[:-2]+"text/" + fname[:-2] + ".txt", "w") as f:
			with open(fname[:-2]+"/txt/" + fname[:-2] + ".txt", "w") as f:
				for elem in self.instructions:
					f.write(elem + "\n")

		if "p" in self.output_type:
			print("------Printing Output------")
			for e in self.instructions:
				print(e)

		print("Number of instructions: {}".format(len(self.instructions)))

	#DO THE MAGIC
	def convert(self,filename):
		if filename[-2::] != ".s":
			raise WrongFileType
		self.filename = filename
		self.r_map, self.instr_data = self.__pre()
		self.code = self.__read_in_advance()
		self.instructions = self.__get_instructions()
		self.__post()