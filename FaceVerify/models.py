from django.db import models

class AlbumImage(models.Model):
    album = models.CharField(max_length=200)
    image = models.ImageField(upload_to='static/static/images/')

    def __unicode__(self,):
        return str(self.image)