"Teradata connection functions for use with the original teradata module"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2018, Paresh Adhia"

from teradata.api import *

def dbconnect(tdconn=None):
	"returns raw database connection"
	from teradata.tdodbc import connect

	if tdconn is None:
		import os
		tdconn = os.environ.get('TDCONN')

	return connect(driver='Teradata', **{k:v for k, v in [a.split('=') for a in tdconn.split(';')]})
