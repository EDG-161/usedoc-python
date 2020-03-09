from django.db import models
from FaceVerify.storage import OverwriteStorage

class AlbumImage(models.Model):
    album = models.CharField(max_length=200)
    image = models.ImageField(max_length=15000, storage=OverwriteStorage(),upload_to='static/static/images/')

    def __unicode__(self,):
        return str(self.image)