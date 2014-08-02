from django.conf import settings
from datetime import datetime
from django.db import models
from fields import JSONField 
from django.contrib.auth.models import User
import hashlib, urllib, re, HTMLParser 

class DataFile(models.Model):
   file_url = models.CharField(max_length=1000,unique=True)
   cached_file = models.CharField(max_length=1000)
   last_modified = models.DateTimeField('last modified')
   dds_info = JSONField(max_length=1000)
   das_info = JSONField(max_length=1000)

   def save(self, *args, **kwargs):
      #Create cached file and save data

      #file name is md5 string of url
      self.cached_file = hashlib.md5(self.file_url).hexdigest()
      urllib.urlretrieve(self.file_url, 
            settings.CACHE_DIR + self.cached_file)

      self.dds_info = ZooAdapter.get_datafile_info(self.file_url, 'dds')
      self.das_info = ZooAdapter.get_datafile_info(self.file_url, 'das')

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

   '''
   def result_wms(self):
      #Get the URL of the result from Zoo in WMS format
      return ZooAdapter.get_result(self.data.all(), self.calculation, 'wms')

   def result_nc(self):
      #Get the URL of the result from Zoo in NC format
      return ZooAdapter.get_result(self.data.all(), self.calculation, 'ncfile')

   def result_opendap(self):
      #Get the URL of the result from Zoo in Opendap format
      return ZooAdapter.get_result(self.data.all(), self.calculation, 'opendap')
   '''

   def save(self, *args, **kwargs):
      if self.created_date is None:
         self.created_date = datetime.now()
      super(Computation, self).save(*args, **kwargs)

class ComputationData(models.Model):
   datafile = models.ForeignKey(DataFile)   
   computation = models.ForeignKey(Computation)
   variables = JSONField(max_length=1000)

class ZooAdapter():

   @staticmethod
   def get_datafile_info(url,type):
      """Get info about datafile, such as variables, attributes, as JSON.

      Keyword arguments:
      url -- datafile remote url
      type -- type of data to get. currently 'dds' or 'das'
      """

      filehandle = urllib.urlopen('http://115.146.84.143:8080/thredds/dodsC/'
            + 'datafiles/outputs/correlate_sample_1D_sample_3D.nc.' + type)

      data = filehandle.read()

      filehandle.close()

      return data


   @staticmethod
   def get_descriptor_file(datafiles, calculation):
      """Get the file that describes the result of our computation.

      This page loads our result files, and returns a list of them (as well as
      other information).

      Note: at least two datafiles are required

      Keyword arguments:
      datafiles -- array of datafile objects to perform calculation on
      calculation -- calculation we want to perform, eg 'correlate', 'regress'
      """

      #must have at least two data files
      if len(datafiles) < 2:
         return;

      descriptor_file = ('http://130.56.248.143/cgi-bin/zoo_loader.cgi?request='
                     'Execute&service=WPS&version=1.0.0.0&identifier='
                     'Operation&DataInputs=selection=' + calculation + ';urls=')

      #append all data files
      for datafile in datafiles:
         descriptor_file += datafile.file_url + ','

      #Remove trailing comma
      descriptor_file = descriptor_file[:-1]

      return descriptor_file

   @staticmethod
   def get_result(datafiles, calculation, format):
      """Get the url of the result file for calculation performed on datafiles.

      Keyword arguments:
      datafiles -- array of datafile objects to perform calculation on
      calculation -- calculation we want to perform, eg 'correlate', 'regress'
      format -- format of result file. either 'wms', 'opendap', or 'ncfile'
      """

      #file containing list of result links
      descriptor_file = ZooAdapter.get_descriptor_file(datafiles, calculation)

      result_url = ''

      filehandle = urllib.urlopen(descriptor_file)

      #find our result link

      regex = '\[' + format + '\](.*?)\[/' + format + '\]'

      for line in filehandle.readlines():
         match = re.search(regex, line)
         if match:
            result_url = match.group(1)
            break

      # decode html entities
      html_parser = HTMLParser.HTMLParser()
      result_url = html_parser.unescape(result_url)

      filehandle.close()
      return result_url
