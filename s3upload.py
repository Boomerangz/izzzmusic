import boto

AWS_ACCESS_KEY_ID = 'AKIAJGXZ2FRDRQHCDFIA'
AWS_SECRET_ACCESS_KEY = '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'
path = '/Users/igorzygin/Dropbox/developing/python/MyMusic/mymusic/media/music/audio-file-ITCZJ-6121552141.mp3'
name = path.split('/')[-1]


bucket_name = 'izzmusic1'
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)


import boto.s3
bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

testfile = path
print 'Uploading %s to Amazon S3 bucket %s' % \
   (testfile, bucket_name)

import sys
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

from boto.s3.key import Key
k = Key(bucket)
k.key = name
k.set_contents_from_filename(testfile,
    cb=percent_cb, num_cb=10)
