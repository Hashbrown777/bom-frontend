from django.contrib import admin
from solo.admin import SingletonModelAdmin
from zooadapter.models import ZooAdapterConfig

admin.site.register(ZooAdapterConfig, SingletonModelAdmin)

