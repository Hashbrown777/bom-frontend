from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import hashlib
import urllib

class DataFile(models.Model):
   class Meta:
      #order by relationship with computation
      ordering = ['computationdatafile__id']

   file_url = models.CharField(max_length=1000)
   cached_file = models.CharField(max_length=1000)
   last_modified = models.DateTimeField('last modified')

   def save(self, *args, **kwargs):
      #Create cache file
      self.cached_file = hashlib.md5(self.file_url).hexdigest()
      urllib.urlretrieve(self.file_url, 
            'climateanalyser/datafiles/' + self.cached_file)

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

      datafiles = models.ManyToManyField(DataFile,through='ComputationDataFile')

      #Get the URL of the result from Zoo.
      def result(self):
         return ZooAdapter.get_result(self.datafiles.all(), self.calculation)

      def save(self, *args, **kwargs):
         if self.created_date is None:
            self.created_date = datetime.now()
         super(Computation, self).save(*args, **kwargs)

class ComputationDataFile(models.Model):
   # This class used so we can have separate datafile order per computation
   datafile = models.ForeignKey(DataFile)
   computation = models.ForeignKey(Computation)

class ZooAdapter():

   #Get result URL from Zoo.
   @staticmethod
   def get_result(datafiles, calculation):

      #must have at least two data files
      if len(datafiles) < 2:
         return;

      result_path = ('http://130.56.248.143/cgi-bin/zoo_loader.cgi?request='
                     'Execute&service=WPS&version=1.0.0.0&identifier='
                     'Operation&DataInputs=selection=' + calculation + ';urls=')

      #append all data files
      for datafile in datafiles:
         result_path += datafile.file_url + ','

      #Remove trailing comma
      result_path = result_path[:-1]

      return result_path


