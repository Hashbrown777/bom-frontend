from django.db import models
from auth.models import ClimateAnalyserUser
#import xml.etree.cElementTree as etree

class ClimateAnalyser():

   def new_computation(data_file):
      print 'woop'
      
class Computation(models.Model):
      data_file = models.CharField(max_length=1000)
      created_by = models.ForeignKey(ClimateAnalyserUser)
      created_date = models.DateTimeField('date created')
      completed_date = models.DateTimeField('date completed')

'''
      zoo_adapter = ZooAdapter()
      ZooAdapter.get_result(this.data_file)
      return;
'''

class ZooAdapter():

   def get_result(data_file):

      result_path = 'http://130.56.248.143/cgi-bin/operators/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=Correlate&DataInputs=url1%3Dwww.google.com%3Burl2%3Dwww.example.com.au%2Fsample.nc'

      xml_doc = open(result_path, 'r')
      xml_doc_data = xml_doc.read()
      xml_doc_tree = etree.XML(xml_doc_data)

      print xml_doc_tree
      
      return 'woo'

      

