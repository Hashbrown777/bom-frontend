from django.contrib import admin
from django import forms
from solo.admin import SingletonModelAdmin
from zooadapter.models import ZooAdapterConfig

class AdminZooAdapterConfigForm(forms.ModelForm):

   zoo_public_key = forms.CharField(widget=forms.Textarea)
   zoo_private_key = forms.CharField(widget=forms.Textarea)

   class Meta:
      model = ZooAdapterConfig

class ZooAdapterConfigAdmin(SingletonModelAdmin):
   form = AdminZooAdapterConfigForm

admin.site.register(ZooAdapterConfig, ZooAdapterConfigAdmin)

