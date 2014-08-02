'''
from django.contrib import admin
from django import forms
from climateanalyser.models import Computation, DataFile
from fields import DataFilesField
from forms import ComputationForm

class AdminComputationForm(ComputationForm):
   class Meta:
      fields = ['id', 'created_by', 'created_date', 'completed_date']


class ComputationAdmin(admin.ModelAdmin):
   form = AdminComputationForm
   list_display = ('id', 'created_by', 'created_date', 'completed_date')


admin.site.register(Computation, ComputationAdmin)
'''
