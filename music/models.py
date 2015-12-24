import uuid
from django.db import models
from django.db.models.signals import post_save
import tinys3

__author__ = 'igorzygin'


from django.conf import settings
from audiofield.fields import AudioField
import os.path



class Track(models.Model):
    artist = models.CharField(max_length=255, default="", blank=True)
    album = models.CharField(max_length=255, default="", blank=True)
    title = models.CharField(max_length=255, default="", blank=True)
    link = models.CharField(max_length=255, default="", blank=True)
    # Add the audio field to your model
    audio_file = AudioField(upload_to='music', blank=True,
                            ext_whitelist=(".mp3", ".wav", ".ogg"),
                            help_text=("Allowed type - .mp3, .wav, .ogg"))

    # Add this method to your model
    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<ul class="playlist"><li style="width:250px;">\
            <a href="%s">%s</a></li></ul>' % (file_url, os.path.basename(self.audio_file.name))
            return player_string

    def save(self, **kwargs):
        super(Track, self).save()
        import eyed3
        audiofile = eyed3.load(self.audio_file.path)
        self.artist=audiofile.tag.artist
        self.album=audiofile.tag.album
        self.title=audiofile.tag.title

        # Creating a simple connection
        result=  super(Track, self).save()
        return result

    @staticmethod
    def post_save_action(sender, instance, *args, **kwargs):
        if instance.link == None or len(instance.link) == 0:
            import boto
            conn = boto.connect_s3(settings.S3_ACCESS_KEY,
            settings.S3_SECRET_KEY)
            import boto.s3
            bucket = conn.create_bucket(settings.S3_BUCKET_NAME,
                location=boto.s3.connection.Location.DEFAULT)
            name = instance.audio_file.path.split('/')[-1]
            testfile = instance.audio_file.path
            print 'Uploading %s to Amazon S3 bucket %s' % \
               (testfile, settings.S3_BUCKET_NAME)

            import sys
            def percent_cb(complete, total):
                sys.stdout.write('.')
                sys.stdout.flush()

            from boto.s3.key import Key
            k = Key(bucket)
            k.key = name
            k.set_contents_from_filename(testfile,
                cb=percent_cb, num_cb=10)
            k.set_acl("public-read")
            instance.link = 'https://s3.amazonaws.com/' + settings.S3_BUCKET_NAME + '/' + name
            instance.save()



    def __unicode__(self):
        return self.str()

    def str(self):
        return self.artist +" - " +self.title

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')

post_save.connect(Track.post_save_action, dispatch_uid=str(uuid.uuid1()), sender=Track)