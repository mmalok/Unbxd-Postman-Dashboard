
'''
import requests
import json
class handler:
	def allsuggestion(self,message):
		url="http://beta.feed.unbxdapi.com/autosuggest/getAllUnbxdSuggestion.do"
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		request = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		return str(request.text)
	def infield(self,message):
		url="http://beta.feed.unbxdapi.com/autosuggest/getAllInFields.do"
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		request = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		return str(request.text)
	def get_popular_product(self,message):
		url="http://feed.unbxdapi.com/autosuggest/getAllPopularProductFields.do"
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		request = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		return str(request.text)
	def add_suggestion(self,message,fields):
		url="http://beta.feed.unbxdapi.com/autosuggest/addUnbxdSuggestion.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"keywordSuggestion": {"name": "'+fields+'","fields": ["'+fields+'"]}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)
	def delete_suggestion(self,message,fields):
		url="http://beta.feed.unbxdapi.com/autosuggest/deleteUnbxdSuggestion.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"keywordSuggestion": {"name": "'+fields+'"}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)
	def add_popular(self,message,fields,conditions):
		url="http://beta.feed.unbxdapi.com/autosuggest/addPopularProductField.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":null},"popularProductField": {"fieldName": "'+fields+'","required": '+conditions+'}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)
	def delete_popular(self,message,fields):
		url="http://beta.feed.unbxdapi.com/autosuggest/deletePopularProductField.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":null},"popularProductField": {"fieldName": "'+fields+'"}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)
	def add_infield(self,message,fields):
		url="http://beta.feed.unbxdapi.com/autosuggest/addInFieldData.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"fieldName": "'+fields+'"}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)
	def delete_infield(self,message,fields):
		url="http://beta.feed.unbxdapi.com/autosuggest/deleteInFieldData.do"
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"fieldName": "'+fields+'"}}'
		print json_data
		response = requests.post(url, data=json_data)
		#response_json=json.loads(request.text)
		#json_dict= dict([(str(k), str(v)) for k, v in response_json.items()])
		print response.text
		return str(response.text)


'''
	
