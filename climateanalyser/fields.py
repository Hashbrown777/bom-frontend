from django import forms

class VariablesMultiField(forms.MultipleChoiceField):

   def validate(self, value):
      """ Custom validate to fix issue with our choices are invalid.

      Choices loaded via ajax are invalid in default validate function so
      we have to override it.
      """

      return value
