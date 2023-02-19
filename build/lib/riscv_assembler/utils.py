from pathlib import Path
import math

__all__ = ['Toolkit','nibbleForm']

#-----------------------------------------------------------------------------------------		
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def nibbleForm(x,delim = '\t'):
	fin_str = ""
	for i in range(0,len(x),4):
		fin_str += (x[i:i+4] + delim)
	return fin_str[:-1]

def flatten(x):
	arr = []
	for e in x:
		if not isinstance(e, list):
			arr.append(e)
		else:
			arr.extend(e)
	return arr


#-----------------------------------------------------------------------------------------		
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

class Toolkit:

	def __init__(self, filename = ""):
		R_instr = [
			"add","sub", "sll", 
			"sltu", "xor", "srl", 
			"sra", "or", "and",
			"addw", "subw", "sllw",
			"slrw", "sraw", "mul",
			"mulh", "mulu", "mulsu",
			"div", "divu", "rem",
			"remu"
		]
		I_instr = [
			"addi", "lb", "lw",
			"ld", "lbu", "lhu",
			"lwu", "fence", "fence.i", 
			"slli", "slti", "sltiu", 
			"xori", "slri", "srai",
			"ori", "andi", "addiw",
			"slliw", "srliw", "sraiw", 
			"jalr", "ecall", "ebreak", 
			"CSRRW", "CSRRS","CSRRC", 
			"CSRRWI", "CSRRSI", "CSRRCI" 
		]
		S_instr = [
			"sw", "sb", "sh", 
			"sd"
		]
		SB_instr = [
			"beq", "bne", "blt", 
			"bge", "bltu", "bgeu"
		]
		U_instr = ["auipc", "lui"]
		UJ_instr = ["jal"]
		pseudo_instr = [
			"beqz", "bnez", "li", 
			"mv", "j", "jr", 
			"la", "neg", "nop", 
			"not", "ret", "seqz", 
			"snez", "bgt", "ble"
		]

		self.instructions = []
		self.filename = filename
		self.r_map = {}
		self.instr_data = {}
		#get instruction data and register mapping
		self.r_map, self.instr_data = self.__pre()
		if filename != "":
			self.code = self.__read_in_advance()
		
		self.all_instr = flatten([
			R_instr, I_instr, S_instr,
			SB_instr, U_instr, UJ_instr, 
			pseudo_instr
		])

		self.R_instr = R_instr
		self.I_instr = I_instr
		self.S_instr = S_instr
		self.SB_instr = SB_instr
		self.U_instr = U_instr
		self.UJ_instr = UJ_instr
		self.pseudo_instr = pseudo_instr

	def __str__():
		return "Toolkit(filename={})".format(self.filename)

			

	def hex(self,x,leading_zero=True):
		if leading_zero:
			num = str(hex(int(x,2)))
			return "0x"+num[2::].zfill(8)
		else:
			return str(hex(int(x,2)))

	def __pre(self):
		#register mapping
		#make dictionary
		
		r_p = {}
		rmap_path = Path(__file__).parent / "data/reg_map.dat"	
		f = open(rmap_path,"r")
		line = f.readline()

		#assign mapping 
		while line != "":
			elems = line.split(" ")
			r_p[elems[0]] = elems[1] 
			line = f.readline()

		f.close()
		#index for instr_data

		#order is [opcode, f3, f7]
		i_data = {}
		instr_path = Path(__file__).parent / "data/instr_data.dat"
		f = open(instr_path,"r")
		line = f.readline()

		#assign data
		while line != "":
			elems = line.replace("\n","").split(" ")
			i_data[elems[0]] = elems[1::]
			line = f.readline()
		f.close()

		return r_p,i_data


	#READ FILE IN ADVANCE
	def __read_in_advance(self):
		code = []
		file = open(self.filename, "r")

		#store the lines in the arr
		line = file.readline()
		while line != "":
			line = line.strip()
			clean = flatten([elem.replace("\n","").split(",") for elem in line.split(" ")])
			if line == "" or not self.__valid_line(clean, True):
				line = file.readline()
				continue
			code.append(line.strip())
			line = file.readline()

		return code

	#helper methods
	def __reg_map(self,x):
		return self.r_map[x]

	def __reg_to_bin(self,x):
		return self.__binary(int(x[1::]), 5)

	def __binary(self, x, size):
		byte_num = math.ceil(size/8)
		b_num = x.to_bytes(byte_num, byteorder = 'big', signed = True)

		fin_bin = ''.join(format(byte, '08b') for byte in b_num)
		
		if byte_num*8 == size:
			return fin_bin
		return fin_bin[len(fin_bin)-size:len(fin_bin)]

	def calcJump(self, x,line_num, filename):
		#calc line number of func
		self.filename = filename
		self.code = self.__read_in_advance()
		for i in range(len(self.code)):
			if x+":" == self.code[i]:
				return (i - line_num)*4 #how many instructions to jump ahead/behind
		#print("Address not found")
		return -10 #if not found

	def R_type(
			self, instr, rs1, 
			rs2, rd):

		if instr not in self.R_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.instr_data[instr][f7],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def I_type(
			self, instr, rs1, 
			imm, rd):

		if instr not in self.I_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def S_type(
			self, instr, rs1, 
			rs2, imm):

		if instr not in self.S_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12)[::-1][5:12][::-1],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			self.__binary(int(imm),12)[::-1][0:5][::-1],
			self.instr_data[instr][opcode]
		])

	def SB_type(
			self, instr, rs1, 
			rs2, imm):

		if instr not in self.SB_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			"".join([
				self.__binary(int(imm),13)[::-1][12][::-1],
				self.__binary(int(imm),13)[::-1][5:11][::-1]
			]),
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			self.instr_data[instr][f3],
			"".join([
				self.__binary(int(imm),13)[::-1][1:5][::-1],
				self.__binary(int(imm),13)[::-1][11][::-1]
			]),
			self.instr_data[instr][opcode]
		])


	def U_type(
			self, instr, 
			imm, rd):

		if instr not in self.U_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),32)[::-1][12:32][::-1],
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])

	def UJ_type(
			self, instr, 
			imm, rd):

		if instr not in self.UJ_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return  "".join([
			"".join([
				self.__binary(int(imm),21)[::-1][20][::-1], self.__binary(int(imm),21)[::-1][1:11][::-1],
				self.__binary(int(imm),21)[::-1][11][::-1], self.__binary(int(imm),21)[::-1][12:20][::-1]
			]),		
			self.__reg_to_bin(rd),
			self.instr_data[instr][opcode]
		])




