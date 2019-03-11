from django.conf.urls import *

from . import views

urlpatterns = [
    url(r'^$', views.summarize, name='home'),
    url(r'^summarize/(?P<video_id>.*)\/*$', views.summarize, name="summary"),
]
