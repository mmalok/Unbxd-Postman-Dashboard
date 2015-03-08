from dao.model import loginData
class store_dao:	
	def store_user(self,username,password):
		#print "2"
		all_data=[]
		#print password
		commit=loginData.insert(username=username,Password=password)
		commmit.execute()
		'''for record in data.select():
			msg=str(record.msg)
			all_data.append(msg)'''
		return "all_data"
	def check_user(self,email):
		#print "checkuser-->storedao"
		for record in loginData.select():
			msg=str(record.username)
			if(msg==email):
				return "already present"
		return "new user"
	def validate_user(self,email,password):
		#print "checkuser-->storedao"
		for record in loginData.select():
			msg=str(record.username)
			if(msg==email):
				if(password==(str(record.Password))):
					return "valid"
		return "invalid"
                
