from django.db import models
from django.db.models.fields import *
from django import forms
from models import DataFile
from django.core.exceptions import ValidationError

class DataFilesField(forms.CharField):

   description = 'Textarea of datafiles.'
   widget = forms.Textarea

   def prepare_value(self, value):
      # Set value to list of files instead of DataFile IDs

      if value == "":
         return value 

      return_value = ''
      
      for id in value:
         return_value += DataFile.objects.get(id=id).file_url + '\n'

      return return_value

   def clean(self, value):
      super(DataFilesField, self).clean(value)
      datafiles = value.splitlines()

      if len(datafiles) < 2:
         raise ValidationError('Please enter at least two data files.')

      return datafiles


