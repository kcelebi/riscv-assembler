from pathlib import Path
from bitstring import BitArray
import math as m

__all__ = [
	'R_instr', 'I_instr', 'S_instr',
	'SB_instr', 'U_instr', 'UJ_instr','pseudo_instr',
	 'R', 'I', 'S', 'SB', 'U', 'UJ',
	 'Rp', 'Ip', 'Sp', 'SBp', 'Up', 'UJp']

class Instruction:
	def compute_instr(self, *args):
		raise NotImplementedError()

	def __call__(self, *args):
		return self.compute_instr(*args)

	def check_instr_valid(self, x, instr_set):
		assert x in instr_set, "{instr} is not the right instruction for this function.".format(instr = x)
		return x

class _R(Instruction):
	def __repr__(self):
		return "R instruction"

	def __str__(self):
		return "R instruction"

	def compute_instr(self, instr, rs1, rs2, rd):
		instr = super().check_instr_valid(instr, R_instr)
		opcode, f3, f7 = 0, 1, 2

		return "".join([
			instr_map[instr][f7],
			reg(rs2),
			reg(rs1),
			instr_map[instr][f3],
			reg(rd),
			instr_map[instr][opcode]
		])

class _I(Instruction):
	def __repr__(self):
		return "I instruction"

	def __str__(self):
		return "I instruction"

	def compute_instr(self, instr, rs1, imm, rd):
		instr = super().check_instr_valid(instr, I_instr)
		opcode, f3 = 0, 1

		return "".join([
			immediate(imm),
			reg(rs1),
			instr_map[instr][f3],
			reg(rd),
			instr_map[instr][opcode]
		])

	@staticmethod
	def immediate(imm):
		#return int(imm) - ((int(imm)>>12)<<12) # imm[11:0]
		return format(int(imm), '012b')

class _S(Instruction):
	def __repr__(self):
		return "S instruction"

	def __str__(self):
		return "S instruction"

	def compute_instr(self, instr, rs1, rs2, imm):
		instr = super().check_instr_valid(instr, S_instr)
		opcode, f3 = 0, 1

		return "".join([
			immediate(imm, 1),
			reg(rs2),
			reg(rs1),
			instr_map[instr][f3],
			immediate(imm, 2),
			instr_map[instr][opcode]
		])

	@staticmethod
	def immediate(imm, n):
		'''mod_imm = (int(imm) - ((int(imm) >> 12) << 12)) >> 5 # imm[11:5]
								mod_imm_2 = int(imm) - ((int(imm) >> 5) << 5) # imm[4:0]
						
								return mod_imm, mod_imm_2'''
		mod_imm = format(((1 << 13) - 1) & int(imm), '013b')
		if n == 1:
			return mod_imm[0] + mod_imm[12-10 : 12-4]
		return mod_imm[12-4 : 12 - 0] + mod_imm[1]


