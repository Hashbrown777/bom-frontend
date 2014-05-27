from django import forms

class UserRegisterForm(forms.Form):
   first_name = forms.CharField(1000)
   last_name = forms.CharField(1000)
   username = forms.CharField(1000)
   email = forms.EmailField(1000)
   password = forms.CharField(widget=forms.PasswordInput)
