from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^feed/(?P<uuid>[a-z0-9\-]+)/$', views.detail, name='detail'),
]