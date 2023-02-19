__all__ = [
	'R_instr', 'I_instr', 'S_instr',
	'SB_instr', 'U_instr', 'UJ_instr',
	'pseudo_instr', 'R', 'I', 'S', 'SB', 'U', 'UJ']

class Instruction:
	def compute_instr(self, *args):
		raise NotImplementedError()

	def __call__(self, *args):
		return self.compute_instr(*args)

	@staticmethod
	def __check_instr_valid(x, instr_set):
		assert x in instr_set, "{instr} is not the right instruction for this function.".format(instr = x)
		return x

class _R(Instruction):
	def compute_instr(self, instr, rs1, rs2, rd):
		instr = __check_instr_valid(instr, R_instr)
		opcode, f3, f7 = 0, 1, 2

		return "".join([
			...
		])

class _I(Instruction):
	def compute_instr(self, instr, rs1, imm, rd):
		instr = __check_instr_valid(instr, I_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = int(imm) - ((int(imm)>>12)<<12) # imm[11:0]

		return "".join([
			...
		])

class _S(Instruction):
	def compute_instr(self, instr, rs1, rs2, imm):
		instr = __check_instr_valid(instr, S_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = (int(imm) - ((int(imm) >> 12) << 12)) >> 5 # imm[11:5]
		mod_imm_2 = int(imm) - ((int(imm) >> 5) << 5) # imm[4:0]

		return "".join([
			...
		])

class _SB(Instruction):
	def compute_instr(self, instr, rs1, rs2, imm):
		instr = __check_instr_valid(instr, SB_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = (int(imm) - ((int(imm) >> 12) << 12)) >> 6 # imm[12]
		mod_imm += (int(imm) - ((int(imm) >> 11) >> 11)) >> 5 # imm[12|10:5]
		mod_imm_2 = (int(imm) - ((int(imm) >> 5) << 5)) # imm[4:1]
		mod_imm_2 += (int(imm) - ((int(imm) >> 11) << 11)) >> 10 # imm[4:1|11]

		return "".join([
			...
		])

class _U(Instruction):
	def compute_instr(self, instr, imm, rd):
		instr = __check_instr_valid(instr, U_instr)
		opcode, f3, f7 = 0, 1, 2
		mod_imm = (int(imm) >> 12)

		return "".join([
			...
		])

class _UJ(Instruction):
	def compute_instr(self, instr, imm, rd):
		instr = __check_instr_valid(instr, UJ_instr)
		opcode, f3, f7 = 0, 1, 2

		mod_imm = ((int(imm) - ((int(imm) >> 20) << 20)) >> 19) << 19 # imm[20]
		mod_imm += (int(imm) - ((int(imm) >> 10) << 10)) >> 1 # imm[20|10:1]
		mod_imm += (int(imm) - ((int(imm) >> 11) << 11)) >> 10 # imm[20|10:1|11]
		mod_imm += (int(imm) - ((int(imm) >> 19) << 19)) >> 12 # imm[20|10:1|11|19:12]
		
		return "".join([
			...
		])


R, I, S, SB, U, UJ = _R(), _I(), _S(), _SB(), _U(), _UJ()

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