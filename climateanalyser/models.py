from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import hashlib, urllib 
from jsonfield import JSONField
from zooadapter.models import ZooAdapter
from solo.models import SingletonModel
from common.models import Common
import json

class ClimateAnalyserConfig(SingletonModel):

   class Meta:
      verbose_name_plural = "ClimateAnalyser Config"
      verbose_name = "ClimateAnalyser Config"

   tilemill_server_address = models.CharField(max_length=255)

   def get_tilemill_server_address(self):
      return Common.prepare_config_address(self.tilemill_server_address)

class DataFile(models.Model):
   file_url = models.CharField(max_length=1000,unique=True)
   cached_file = models.CharField(max_length=1000)
   last_modified = models.DateTimeField('last modified')
   metadata = JSONField()

   def clean(self):
      #Create cached file and save data

      #file name is md5 string of url
      self.cached_file = hashlib.md5(self.file_url).hexdigest()
      urllib.urlretrieve(self.file_url, settings.CACHE_DIR + self.cached_file)

      self.metadata = ZooAdapter.get_datafile_metadata(self.file_url)

      self.last_modified = datetime.now()

   def get_variables(self):
      return json.loads(self.metadata)

   def __unicode__(self):
      return self.file_url

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

   def result_wms(self):
      #Get the URL of the result from Zoo in WMS format
      return ZooAdapter.get_result(self.get_computationdata().all(), 
            self.calculation, 'wms')

   def result_nc(self):
      #Get the URL of the result from Zoo in NC format
      return ZooAdapter.get_result(self.get_computationdata().all(), 
            self.calculation, 'ncfile')

   def result_opendap(self):
      #Get the URL of the result from Zoo in Opendap format
      return ZooAdapter.get_result(self.get_computationdata().all(), 
            self.calculation, 'opendap')

   def clean(self):
      self.created_date = datetime.now()

   def get_computationdata(self):
      return ComputationData.objects.filter(computation=self).order_by('id')

class ComputationData(models.Model):
   datafile = models.ForeignKey(DataFile)   
   computation = models.ForeignKey(Computation)
   variables = JSONField()

   def clean(self):
      # make sure selected variables exist in datafile
      for variable in self.variables:
         if variable not in self.datafile.get_variables():
            raise ValidationError('Variable does not exist in Data File.')


