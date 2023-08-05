"Default Teradata connection functions"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2018, Paresh Adhia"

# A connection module requires:
# -----------------------------
# 1) import all names from the DB API module
# 2) dbconn_args() function that optionally allows command line scripts to provide teradata authentication
# 3) dbconnect() function that returns a raw database connection

# 1)
from teradatasql import *

# 2)
def dbconn_args(parser):
	"add an argument to obtain authentication as a ODBC connection string"
	import os

	default_auth = os.environ.get('TDCONN', '{"host": "dbc", "user": "dbc", "password": "dbc"}')
	parser.add_argument("--tdconn", default=default_auth, help="Teradata connection JSON string")

# 3)
def dbconnect(args):
	"returns a raw database connection"
	return connect(args.tdconn)
