from datetime import datetime
from django.utils.dateformat import format
from django.template.loader import get_template
from django.shortcuts import render
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from climateanalyser.forms import ComputeForm
from climateanalyser.models import *

#Default page
def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)

#Form for creating new computation
def compute(request):

   if request.method == 'POST':

      #grab form with the user input
      form = ComputeForm(request.POST)

      if form.is_valid():

         user = request.user

         #Save our data
         computation = Computation(created_by=user,created_date=datetime.now(),
               calculation=form.cleaned_data['calculation'])
         computation.save()

         data_file_1 = DataFile(path=form.cleaned_data['data_file_1'],
               computation=computation)
         data_file_2 = DataFile(path=form.cleaned_data['data_file_2'],
               computation=computation)

         data_file_1.save()
         data_file_2.save()

         #show result page
         return HttpResponseRedirect('/result?computation=' 
               + str(computation.id))

   else:
      form = ComputeForm()

   return render(request, 'compute_form.html', { 'form' : form, })

#Display result after submitting computation
def result(request):
   #grab computation id from URL string
   computation = Computation.objects.get(id=request.GET.get('computation'))
   return render(request, 'result.html', {'computation': computation})

#display single computation
def computation(request):
   computation = Computation.objects.get(id=request.GET.get('id'))

   return render(request, 'computation.html', {'computation': computation})


#View currently logged in user's computations
def my_computations(request):
   computations = Computation.objects.filter(created_by=request.user)
   return render(request, 'computations.html', { 'computations' : computations })

#View all computations in the system
def computations(request):
   computations = Computation.objects.filter()
   return render(request, 'computations.html', { 'computations' : computations })

