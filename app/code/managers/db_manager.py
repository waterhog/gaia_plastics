# methods for interacting with database, using either WIFI or LTE
import pyodbc
from values_manager import get_database
from lte_manager import setup_sms, lte_insert_data

class DBManager:
	""" """

	def __init__(self, method):
		self.method = method
		self.database = get_database()

		# initialize to Non
		self.DRIVER = None
		self.TDS_VERSION = None
		self.connection = None
		# set up connection to database with pyodbc if using WIFI
		if self.method == "WIFI":
			self._open_connection()
		else:
			setup_sms()

	def update_table(self, data):
		if self.method == "WIFI":
			self._pyodbc_insert_to_table(self.connection, data)
			self.connection.commit()
		else:
			lte_insert_data(data)
		print("Sent data to table: " )
		print(data)

	def _open_connection(self):
		if self.method == "WIFI":
			self.DRIVER = '{FreeTDS}'
			self.TDS_VERSION = 8.0
			self.connection = pyodbc.connect('DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_VERSION={}'.format(self.DRIVER, self.database["server"], self.database["database"], self.database["username"], self.database["password"], self.TDS_VERSION))

	def _close_connection(self):
		if self.method == "WIFI":
			self.connection.close()
			self.connection = None

	def _commit_changes(self, connection):
		self.connection.commit()

	# TODO the print output of this is messy, clean it up, or learn to use a dictionary
	def _pyodbc_insert_to_table(self, connection, data):
		str = ""
		tmpstr = "?,"
		value_list = []
		cursor = self.connection.cursor()
		for i in range(len(data)):
			str = str + tmpstr
			value_list.append(data[i])
		sql_query = str[:-1]
		sql_query = "Insert Into " + self.database["table"] + " Values(" + sql_query + ")"
		cursor.execute(sql_query, value_list)
