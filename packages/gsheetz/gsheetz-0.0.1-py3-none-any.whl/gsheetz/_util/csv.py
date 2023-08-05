import pandas as pd

def colnum_string(n):
	# Get column number string given a number for the column
	# 0 Indexed
	string = ""
	n+=1
	while n > 0:
		n, remainder = divmod(n - 1, 26)
		string = chr(65 + remainder) + string
	return string

# Return the name of a cell
def get_cell_name(sheetname,r,c):
	return get_range_name(sheetname,r,c,r,c)

# Return the range name for a range defined by 2 coordinates (0 indexed)
def get_range_name(sheetname,r1,c1,r2,c2):
	if r1 == r2 and c1 == c2:
		return f"{sheetname}!{colnum_string(c1)}{r1+1}"
	return f"{sheetname}!{colnum_string(c1)}{r1+1}:{colnum_string(c2)}{r2+1}"
	# r1, r2 inclusive
	# c1, c2 inclusive
