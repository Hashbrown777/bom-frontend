from django.template.loader import get_template
from django.shortcuts import render
from django.template import RequestContext,loader
from django.http import HttpResponse

def zoo_dashboard(request):
   t = loader.get_template('admin/zoo_dashboard.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)
