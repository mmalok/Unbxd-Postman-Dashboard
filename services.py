from storedao import *
class services:
	def insert(self,username,password):
		print("1")
		store_dao_object = store_dao()
		return store_dao_object.store_user(username,password)