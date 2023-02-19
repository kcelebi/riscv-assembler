__all__ = [
	'R_instr', 'I_instr', 'S_instr',
	'SB_instr', 'U_instr', 'UJ_instr',
	'pseudo_instr', 'R', 'I', 'S', 'SB', 'U', 'UJ']

class Instruction:
	def compute_instr(self, *args):
		raise NotImplementedError()

	def __call__(self):
		...

class _R(Instruction):
	def compute_instr(self, _):
		...

class _I(Instruction):
	def compute_instr(self, _):
		...

class _S(Instruction):
	def compute_instr(self, _):
		...

class _SB(Instruction):
	def compute_instr(self, _):
		...

class _U(Instruction):
	def compute_instr(self, _):
		...

class _UJ(Instruction):
	def compute_instr(self, _):
		...


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