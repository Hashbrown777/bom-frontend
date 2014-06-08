from datetime import datetime
from django.utils.dateformat import format
from django.template.loader import get_template
from django.shortcuts import render
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from climateanalyser.forms import ComputationForm,DataFileForm
from climateanalyser.models import *
from django.contrib import messages

#Default page
def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)

#Form for creating new computation
def compute(request):

   if (request.user.is_authenticated() == False):
      messages.error(request, 'You must login to view that page.')
      return HttpResponseRedirect('/auth/login')

   computation_form = ComputationForm()
   data_file_form = DataFileForm()

   if (request.POST.get('file_url')):
      return HttpResponse(request.POST.get('file_url'))

   return render(request, 'compute_form.html', { 
         'computation_form' : computation_form, 
         'data_file_form' : data_file_form })

#display single computation
def computation(request):
   computation = Computation.objects.get(id=request.GET.get('id'))

   return render(request, 'computation.html', {'computation': computation})

#View list of computations in the system
def computations(request):

   template_params = {}

   #Filter for current user
   if (request.GET.get('show_mine')):
      user = request.user
      template_params['computations'] = Computation.objects.filter(
            created_by=user)
      template_params['show_mine'] = True;
   else:
      template_params['computations'] = Computation.objects.filter()
      template_params['show_mine'] = False;

   return render(request, 'computations.html', template_params)

