from django.template.loader import get_template
from django.template import RequestContext,loader
from django.http import HttpResponse
from auth.models import *
from auth.forms import *
from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
   t = loader.get_template('index.html')
   context = RequestContext(request, {})
   html = t.render(context)
   return HttpResponse(html)
   
def register(request):

   if request.method == 'POST':
      userName = request.REQUEST.get('username', None)
      userPass = request.REQUEST.get('password', None)
      userMail = request.REQUEST.get('email', None)
      userFirst = request.REQUEST.get('first_name', None)
      userLast = request.REQUEST.get('last_name', None)
      user = User.objects.create_user(username=userName,email=userMail,password=userPass)
      user.last_name = userLast;
      user.first_name = userFirst;
      user.save();
      return render(request,'index.html')
   else:
      form = UserRegisterForm()
      t = loader.get_template('register.html')
      context = RequestContext(request, { 'form':form })
      html = t.render(context)
      return HttpResponse(html)
