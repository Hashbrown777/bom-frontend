from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bom.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^climateanalyser/', include('climateanalyser.urls')),
    url(r'^$', include('climateanalyser.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
