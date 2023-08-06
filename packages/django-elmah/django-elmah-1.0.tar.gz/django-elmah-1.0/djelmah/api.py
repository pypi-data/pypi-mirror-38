from django.conf.urls import include, url
from tastypie.api import Api
from . import resources

# api resources
api = Api(api_name='v1')
api.register(resources.DjelmahLogResource())

urlpatterns = [
    url(r'^', include(api.urls)),
]
