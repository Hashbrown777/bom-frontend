from django.template.loader import get_template
from django.template import RequestContext,loader
from django.http import HttpResponse

def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)
