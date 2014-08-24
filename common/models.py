from django.db import models

class Common():

   @staticmethod
   def prepare_config_address(address):
      """ Return address ready for use."""
      if address[:3] is not 'http':
         return 'http://' + address
      return address


