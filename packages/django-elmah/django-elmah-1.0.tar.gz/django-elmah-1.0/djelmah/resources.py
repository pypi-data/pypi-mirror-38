from datetime import datetime
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from models import DjelmahLog

class DjelmahLogResource(ModelResource):
    class Meta:
        resource_name = "logs"
        max_limit = 0
        limit = 0

        queryset = DjelmahLog.objects.all()
        filtering = {
            'host': {'exact'}
        }

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
