from django.contrib import admin
from climateanalyser.models import Computation, DataFile

class DataFileInline(admin.StackedInline):
   model = DataFile
   extra = 2

class ComputationAdmin(admin.ModelAdmin):
   list_display = ['id', 'created_by', 'created_date', 'completed_date']
   inlines = [DataFileInline]

admin.site.register(Computation, ComputationAdmin)


