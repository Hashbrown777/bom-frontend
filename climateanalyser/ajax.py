import json,urllib,rsa,base64
from django.http import HttpResponse
from models import DataFile,Computation
from zooadapter.models import ZooAdapter,ZooComputationStatus

def load_datafile_variables(request):

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
   encrypted_status_id = request.GET.get('status')
   encrypted_comp_id = request.GET.get('id')

   # no input
   if not encrypted_status_id or not encrypted_comp_id:
      return HttpResponse(response)

   try:
      # prepare strings for decryption 
      encrypted_status_id = urllib.unquote(base64.b64decode(encrypted_status_id))
      encrypted_comp_id = urllib.unquote(base64.b64decode(encrypted_comp_id))

      # decrypt!
      status_id = rsa.decrypt(encrypted_status_id, private_key)
      computation_id = rsa.decrypt(encrypted_comp_id, private_key)

      status = ZooComputationStatus.objects.get(code=status_id)
      computation = Computation.objects.get(id=computation_id)

   except Exception: 
      return HttpResponse(response)

   if computation and status:
      computation.status = status
      computation.save()
      response = 'success'

   return HttpResponse(response)

# Returns the maximum and minimum values on a map
def get_data_range(request):
   # Default is -50 to 50
   response = '{"min": -50,"max": 50}'

   map_url = request.GET.get('wms_resource')
   layer = request.GET.get('layer')

   resp = urllib.urlopen(map_url + '?service=WMS&version=1.3.0'
                         + '&request=GetMetadata&item=minmax&layers='
                         + layer + '&srs=EPSG%3A4326&bbox=-180,-90,180,90'
                         + '&width=50&height=50')

   if resp.getcode() == 200:
      response = resp.read()

   return HttpResponse(response, content_type="application/json")
