from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms
from fields import DataFilesField

class ComputationForm(ModelForm):
   data_files = DataFilesField()
   class Meta:
      model=Computation
      fields = ['calculation']

   def save(self):

      user = self.instance.user

      computation = Computation(
            created_by = user,
            calculation = self.cleaned_data['calculation'])

      computation.save()

      for data_file in self.cleaned_data['data_files']:
         computation.datafiles.create(file_url=data_file)

