from django import forms
from django.forms import ModelForm
from climateanalyser.models import Computation

class ComputeForm(ModelForm):
   class Meta:
      model = Computation
      fields = ['data_file']
