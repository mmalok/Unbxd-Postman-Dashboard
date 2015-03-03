class settings:
	def update(self,resource):
		if resource=="InFields.do":
			resource="InFieldData.do"
		return("add"+resource)


	def delete(self,resource):
		if resource=="InFields.do":
			resource="InFieldData.do"
		return("delete"+resource)

	def all(self,resource):
		if resource=="PopularProductField.do":
			resource="PopularProductFields.do"
		return("getAll"+resource)