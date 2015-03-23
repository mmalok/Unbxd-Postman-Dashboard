import peewee as pw
import sys
from config import *

#data = SqliteDatabase('database.db')
mysql = pw.MySQLDatabase(Database["Name"], host=Database["Host"], \
        user=Database["User"], passwd=Database["Password"],threadlocals=True)
read_mysql= pw.MySQLDatabase(readonly_database["Name"], host=readonly_database["Host"], \
        user=readonly_database["User"], passwd=readonly_database["Password"],threadlocals=True)
#print mysql
admin_mysql=pw.MySQLDatabase(admin_Database["Name"], host=admin_Database["Host"], \
        user=admin_Database["User"], passwd=admin_Database["Password"],threadlocals=True)


def mysql_connect():
    try:
    	mysql.connect()
    except Exception as e:
    	print e
    	sys.exit()
def mysql_close():
    mysql.close()

def read_mysql_connect():
    try:
        read_mysql.connect()
    except Exception as e:
        print e
        sys.exit()
def read_mysql_close():
    mysql.close()



class MySQLModel(pw.Model):
    class Meta:
        database = mysql
        


class loginData(MySQLModel):
    #print "3"
    id = pw.PrimaryKeyField()
    username=pw.CharField()
    Password=pw.CharField()
    permissions_read=pw.BooleanField(default=False)
    permissions_write=pw.BooleanField(default=False)
    permissions_delete=pw.BooleanField(default=False)
class site_request(MySQLModel):
    class Meta:
        database=read_mysql
    #print "3"
    site_id = pw.PrimaryKeyField()
    site_name=pw.CharField()
class login_Admin_Data(MySQLModel):
    #print "3"
    class Meta:
        database=admin_mysql
    id = pw.PrimaryKeyField()
    username=pw.CharField()
    Password=pw.CharField()

   