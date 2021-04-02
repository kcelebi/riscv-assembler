from project_convert import *
from convert import *

pc = ProjectConverter('tests/assembly')

ac = AssemblyConverter(output_type='r')

lines = ac.convert('tests/assembly/test2.s')

print(lines)
#TEST CASES
# 1. w/ or w/o filepath
# 2. incorrect filepath raises error