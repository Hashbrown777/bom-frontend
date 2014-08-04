from django.conf.urls import url

from climateanalyser import views

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^compute/$', views.compute, name='compute'),
   url(r'^computations/$', views.computations, name='computations'),
   url(r'^computation$', views.computation, name='computation'),
   url(r'^load_cache$', views.load_cache, name='load_cache'),
]