class _SB(Instruction):
	def __repr__(self):
		return "SB instruction"

	def __str__(self):
		return "SB instruction"

	def compute_instr(self, instr, rs1, rs2, imm):
		instr = super().check_instr_valid(instr, SB_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm, mod_imm_2 = immediate(imm)

		return "".join([
			...
		])

	@staticmethod
	def immediate(imm):
		mod_imm = (int(imm) - ((int(imm) >> 12) << 12)) >> 6 # imm[12]
		mod_imm += (int(imm) - ((int(imm) >> 11) >> 11)) >> 5 # imm[12|10:5]
		
		mod_imm_2 = (int(imm) - ((int(imm) >> 5) << 5)) # imm[4:1]
		mod_imm_2 += (int(imm) - ((int(imm) >> 11) << 11)) >> 10 # imm[4:1|11]

		return mod_imm, mod_imm_2

class _U(Instruction):
	def __repr__(self):
		return "U instruction"

	def __str__(self):
		return "U instruction"

	def compute_instr(self, instr, imm, rd):
		instr = super().check_instr_valid(instr, U_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = immediate(imm)

		return "".join([
			...
		])

	@staticmethod
	def immediate(imm):
		return (int(imm) >> 12)

class _UJ(Instruction):
	def __repr__(self):
		return "UJ instruction"

	def __str__(self):
		return "UJ instruction"

	def compute_instr(self, instr, imm, rd):
		instr = super().check_instr_valid(instr, UJ_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = immediate(imm)
		
		return "".join([
			...
		])

	@staticmethod
	def immediate(imm):
		mod_imm = ((int(imm) - ((int(imm) >> 20) << 20)) >> 19) << 19 # imm[20]
		mod_imm += (int(imm) - ((int(imm) >> 10) << 10)) >> 1 # imm[20|10:1]
		mod_imm += (int(imm) - ((int(imm) >> 11) << 11)) >> 10 # imm[20|10:1|11]
		mod_imm += (int(imm) - ((int(imm) >> 19) << 19)) >> 12 # imm[20|10:1|11|19:12]

		return mod_imm

class InstructionParser:
	def organize(self, *args):
		raise NotImplementedError()

	def __call__(self, *args):
		return self.organize(*args)

class _R_parse(InstructionParser):
	def organize(self, tokens):
		instr, rs1, rs2, rd = tokens[0], reg_map[tokens[2]], reg_map[tokens[3]], reg_map[tokens[1]]
		return R(instr, rs1, rs2, rd)

class _I_parse(InstructionParser):
	def organize(self, tokens):
		instr, rs1, imm, rd = tokens[0], None, None, None
		if instr == "jalr":
			if len(tokens) == 4:
				rs1, imm, rd = reg_map[tokens[2]], JUMP(tokens[3]), reg_map[tokens[1]]
			else:
				rs1, imm, rd = reg_map[tokens[1]], 0, reg_map["x1"]
		elif instr == "lw":
			rs1, imm, rd = reg_map[tokens[3]], tokens[2], reg_map[tokens[1]]
		else:
			rs1, imm, rd = reg_map[tokens[2]], tokens[3], reg_map[tokens[1]]

		return I(instr, rs1, imm, rd)

class _S_parse(InstructionParser):
	def organize(self, tokens):
		instr, rs1, rs2, imm = tokens[0], reg_map[tokens[3]], reg_map[tokens[1]], tokens[2]
		return S(instr, rs1, rs2, imm)

class _SB_parse(InstructionParser):
	def organize(self, tokens):
		instr, rs1, rs2, imm = tokens[0], reg_map[tokens[1]], reg_map[tokens[2]], JUMP(tokens[3])
		return SB(instr, rs1, rs2, imm)

class _U_parse(InstructionParser):
	def organize(self, tokens):
		instr, imm, rd = tokens[0], tokens[1], reg_map[tokens[2]]
		return U(instr, imm, rd)

class _UJ_parse(InstructionParser):
	def organize(self, tokens):
		instr, imm, rd = tokens[0], None, None
		if len(tokens) == 3:
			imm, rd = JUMP(tokens[2]), reg_map[tokens[1]]
		else:
			imm, rd = JUMP(tokens[1]), reg_map["x1"]

		return UJ(instr, imm, rd)

class _Pseudo_parse(InstructionParser):
	def organize(self, tokens):
		instr = tokens[0]
		if instr == 'nop':
			rs1, imm, rd = reg_map["x0"], 0, reg_map["x0"]
			return I("addi", rs1, imm, rd)
		elif instr == "mv":
			rs1, imm, rd = reg_map[tokens[2]], 0, reg_map[tokens[1]]
			return I("addi", rs1, imm, rd)
		elif instr == "not":
			rs1, imm, rd = reg_map[tokens[2]], -1, reg_map[tokens[1]]
			return I("xori", rs1, imm, rd)
		elif instr == "neg":
			rs1, rs2, rd = reg_map["x0"], reg_map[tokens[2]], reg_map[tokens[1]]
			return R("sub", rs1, rs2, rd)

		return BadInstructionError()

def reg(x):
	#return __binary(int(x[1:]), 5)
	return format(int(imm[1:]), '05b')

def __binary(x, size):
	byte_num = m.ceil(size/8)
	b_num = x.to_bytes(byte_num, byteorder = 'big', signed = True)

	fin_bin = ''.join(format(byte, '08b') for byte in b_num)
	
	if byte_num*8 == size:
		return fin_bin
	return fin_bin[len(fin_bin)-size:len(fin_bin)]

def register_map():
	path = Path(__file__).parent / "data/reg_map.dat"
	rmap = {}

	f = open(path, "r")
	line = f.readline()
	while line != "":
		e = line.split()
		rmap[e[0]] = e[1] 
		line = f.readline()
	f.close()

	return rmap

def instruction_map():
	path = Path(__file__).parent / "data/instr_data.dat"
	imap = {}

	f = open(path, "r")
	line = f.readline()
	while line != "":
		e = line.split()
		imap[e[0]] = e[1:]
		line = f.readline()
	f.close()

	return imap


R, I, S, SB, U, UJ = _R(), _I(), _S(), _SB(), _U(), _UJ()
Rp, Ip, Sp, SBp, Up, UJp = _R_parse(), _I_parse(), _S_parse(), _SB_parse(), _U_parse(), _UJ_parse()
reg_map, instr_map = register_map(), instruction_map()


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

'''get_intr_set_map = {}
for instr_set in [R_instr, I_instr, S_instr, SB_instr, U_instr, UJ_instr, pseudo_instr]:
	for instr in instr_set:
		get_instr_set_map[instr] = '''