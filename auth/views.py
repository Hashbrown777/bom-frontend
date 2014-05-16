from django.template.loader import get_template
from django.template import RequestContext,loader
from django.http import HttpResponse

def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)
   
def register(request):

   form = UserCreateForm()

   #t = loader.get_template('register.html')
   context = RequestContext(request, { 'form':form })
   html = t.render(context)
   return HttpResponse(html)
