from project_convert import *
from convert import *

#pc = ProjectConverter('tests/assembly')

pc = ProjectConverter(root = 'tests/assembly/prjtest1')

pc.setOutputType('r')
pc.setHex(True)

res = pc.convert()

print("\n".join(["{}: {}".format(p, len(res[p])) for p in res.keys()]))
print(pc.getFailedConvert())



#TEST CASES
# 1. w/ or w/o filepath
# 2. incorrect filepath raises error