
from django.db import models

__author__ = 'igorzygin'



class Track(models.Model):
    artist = models.CharField(max_length=255, default="", blank=True)
    album = models.CharField(max_length=255, default="", blank=True)
    title = models.CharField(max_length=255, default="", blank=True)
    duration = models.IntegerField(max_length=255, default=0, blank=True)
    link = models.CharField(max_length=255, default="", blank=True)
    telegram_id = models.CharField(max_length=255, default="", blank=True)

    def __unicode__(self):
        return self.str()

    def str(self):
        return self.artist +" - " +self.title