import requests
class taskschdao:
	def status(self):
		print("3")
		try:
			req=requests.get("http://sol-serv-a-d1-1.cloudapp.net:8001/ping")
			print req
			print "4"
			print req.text
			return req.text
		except:
			return '{"status":"connection refused"}'
	def add_task(self,msg):
		print("3")
		try:
			msg=msg.split("#")
			time=msg[4].split(":")
			url='http://sol-serv-a-d1-1.cloudapp.net:8001/addTask?taskData={"cmd":"'+str(msg[0])+'","name":"'+str(msg[1])+'","week":'+str(msg[2])+',"day":'+str(msg[3])+',"second":0,"minute":'+str(time[1])+',"hour":'+str(time[0])+',"r":'+str(msg[5])+'}'
			print url
			req=requests.get(url)
			print req.text
			return req.text
		except:
			return '{"status":"connection refused"}'
	def task_manager(self):
		try:
			req=requests.get("http://sol-serv-a-d1-1.cloudapp.net:8000/ping?name=manager")
			return req.text
		except:
			return '{"status":"connection refused"}'
	def task_all(self):
		try:
			req=requests.get("http://sol-serv-a-d1-1.cloudapp.net:8000/ping?name=all")
			return req.text
		except:
			return '{"status":"connection refused"}'
	def running_task_all(self):
		try:
			req=requests.get("http://sol-serv-a-d1-1.cloudapp.net:8000/tasks?owner=all")
			print req.text
			return req.text
		except:
			return '{"status":"connection refused"}'
	def specific_task(self,name):
		try:
			url='http://sol-serv-a-d1-1.cloudapp.net:8000/ping?name='+name
			print url
			req=requests.get(url)
			return req.text
		except:
			return '{"status":"connection refused"}'		
	def running_specific_task(self,name):
		try:
			url='http://sol-serv-a-d1-1.cloudapp.net:8000/tasks?owner='+name
			print url
			req=requests.get(url)
			return req.text
		except:
			return '{"status":"connection refused"}'		