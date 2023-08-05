from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def connect_to_api(credentials):
	"""
	Returns a sheets API service object given a valid credentials object
	"""
	service = build('sheets', 'v4', http=credentials.authorize(Http()))
	return service.spreadsheets()

def get_credentials(token,secret,scopes):
	"""
	Gets credentials object given token file name,
	secret file name, and scopes list/string

	token: path or path-like representing the path of a
	file with token information
	secret: path or path-like representing the path of a
	file with the client secret and related information
	scopes: list/string for scopes
	"""
	# Try to get an existing token
	store = file.Storage( token )
	creds = store.get() # Get stored credentials

	# There's no token!
	if not creds or creds.invalid:
		# Create Flow object
	    flow = client.flow_from_clientsecrets(secret, scopes)

		# Get credentials
	    creds = tools.run_flow(flow, store)
	return creds
