from climateanalyser.models import Computation,DataFile
from django.forms import ModelForm
from django import forms

class DataFileForm(forms.Form):
   
   #Override init funct so we can add custom ARRAY of file_url fields.
   #This is so on the frontend, we can easily use JS to add more inputs.
   def __init__(self, *args, **kwargs):
      super(DataFileForm, self).__init__(*args, **kwargs)
      
      field = forms.CharField(label='Data Files', max_length=1000)
      field.widget = forms.TextInput( attrs={'id' : 'file_url_1'}) 
      self.fields['file_url[]'] = field

class ComputationForm(ModelForm):
   class Meta:
      model=Computation
      fields = ['calculation']

