from django.conf.urls import url

urlpatterns = [
   url(r'^admin/zooadapter/zoodashboard/$',
         'zooadapter.admin_views.zoo_dashboard'),
]
