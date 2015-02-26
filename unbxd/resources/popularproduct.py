from .base import *

class popularproduct(ListableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'PopularProductField.do'

    