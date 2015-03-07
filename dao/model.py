import peewee as pw
import sys
from config import Database

#data = SqliteDatabase('database.db')
mysql = pw.MySQLDatabase(Database["Name"], host=Database["Host"], \
        user=Database["User"], passwd=Database["Password"],threadlocals=True)
print mysql


def mysql_connect():
    try:
    	mysql.connect()
    except Exception as e:
    	print e
    	sys.exit()
def mysql_close():
    mysql.close()



class MySQLModel(pw.Model):
    class Meta:
        database = mysql

class loginData(MySQLModel):
    #print "3"
    id = pw.PrimaryKeyField()
    username=pw.CharField()
    Password=pw.CharField()