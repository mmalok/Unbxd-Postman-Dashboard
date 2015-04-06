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
	def validate_admin(self,email,password):
		#print("services-->validate_user")
		store_dao_object = store_dao()
		return store_dao_object.validate_admin(email,password)
	def user_data(self):
		store_dao_object=store_dao()
		return store_dao_object.get_user_data()
	def delete_user(self,username):
		store_dao_object=store_dao()
		return store_dao_object.delete_user(username)
	def update_user(self,username,read,write,delete):
		store_dao_object=store_dao()
		return store_dao_object.update_user(username,read,write,delete)
	def session_permission(self,username):
		store_dao_object=store_dao()
		return store_dao_object.session_permission(username)
	def get_internal_sitename(self,company):
		store_dao_object=store_dao()
		return store_dao_object.get_internal_sitename(company)
	def send_autosuggest_data(self,site_internal_name):
		store_dao_object=store_dao()
		return store_dao_object.send_autosuggest_data(site_internal_name)