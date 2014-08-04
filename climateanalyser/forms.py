from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms
from fields import DataFilesField
from models import ComputationDataFile

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

      print 'data files: '
      print self.cleaned_data['datafiles']

      for file_url in self.cleaned_data['datafiles']:

         datafile = DataFile.objects.filter(file_url=file_url)
   
         if datafile:
            #add existing datafile instance
            datafile = datafile[0]
         else:
            datafile = DataFile(file_url=file_url)
            datafile.save()
            #new datafile
  
         ComputationDataFile.objects.create(computation=self.instance,
            datafile=datafile)
