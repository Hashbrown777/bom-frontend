from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class DataFile(models.Model):
   file_url = models.CharField(max_length=1000)
   cached_file = models.CharField(max_length=1000)
   last_modified = models.DateTimeField('last modified')

   def save(self, *args, **kwargs):
      self.cached_file = self.file_url
      self.last_modified = datetime.now()
      super(DataFile, self).save(*args, **kwargs)

class Computation(models.Model):
      created_by = models.ForeignKey(User)
      created_date = models.DateTimeField('date created')
      completed_date = models.DateTimeField('date completed',null=True,
            blank=True)

      CALCULATION_CHOICES = (
            ('correlate', 'Correlate'),
            ('regress', 'Regress'),
      )

      calculation = models.CharField(max_length=100,
            choices=CALCULATION_CHOICES, default='correlate')

      datafiles = models.ManyToManyField(DataFile)

      #Get the URL of the result from Zoo.
      def result(self):
         return ZooAdapter.get_result(self.datafiles.all(), self.calculation)

      def save(self, *args, **kwargs):
         if self.created_date is None:
            self.created_date = datetime.now()
         super(Computation, self).save(*args, **kwargs)



class ZooAdapter():

   #Get result URL from Zoo.
   @staticmethod
   def get_result(data_files, calculation):

      #must have at least two data files
      if len(data_files) < 2:
         return;

      result_path = ('http://130.56.248.143/cgi-bin/zoo_loader.cgi?request='
                     'Execute&service=WPS&version=1.0.0.0&identifier='
                     'Operation&DataInputs=selection=' + calculation + ';urls=')

      #append all data files
      for data_file in data_files:
         result_path += data_file.file_url + ','

      #Remove trailing comma
      result_path = result_path[:-1]

      return result_path


