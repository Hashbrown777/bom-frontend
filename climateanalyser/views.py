from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

# Create your views here.
def index(request):
   #return HttpResponse("Woo !!! climateanalyser!!")
   t = get_template('base.html')
   html = t.render(Context())
   return HttpResponse(html)
