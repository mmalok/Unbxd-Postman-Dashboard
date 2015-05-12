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
	def task_manager(self):
		print "services"
		store_dao_object = taskschdao()
		return store_dao_object.task_manager()
	def task_all(self):
		print "services"
		store_dao_object = taskschdao()
		return store_dao_object.task_all()
	def running_task_all(self):
		print "services"
		store_dao_object = taskschdao()
		return store_dao_object.running_task_all()
	def specific_task(self,name):
		print "services"
		store_dao_object = taskschdao()
		return store_dao_object.specific_task(name)
	def running_specific_task(self,name):
		print "services"
		store_dao_object = taskschdao()
		return store_dao_object.running_specific_task(name)