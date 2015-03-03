from settings import *
class Mapping(dict):
    """
    Mapping

    provides '.' access to dictionary keys
    """
    def __init__(self, mapping, *args, **kwargs):
        """
        Create a new mapping. Filters the mapping argument
        to remove any elements that are already methods on the
        object.

        For example, Orders retains its `coupons` method, instead
        of being replaced by the dict describing the coupons endpoint
        """
        filter_args = {k: mapping[k] for k in mapping if k not in dir(self)}
        self.__dict__ = self
        dict.__init__(self, filter_args, *args, **kwargs)

    def __str__(self):
        """
        Display as a normal dict, but filter out underscored items first
        """
        return str({k: self.__dict__[k] for k in self.__dict__ if not k.startswith("_")})

    def __repr__(self):
        return "<%s at %s, %s>" % (type(self).__name__, hex(id(self)), str(self))


class ApiResource(Mapping):
    resource_name = ""  # The identifier which describes this resource in urls

    @classmethod
    def _create_object(cls, response, connection=None):
        if isinstance(response, list):
            return [cls._create_object(obj, connection) for obj in response]
        else:
            return cls(response, _connection=connection)

    @classmethod
    def _make_request(self, method, url, connection, data=None, params={}):
        return connection.make_request(method, url, data, params)

    @classmethod
    def get(cls, id, connection=None, **params):
        response = cls._make_request('GET', "%s/%s" % (cls.resource_name, id), connection, params=params)
        return cls._create_object(response, connection=connection)





class CreateableApiResource(ApiResource):
    @classmethod
    def create(cls, connection=None, **params):
        response = cls._make_request('POST', cls.resource_name, connection, data=params)
        return cls._create_object(response, connection=connection)




class ListableApiResource(ApiResource):
    @classmethod
    def all(cls, connection=None, **params):
        local_resource=cls.resource_name
        setting=settings()
        cls.resource_name=str(setting.all(cls.resource_name))
        response = cls._make_request('get', cls.resource_name, connection, params=params)
        cls.resource_name=local_resource
        return response

class UpdateableApiResource(ApiResource):
    @classmethod
    def update(cls, connection=None, **params):
        local_resource=cls.resource_name
        setting=settings()
        cls.resource_name=str(setting.update(cls.resource_name))
        response = cls._make_request('put', cls.resource_name,connection, params=params)
        cls.resource_name=local_resource
        return response



class DeleteableApiResource(ApiResource):
    @classmethod
    def delete(cls, connection=None, **params):
        local_resource=cls.resource_name
        setting=settings()
        cls.resource_name=str(setting.delete(cls.resource_name))
        response = cls._make_request('delete', cls.resource_name,connection, params=params)
        cls.resource_name=local_resource
        return response
