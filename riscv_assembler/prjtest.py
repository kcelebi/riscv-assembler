from project_convert import *
from convert import *

#pc = ProjectConverter('tests/assembly')

ac = AssemblyConverter()

ac.setOutputType('p')
ac.setHex(True)

ac.convert('tests/assembly/test3.s')
#TEST CASES
# 1. w/ or w/o filepath
# 2. incorrect filepath raises error