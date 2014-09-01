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
 
def update_computation_status(request):

   computation = Computation.objects.get(id=request.POST.get('id'))
   status = request.POST.get('status')

   # whether or not we failed to update status
   response = 'failure'

   if computation:
      computation.status = status
      computation.save()
      response = 'success'

   return HttpResponse(response)
      
