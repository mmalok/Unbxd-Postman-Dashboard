from model import *

def CreateTables():
    # Add all the tables needed to be created here
    #print "4"
    loginData.create_table(True)
    login_Admin_Data.create_table(True)