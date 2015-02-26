class data_handler:
	def all_unbxd_suggestion(self,message):
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		return json_data
	def get_all_infield(self,message):
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		return json_data
	def all_popular_product(self,message):
		json_data='{"siteDetail":{"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0}}'
		return json_data
	def add_unbxd_suggestion(self,message,fields):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"keywordSuggestion": {"name": "'+fields+'","fields": ["'+fields+'"]}}'
		return json_data
	def add_popular_product(self,message,fields,conditions):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":null},"popularProductField": {"fieldName": "'+fields+'","required": '+conditions+'}}'
		return json_data
	def add_in_field(self,message,fields):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"fieldName": "'+fields+'"}}'
		return json_data
	def delete_unbxd_suggestion(self,message,fields):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"keywordSuggestion": {"name": "'+fields+'"}}'
		return json_data
	def delete_in_field(self,message,fields):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":0},"fieldName": "'+fields+'"}}'
		return json_data
	def delete_popular_product(self,message,fields):
		json_data='{"siteDetail": {"siteId":'+message+',"iSiteName":null,"siteName":null,"subscribers":null,"userId":null},"popularProductField": {"fieldName": "'+fields+'"}}'
		return json_data
