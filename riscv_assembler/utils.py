
__all__ = ['tools','nibbleForm']


def nibbleForm(x):
	fin_str = ""
	for i in range(0,len(x),4):
		fin_str += (x[i:i+4] + "\t")
	return fin_str[:-1]

class tools:
	r_map = {}
	instr_data = {}

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

	all_instr = flatten([
		R_instr, I_instr, S_instr,
		SB_instr, U_instr, UJ_instr, 
		pseudo_instr
	])

	def __init__(self, filename):
		self.instructions = []
		
		#get instruction data and register mapping
		r_map, instr_data = self.__pre()
		self.code = self.__read_in_advance()


	def __pre(self):
		#register mapping
		#make dictionary
		rmap_path = Path(__file__).parent / "data/reg_map.dat"	
		r_p = {}
		
		f = open(rmap_path,"r")
		#f = open("riscinterpreter/data/reg_map.dat", "r")
		#f = open("src/data/reg_map.dat","r")
		line = f.readline()

		#assign mapping 
		while line != "":
			elems = line.split(" ")
			r_p[elems[0]] = elems[1] 
			line = f.readline()

		f.close()
		#index for instr_data
		opcode = 0
		f3 = 1
		f7 = 2

		#order is [opcode, f3, f7]
		i_data = {}
		instr_path = Path(__file__).parent / "data/instr_data.dat"
		f = open(instr_path,"r")
		#f = open("riscinterpreter/data/instr_data.dat", "r")
		#f = open("src/data/instr_data.dat","r")
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

	def R_type(
			self, instr, rs1, 
			rs2, rd):

		if instr not in R_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			instr_data[instr][f7],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			instr_data[instr][f3],
			self.__reg_to_bin(rd),
			instr_data[instr][opcode]
		])

	def I_type(
			self, instr, rs1, 
			imm, rd):

		if instr not in I_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12),
			self.__reg_to_bin(rs1),
			instr_data[instr][f3],
			self.__reg_to_bin(rd),
			instr_data[instr][opcode]
		])

	def S_type(
			self, instr, rs1, 
			rs2, imm):

		if instr not in S_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),12)[::-1][5:12][::-1],
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			instr_data[instr][f3],
			self.__binary(int(imm),12)[::-1][0:5][::-1],
			instr_data[instr][opcode]
		])

	def SB_type(
			self, instr, rs1, 
			rs2, imm):

		if instr not in SB_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			"".join([
				self.__binary(int(imm),13)[::-1][12][::-1],
				self.__binary(int(imm),13)[::-1][5:11][::-1]
			]),
			self.__reg_to_bin(rs2),
			self.__reg_to_bin(rs1),
			instr_data[instr][f3],
			"".join([
				self.__binary(int(imm),13)[::-1][1:5][::-1],
				self.__binary(int(imm),13)[::-1][11][::-1]
			]),
			instr_data[instr][opcode]
		])


	def U_type(
			self, instr, 
			imm, rd):

		if instr not in U_instr:
			raise WrongInstructionType()
		opcode = 0;f3 = 1;f7 = 2
		return "".join([
			self.__binary(int(imm),32)[::-1][12:32][::-1],
			self.__reg_to_bin(rd),
			instr_data[instr][opcode]
		])

	def UJ_type(
			self, instr, 
			imm, rd):

		if instr not in UJ_instr:
			raise WrongInstructionType()

		opcode = 0;f3 = 1;f7 = 2
		return  "".join([
			"".join([
				self.__binary(int(imm),21)[::-1][20][::-1], self.__binary(int(imm),21)[::-1][1:11][::-1],
				self.__binary(int(imm),21)[::-1][11][::-1], self.__binary(int(imm),21)[::-1][12:20][::-1]
			]),		
			self.__reg_to_bin(rd),
			instr_data[instr][opcode]
		])



