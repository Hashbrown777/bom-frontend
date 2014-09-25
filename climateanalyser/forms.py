from django.forms import ModelForm
from django import forms
from models import Computation,DataFile,ComputationData
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User 
from fields import VariablesMultiField

class DataFileForm(ModelForm):
   class Meta:
      model = DataFile
      fields = ['file_url']

class ComputationDataForm(ModelForm):
   variables = VariablesMultiField()

   class Meta:
      model = ComputationData
      fields = ['datafile', 'variables','computation']

   class Media:
         js = ('climateanalyser/js/jquery.cookie.min.js',
         'climateanalyser/js/computationdataform.js',)

   def __init__(self, *arg, **kwarg):
      super(ComputationDataForm, self).__init__(*arg, **kwarg)
      #don't allow empty fields
      self.empty_permitted = False

class ComputationForm(ModelForm):
   created_by = forms.ModelChoiceField(queryset=User.objects.all(),
         widget=forms.HiddenInput())

   class Meta:
      model = Computation
      fields = ['calculation','created_by']

   def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request',None)
      super(ComputationForm,self).__init__(*args, **kwargs)

   def clean(self):
      cleaned_data = super(ComputationForm, self).clean()

      data_count = int(self.request.POST.get('computationdata_set-TOTAL_FORMS'))

      calculation = cleaned_data.get('calculation')

      if data_count < calculation.min_datafiles or \
         data_count > calculation.max_datafiles:
         raise forms.ValidationError(
               'Invalid number of datafiles for selected calculation.')

      return cleaned_data
