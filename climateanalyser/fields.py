from django.db import models
from django.db.models.fields import *
from django import forms
from django.core.exceptions import ValidationError
import json

class JSONField(models.Field):

   def __init__(self, *args, **kwargs):
      super(JSONField, self).__init__(*args, **kwargs)

   def db_type(self, connection):
      return 'char(%s)' % self.max_length

   def to_python(self, value):
      return json.loads(value)

   def get_prep_value(self, value):
      return json.dumps(value)

   def get_internal_type(self):
      return 'CharField'

   def value_to_string(self, obj):
      value = self._get_val_from_obj(obj)
      return self.get_prep_value(value)
    
'''
class DataFilesField(forms.CharField):

   description = 'Textarea of datafiles.'
   widget = forms.Textarea

   def prepare_value(self, value):
      # Set value to list of files instead of DataFile IDs

      if not value:
         return ''

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

'''
