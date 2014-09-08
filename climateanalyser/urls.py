from django.conf.urls import url
from climateanalyser import views
from climateanalyser import ajax

urlpatterns = [
   url(r'^$', views.index, name='index'),
   url(r'^datafiles/$', views.datafiles, name='datafiles'),
   url(r'^create_datafile/$', views.create_datafile, name='create_datafile'),
   url(r'^create_computation/$', views.create_computation,
         name='create_computation'),
   url(r'^computations/$', views.computations, name='computations'),
   url(r'^computation$', views.computation, name='computation'),
   url(r'^load_cache$', views.load_cache, name='load_cache'),
   url(r'^load_datafile_metadata$', ajax.load_datafile_metadata,
         name='load_datafile_metadata'),
]
