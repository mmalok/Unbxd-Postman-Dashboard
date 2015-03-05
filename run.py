import sys
from view import app

#execute some sql statement to create all the tables if not present, ignore otherwise
from dao import CreateTables
try:
	CreateTables()
except Exception as e :
	print e
	sys.exit()

app.run(debug=True)