from gsheetz.views.view import SheetView
import mr_clean as mrc
import pandas as pd

class BasicView(SheetView):

	# header is the header row of the sheet, 0 indexed, header = None means no header
	def __init__(self,api, header = 0):
		if header < 0:
			raise ValueError("Can't have a negative value for header row! Set to 'None' to indicate no headers")
		super(BasicView,self).__init__(api)
		self.header = header

	def format_sheet(self, df):
		if self.header is not None: # If there's a header row
			df.columns = df.iloc[self.header,:] # sets the colnames to the last row of the header
			df = df.drop(range(self.header+1),axis = 0)
		df.columns.name = None # Removing name from column
		df = df.replace(r'^\s+$', pd.np.nan,regex=True) # Removing whitespace-only cells
		df = df.replace('',pd.np.nan) # removing empty string cells
		df.fillna(value=pd.np.nan, inplace=True) # Empty cells should by a NaN
		df = mrc.clean(df,debug = False) # Cleaning
		return df
