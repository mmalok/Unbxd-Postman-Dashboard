from model import loginData

def CreateTables():
    # Add all the tables needed to be created here
    #print "4"
    loginData.create_table(True)