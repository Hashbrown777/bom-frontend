from django.db import models
#from auth.models import ClimateAnalyserUser
from django.contrib.auth.models import User

class Computation(models.Model):
      created_by = models.ForeignKey(User)
      created_date = models.DateTimeField('date created')
      completed_date = models.DateTimeField('date completed',null=True)

      def get_data_files(self):
         return DataFile.objects.filter(computation=self.id)

      def get_result(self):
         return ZooAdapter.get_result(self.get_data_files())

class ZooAdapter():

   @staticmethod
   def get_result(data_files):

      result_path = 'http://130.56.248.143/cgi-bin/operators/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=Correlate&DataInputs=url&url1=' + data_files[0].path + '&url2=' + data_files[1].path + '&Fsample.nc'

      return result_path

class DataFile(models.Model):
   path = models.CharField(max_length=1000)
   computation = models.ForeignKey(Computation)

