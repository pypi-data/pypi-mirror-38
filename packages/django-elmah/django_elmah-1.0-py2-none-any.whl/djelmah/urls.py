from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logs/$', views.log_index),
    url(r'^logs/(?P<log_id>\d+)$', views.log_detail),
    url(r'^logs/delete$', views.delete_log),
    url(r'^logs/test$', views.log_test),
    url(r'^keys/$', views.api_keys),
    url(r'^keys/create$', views.create_api_key),
    url(r'^keys/revoke$', views.revoke_api_key),
]
