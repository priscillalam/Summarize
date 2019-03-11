from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
	url(r'^', include('app.urls')),
]
