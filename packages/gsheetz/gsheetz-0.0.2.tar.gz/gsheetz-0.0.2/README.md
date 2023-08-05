# GSheetz
GSheetz is a small package that I made while trying to connect to the google sheets API. It was really annoying so I made a few classes and functions to make it easier.

The easiest way to use it is through the `get_view` function and the `SheetView` class. This package is really for personal use so I'm not going to spend much time on documentation for now, but if the project expands I'll maybe do stuff to make it legible and stuff like that.

Here's some example usage:

```python
from gsheetz.views import SheetView

TOKEN = 'token.json' # Path of token file
SECRET = 'client_secret.json' # Path of client secret file
SCOPES = 'https://www.googleapis.com/auth/spreadsheets' # Scopes variable as defined by API
sheetID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms' # Sheet ID
sheetName = 'Class Data'

# SheetView is the default so you don't technically need to import it
view = SheetView.get_view(TOKEN,SECRET,SCOPES)
df = view.view_sheet(sheetID,sheetName)
# View the sheet - This loads the sheet,
# stores it in a pandas DataFrame at view.localdf,
# formats it (if you override the format_sheet method),
# sets view.current = sheetID and view.sheet = sheetName, and then returns the DataFrame
```

As you can see, the point of this package is to take care of the boiler-plate for you. If you'd like to interact with the API yourself, simply call `get_view(TOKEN,SECRET,SCOPES).api` to get access to the API object (`service.spreadsheets()`).

### Future Plans (in arbitrary order)
* Dynamically update the `localdf` attribute of `SheetView` objects instead of just 'refreshing' it.
* Add support for editing multiple ranges
* Eventually change the architecture for the connection module to use something besides `oath2client` (it's been deprecated)
* Add functionality to load a range instead of a whole sheet
* Write documentation

### Sources
* [Google Sheets API][sheets-api-homepage] - The docs for the API
* [Guide and Quickstart][API-quickstart] - I literally copy-pasted the python code from this and separated it into multiple functions. I tried figuring out how to use `google.auth` but figured it wasn't worth the extra time to parse through all the docs when the code is already written for me
* [Google Sheets API for Python Developers][sheets-for-py] - the docs that explain how to use the python methods

[shlex]: https://docs.python.org/3/library/shlex.html
[sheets-api-homepage]: https://developers.google.com/sheets/api/
[API-quickstart]: https://developers.google.com/sheets/api/guides/concepts
[sheets-for-py]: https://developers.google.com/api-client-library/python/apis/sheets/v4
