from django.conf.urls import url

from climateanalyser import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   #url(r'^login/$', views.login_user, name='login_user')
   url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name' : 'login.html' }),
   url(r'^logout/$', 'django.contrib.auth.views.logout', { 'template_name' : 'logout.html' }),
]
