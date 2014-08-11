from django.contrib import admin
from django.forms import ModelForm
from climateanalyser.models import *
from forms import *
from solo.admin import SingletonModelAdmin
from climateanalyser.models import ClimateAnalyserConfig

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

class AdminDataFileForm(DataFileForm):
   class Media:
      # css to hide save buttons (should only show on edit form)
      css = { 'all' : ('climateanalyser/css/admindatafileform.css',) }

class DataFileAdmin(admin.ModelAdmin):
   list_display = ['id','file_url','cached_file','last_modified']

   def get_form(self, request, obj=None, **kwargs):
      if obj: # edit form
         # make edit form a read-only 'profile' page
         self.form = AdminDataFileForm
         self.form.fields = ['file_url', 'last_modified', 'cached_file', 'metadata']
         self.readonly_fields = ('file_url', 'last_modified', 'cached_file',
               'metadata')
      else: # add form
         self.form = DataFileForm
         self.form.fields = ['file_url']
         self.readonly_fields = []
         # don't hide save buttons on add form
         self.form.Media = None
      return super(DataFileAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Computation, ComputationAdmin)
admin.site.register(DataFile, DataFileAdmin)
admin.site.register(ClimateAnalyserConfig, SingletonModelAdmin)
