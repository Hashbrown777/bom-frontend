from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms
from models import ComputationData
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.contrib.auth.models import User 
from django.http import HttpResponse
from fields import VariablesMultiField
import json


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
