from django.db import models
from django.contrib.auth.models import User

class ClimateAnalyserUser(models.Model):
   user = models.OneToOneField(User);
   
   def get_computation(computation_id):
      print 'cool and fun times'

   def get_computations():
      #return all computations
      print 'cool and fun times'
   
   def userCreateForm():
      #return all computations
      print 'cool and fun times'
