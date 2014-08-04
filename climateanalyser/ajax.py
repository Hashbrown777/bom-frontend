from django.http import HttpResponse
from models import DataFile
import json

def load_datafile_metadata(request):

   datafile = DataFile.objects.get(id=request.POST.get('id'))

   response = ''

   if datafile:
      variables = datafile.get_variables()
      response = json.dumps(variables)

   return HttpResponse(response)
