import requests
class exception_handler:
	def get_index_field(self,message):
		url='http://feed.unbxdapi.com/getIndexFields?siteId='+message
		#print url
		response=requests.get(url)
		#print response.text
		return response.text