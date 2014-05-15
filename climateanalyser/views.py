from django.template.loader import get_template
from django.shortcuts import render
from django.template import RequestContext,loader
from django.http import HttpResponse
from climateanalyser.forms import ComputeForm
from climateanalyser.models import ClimateAnalyser

def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)

def compute(request):

   if request.method == 'POST':

         form = ComputeForm(request.POST)

         if form.is_valid():
            return HttpResponseRedirect('/result/')

   else:
      form = ComputeForm()

   return render(request, 'compute_form.html', { 'form' : form, })


def result(request):
   print 'hello'

