from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms
from fields import DataFilesField

class ComputationForm(ModelForm):
   datafiles = DataFilesField()
   class Meta:
      model = Computation
      fields = ['calculation','datafiles']

   def save(self,user=False,commit=True):

      if not self.instance.id:
         self.instance = Computation(created_by = user,
              calculation = self.cleaned_data['calculation'])
         self.instance.save()
         self.save_m2m()

      return self.instance

   def save_m2m(self):
      #Save DataFiles

      #remove relationships with existing datafiles but don't delete them!
      self.instance.datafiles.clear()

      for file_url in self.cleaned_data['datafiles']:
         
         datafile = DataFile.objects.filter(file_url=file_url)
   
         if datafile:
            #add existing datafile instance
            self.instance.datafiles.add(datafile[0])
         else:
            #new datafile
            self.instance.datafiles.create(file_url=file_url)
  
