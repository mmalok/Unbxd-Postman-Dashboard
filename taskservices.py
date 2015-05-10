from taskschdao import *
class taskschservices:
	def status(self):
		#print("2")
		store_dao_object = taskschdao()
		return store_dao_object.status()
	def add_task(self,msg):
		print("2")
		store_dao_object = taskschdao()
		return store_dao_object.add_task(msg)