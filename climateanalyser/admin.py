from django.contrib import admin
from django import forms
from django.forms import ModelForm
from climateanalyser.models import Computation,DataFile,ComputationData
from forms import ComputationForm,ComputationDataForm,DataFileForm

class ComputationDataInline(admin.StackedInline):
   model = ComputationData
   form = ComputationDataForm

   class Media:
      js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js',
         'climateanalyser/js/jquery.cookie.min.js',
         'climateanalyser/js/computationdataform.js',)

class AdminComputationForm(ComputationForm):
   class Meta:
      fields = ['id', 'created_by', 'created_date', 'completed_date']

class ComputationAdmin(admin.ModelAdmin):
   inlines = [ComputationDataInline]
   form = AdminComputationForm
   list_display = ('id', 'created_by', 'created_date', 'completed_date')

class DataFileAdmin(admin.ModelAdmin):
   list_display = ['id','file_url','cached_file','last_modified']
   fields = ['file_url']

   def __init__(self, *args, **kwargs):
      super(DataFileAdmin, self).__init__(*args, **kwargs)
      # disable edit link (we only want to allow add/delete)
      self.list_display_links = (None, )

admin.site.register(Computation, ComputationAdmin)
admin.site.register(DataFile, DataFileAdmin)
