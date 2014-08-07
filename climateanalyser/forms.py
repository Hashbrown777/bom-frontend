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

class ComputationForm(ModelForm):
   created_by = forms.ModelChoiceField(queryset=User.objects.all(),
         widget=forms.HiddenInput())
   class Meta:
      model = Computation
      fields = ['calculation','created_by']
