import json
class response_handler:
	def addPopular(self,message):
		print("addPopular")
	 	response_text_json=json.loads(message)
		#print str(asd['popularProductFields'][0])
		#print(len(response_text_json['popularProductFields']))
		if (str(response_text_json['status'])== 'Success'):
			print response_text_json['status']
			return (response_text_json['status'])
		else:
			return response_text_json['errors'][0]['message']
	def true_check(self,message):
		true_count=0
		response_text_json=json.loads(message)
		try:
			for val in response_text_json['popularProductFields']:
				print val['required']
				if str(val['required'])=="True":
					true_count=true_count+1

			return true_count
		except:
			return true_count
	def delPopular(self,message):
		print "delPopular"
		response_text_json=json.loads(message)
		#print str(asd['popularProductFields'][0])
		#print(len(response_text_json['popularProductFields']))
		if (str(response_text_json['status'])== 'Success'):
			print response_text_json['status']
			return (response_text_json['status'])
		else:
			return response_text_json['errors'][0]['message']