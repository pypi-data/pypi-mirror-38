import pandas as pd
from gsheetz._util.csv import get_cell_name, get_range_name
from gsheetz.connection import connect_to_api,get_credentials

# Class for viewing spreadsheets, reading from them, and writing to them
# I suggest overriding the format_sheet method
class SheetView:

	# Takes an API object - i.e. the value of service.spreadsheets() - as input
	def __init__(self, api):
		self.api = api
		self.current = None
		self.sheet = None
		self.localdf = None

	def write(self, *values, **kwargs):
		axis = kwargs.pop('axis', 0)
		shift = kwargs.pop('shift',0)
		if kwargs:
			raise TypeError(f"write() got an unexpected keyword argument '{kwargs.keys()[0]}'")
		# Writes values to a line of cells. axis = 0 for writing to a row, axis = 1 for writing to a column
		# Values is list of values to enter into sheets
		# shift is amount of cells in line to skip before writing
		# Shortcut for write_row and write_col
		# Writes to row/column with the lowest row/col number that is completely empty
		# i.e. expands the localdf by 1 row or 1 column
		# Override this function if you'd like to write a convenience function
		if axis == 0:
			return self.write_row(self.last_index()+1,values,shift)
		else:
			return self.write_col(self.localdf.shape[1],values,shift)

	def last_index(self):
		# Returns the last index of the sheet
		return self.localdf.index[-1]

	def write_row(self, row, values, shift = 0):
		# Writes a single line
		# row is row number, 0 indexed
		# values is a list of values to enter into the sheets
		# shift is the amount of cells to skip before starting to write on the row
		# writes left to right
		return self.write_lines( get_cell_name(self.sheet,row,shift) , [[str(value) for value in values]] )

	def write_col(self, col, values, shift = 0):
		# Writes a single line
		# col is column number, 0 indexed
		# values is a list of values to enter into the sheets
		# shift is the amount of cells to skip before starting to write on the column
		# writes top to bottom
		return self.write_lines( get_cell_name(self.sheet,shift,col) , [[str(value)] for value in values] )

	def write_lines(self, range_name, values):
		# Writing
		# values is a list of lists, each list is a row
		# range_name is a range name string, in SHEET_NAME!A1:C2 format
		# A1 and C2 are placeholders for cell locations in A1 format
		# returns number of cells updated
		body = {
		    'values': values
		}
		result = self.api.values().update(
		    spreadsheetId=self.current, range=range_name,
		    valueInputOption='USER_ENTERED', body=body).execute()
		self.view_sheet(force_reload = True)
		return result.get('updatedCells')


	# View the dataframe of a sheet, or the current sheet if not specified
	# Should also eventually retrieve sheet metadata as well
	# Then check if sheetname is in the list of sheets
	def view_sheet(self,spreadsheetID = None, sheetname = "sheet1", force_reload = False):
		if spreadsheetID is None:
			if self.current is None:
				raise ValueError("Can't call view_sheet() without an ID if not currently viewing a sheet!")
			else:
				spreadsheetID = self.current
				sheetname = self.sheet

		if spreadsheetID == self.current and sheetname == self.sheet and force_reload is False:
			return self.localdf.copy()
		sheet = self._read_sheet(spreadsheetID,sheetname)
		self.localdf = self.format_sheet(sheet)
		self.current = spreadsheetID
		self.sheet = sheetname
		return self.localdf.copy()

	def format_sheet(self,df):
		# Method to override, telling how to format the sheet
		# Input is dataframe and output is formatted dataframe
		# Note that This class doesn't do anything to ensure that
		# the formatted sheet is in any way like the sheet before
		# formatting
		return df

	def range_string(self,sheetname,r1,c1,r2 = None,c2 = None):
		# Gets a string cooresponding to a zero-indexed coordinate section of a sheet
		if r2 is None:
			r2 = r1
		if c2 is None:
			c2 = c1
		return get_range_name(sheetname, r1,c1, r2,c2)

	def _read_sheet(self,spreadsheetID,sheetname):
		# Read a sheet from the api
		sheet_metadata = self.api.get(spreadsheetId=spreadsheetID).execute() # Get sheet
		sheets = sheet_metadata.get('sheets', []) # Get from dictionary object
		sheetnames = [sdict.get("properties", {}).get('title') for sdict in sheets]
		if sheetname not in sheetnames: # Check that the sheetname is in the google sheets document
			raise ValueError("sheetname parameter must be a valid sheetname!")
		# title = sheets[0].get("properties", {}).get("title", "Sheet1")
		# sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
		del sheet_metadata, sheets, sheetnames # Free up RAM before doing next API call
		result = self.api.values().get(
			spreadsheetId=spreadsheetID,
			range = sheetname,
			valueRenderOption='UNFORMATTED_VALUE').execute()
		# Read in the ledger
		values = result.get('values', [])
		return pd.DataFrame(values)

def get_view(token_path,secret_path,scopes,view_class = SheetView):
	# Creates a viewer
	creds = get_credentials(token_path,secret_path,scopes)
	sheets = connect_to_api(creds)
	return view_class(sheets)
