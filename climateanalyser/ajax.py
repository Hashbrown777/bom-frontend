import json,urllib,rsa,base64
from django.http import HttpResponse
from models import DataFile,Computation
from zooadapter.models import ZooAdapter

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
   """Update the status of a computation. All input from request should be
   rsa encoded"""

   private_key = ZooAdapter.config.get_private_key()

   response = 'failure' # whether or not we failed to update status
   encrypted_status = request.GET.get('status')
   encrypted_comp_id = request.GET.get('id')

   # no input
   if not encrypted_status or not encrypted_comp_id:
      return HttpResponse(response)

   # prepare strings for decryption 
   encrypted_status = urllib.unquote(base64.b64decode(encrypted_status))
   encrypted_comp_id = urllib.unquote(base64.b64decode(encrypted_comp_id))

   # decrypt!
   status = rsa.decrypt(encrypted_status, private_key)
   computation_id = rsa.decrypt(encrypted_comp_id, private_key)

   try:
      computation = Computation.objects.get(id=request.POST.get('id'))
   except Computation.DoesNotExist:
      return HttpResponse(response)

   if computation:
      computation.status = status
      computation.save()
      response = 'success'

   return HttpResponse(response)
