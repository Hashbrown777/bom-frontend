from django.db import models
import HTMLParser, re
from solo.models import SingletonModel
import urllib

class ZooAdapterConfig(SingletonModel):
   zoo_server_address = models.CharField(max_length=255)
   thredds_server_address = models.CharField(max_length=255)

   def get_zoo_server_address(self):
      """ Return zoo server address ready for use."""
      return self._prepare_address(self.zoo_server_address)

   def get_thredds_server_address(self):
      """ Return thredds server address ready for use."""
      return self._prepare_address(self.thredds_server_address)

   def _prepare_address(self, address):
      """ Return address ready for use."""
      if address[:3] is not 'http':
         return 'http://' + address
      return address

   def __unicode__(self):
      return u"Zoo Adapter Configuration"

class ZooAdapter():

   config = ZooAdapterConfig.objects.get()

   @staticmethod
   def get_datafile_metadata(url):
      """Get datafile metadata in JSON format
         
      Keyword arguments:
      url -- datafile remote url
      """

      filehandle = urllib.urlopen(ZooAdapter.config.get_zoo_server_address() +
            '/samples/sample_3D-Metadata.txt')

      data = filehandle.read()
      filehandle.close()
      return data

   @staticmethod
   def get_descriptor_file(computationdata_list, calculation):
      """Get the file that describes the result of our computation.

      This page loads our result files, and returns a list of them (as well as
      other information).

      Note: at least two datafiles are required

      Keyword arguments:
      datafiles -- array of datafile objects to perform calculation on
      calculation -- calculation we want to perform, eg 'correlate', 'regress'
      """

      #must have at least two data files
      #TODO: exception?
      if len(computationdata_list) < 2:
         return;

      descriptor_file = (ZooAdapter.config.get_zoo_server_address() +
            '/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS'
            '&version=1.0.0.0&identifier='
            'Operation&DataInputs=selection=' + calculation + ';urls=')

      #append all data files
      for computationdata in computationdata_list:
         descriptor_file += computationdata.datafile.file_url + ','

      #Remove trailing comma
      descriptor_file = descriptor_file[:-1]

      return descriptor_file

   @staticmethod
   def get_result(computationdata_list, calculation, format):
      """Get the url of the result file for calculation performed on datafiles.

      Keyword arguments:
      datafiles -- array of datafile objects to perform calculation on
      calculation -- calculation we want to perform, eg 'correlate', 'regress'
      format -- format of result file. either 'wms', 'opendap', or 'ncfile'
      """

      #file containing list of result links
      descriptor_file = ZooAdapter.get_descriptor_file(computationdata_list, 
            calculation)

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