
__all__ = ['nibbleForm']


def nibbleForm(x):
	fin_str = ""
	for i in range(0,len(x),4):
		fin_str += (x[i:i+4] + "\t")
	return fin_str[:-1]