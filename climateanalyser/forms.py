from django import forms

class ComputeForm(forms.Form):
   data_file_1 = forms.CharField(1000)
   data_file_2 = forms.CharField(1000)
   calculation = forms.ChoiceField(choices=(('correlate', 'Correlate'),))
