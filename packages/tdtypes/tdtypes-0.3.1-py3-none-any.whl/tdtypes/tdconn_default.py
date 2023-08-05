"Default Teradata connection functions"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2018, Paresh Adhia"

# A connection module requires:
# -----------------------------
# 1) DB API names to be imported
# 2) dbconnect() function that returns a raw database connection

from teradatasql import *

def dbconnect(tdconn=None):
	"returns a raw database connection"

	if tdconn is None:
		import os
		tdconn = os.environ.get('TDCONN', '{"host": "dbc", "user": "dbc", "password": "dbc"}')

	return connect(tdconn)
