from django.db.models.signals import post_delete
from models import DataFile
import os
from django.conf import settings

def delete_cache(sender, **kwargs):
   """ Delete local cache file when deleting a DataFile from the system """
   os.remove(settings.CACHE_DIR + kwargs['instance'].cached_file)

post_delete.connect(delete_cache, sender=DataFile)


