from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms
from models import ComputationData
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

class DataFileForm(ModelForm):
   class Meta:
      model = DataFile
      fields = ['file_url']

class ComputationDataForm(ModelForm):
   class Meta:
      model = ComputationData
      fields = ['datafile', 'variables']

class ComputationForm(ModelForm):
   class Meta:
      model = Computation
      fields = ['calculation']
