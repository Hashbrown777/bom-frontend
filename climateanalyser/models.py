from django.db import models
from django.contrib.auth.models import User

class Computation(models.Model):
      created_by = models.ForeignKey(User)
      created_date = models.DateTimeField('date created')
      completed_date = models.DateTimeField('date completed',null=True)
      calculation = models.CharField(max_length=100)

      #Return all the data files associated with this computation.
      def get_data_files(self):
         return DataFile.objects.filter(computation=self.id).order_by('id')

      #Get the URL of the result from Zoo.
      def get_result(self):
         return ZooAdapter.get_result(self.get_data_files(), self.calculation)
    
class ZooAdapter():

   #Get result URL from Zoo.
   @staticmethod
   def get_result(data_files, calculation):

      result_path = ('http://130.56.248.143/cgi-bin/zoo_loader.cgi?request='
                     'Execute&service=WPS&version=1.0.0.0&identifier='
                     'Operation&DataInputs=selection=' + calculation + ';urls='
                     + data_files[0].path + ',' + data_files[1].path)

      return result_path

class DataFile(models.Model):
   path = models.CharField(max_length=1000)
   computation = models.ForeignKey(Computation)

