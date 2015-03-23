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
	def validate_admin(self,email,password):
		#print "checkuser-->storedao"
		for record in login_Admin_Data.select():
			msg=str(record.username)
			if(msg==email):
				if(password==(str(record.Password))):
					return "valid"
		return "invalid"
	def get_user_data(self):
		string=""
		outer=[]
		for record in loginData.select():
			msg=str(record.username)
			password=str(record.Password)
			read=str(record.permissions_read)
			write=str(record.permissions_write)
			delete=str(record.permissions_delete)
			inner=[]
			inner=[msg,password,read,write,delete]
			outer.append(inner)
		print outer
		return outer
	def delete_user(self,username):
		query = loginData.delete().where(loginData.username == username)
		query.execute()
		return "done"
	def update_user(self,name,read,write,delete):
		if(read=="False"):
			read=0
		if(write=="False"):
			write=0
		if(delete=="False"):
			delete=0
		query=loginData.update(permissions_read= read,permissions_write=write,permissions_delete=delete).where(loginData.username==name);
		query=query.execute()
		print (query)
		return "done"