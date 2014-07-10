from django.db import models
from django.db.models.fields import *
from django import forms

class DataFilesField(forms.CharField):

   description = 'Textarea of datafiles.'
   widget = forms.Textarea

   def clean(self, value):
      super(DataFilesField, self).clean(value)
      data_files = value.splitlines()

      if len(data_files) < 2:
         raise ValidationError('Please enter at least two data files.')

      return data_files
