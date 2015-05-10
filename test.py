from taskservices import *
print "1"
taskservice_obj=taskschservices()
response=taskservice_obj.status()
response=eval(response)
print response['status']
print response