from django.conf.urls import url

from auth import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name' : 'login.html' }),
   url(r'^logout/$', 'django.contrib.auth.views.logout', { 'template_name' : 'auth/logout.html' }),
   url(r'^register/$', views.register)
]
