from dao.model import *
class store_dao:	
	def store_user(self,username,password):
		#print "2"
		all_data=[]
		#print password
		commit=loginData.insert(username=username,Password=password)
		commit.execute()
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
     
	def get_readonly_data(self,msg):
		print "storedao"
		data=""
		for record in site_request.select():
			site_id=str(record.site_id)
			site_name=str(record.site_name)
			data=data+site_id+"_"+site_name+" "
			#data.append(final_data)
		return data