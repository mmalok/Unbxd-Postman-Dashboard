from storedao import *
class services:
	def insert(self,username,password):
		#print("1")
		store_dao_object = store_dao()
		return store_dao_object.store_user(username,password)
	def check(self,email):
		#print("services-->email")
		store_dao_object = store_dao()
		return store_dao_object.check_user(email)
	def validate_user(self,email,password):
		#print("services-->validate_user")
		store_dao_object = store_dao()
		return store_dao_object.validate_user(email,password)

	def read_data(self,msg):
		print "services"
		store_dao_object=store_dao()
		return store_dao_object.get_readonly_data(msg)