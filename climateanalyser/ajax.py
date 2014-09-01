from django.http import HttpResponse
from models import DataFile,Computation
import json

def load_datafile_metadata(request):

   response = 'failure'

   try:
      datafile = DataFile.objects.get(id=request.POST.get('id'))
   except DataFile.DoesNotExist:
      return HttpResponse(response)

   if datafile:
      variables = datafile.get_variables()
      response = json.dumps(variables)

   return HttpResponse(response)
 
def update_computation_status(request):

   response = 'failure' # whether or not we failed to update status
   status = request.POST.get('status')

   try:
      computation = Computation.objects.get(id=request.POST.get('id'))
   except Computation.DoesNotExist:
      return HttpResponse(response)

   if computation:
      computation.status = status
      computation.save()
      response = 'success'

   return HttpResponse(response)
