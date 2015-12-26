import json
import os
import uuid
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, TemplateView, RedirectView
import requests
from music.models import Track
from mymusic import settings
import eyed3

__author__ = 'igorzygin'


def temp_file_name():
    path = '/tmp/%s.mp3' % uuid.uuid1()
    return path


class MusicView(ListView):
    model = Track
    template_name = 'music_list2.html'


def handle_uploaded_file(f, dest_path):
    with open(dest_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(path):
    import boto
    conn = boto.connect_s3(settings.S3_ACCESS_KEY,
    settings.S3_SECRET_KEY)
    import boto.s3
    bucket = conn.create_bucket(settings.S3_BUCKET_NAME,
        location=boto.s3.connection.Location.DEFAULT)
    name = path.split('/')[-1]
    testfile = path
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
    link = 'https://s3.amazonaws.com/' + settings.S3_BUCKET_NAME + '/' + name
    return link

def add_audio(request):
    template = 'music_upload.html'
    if request.method == 'POST':
        if 'audio' in request.FILES:
            path = temp_file_name()
            handle_uploaded_file(request.FILES['audio'], path)
            audiofile = eyed3.load(path)
            artist=audiofile.tag.artist
            album=audiofile.tag.album
            title=audiofile.tag.title
            duration=audiofile.info.time_secs
            link=upload_file(path)
            os.remove(path)
            t=Track.objects.create(artist=artist,album=album,title=title,duration=duration,link=link)
            t.save()
            return HttpResponseRedirect('/')
    data = {}
    return render_to_response(template, data,
           context_instance=RequestContext(request))




def plain_text(chat_id, text):
    strings = text.split(' ')
    tracks=Track.objects.all()
    for str in strings:
        tracks = tracks.filter(Q(artist__contains=text)|Q(album__contains=text)|Q(title__contains=text))
    if len(tracks)==1:
        id_list(chat_id, [tracks[0].id])
    else:
        track_strs = ["%d %s %s"%(t.id, t.artist,t.title) for t in tracks]
        tracks_string = "\n".join(track_strs)
        r = requests.post('https://api.telegram.org/bot%s/sendMessage'%settings.BOT_TOKEN, data={"chat_id":chat_id, 'text':tracks_string})
        print r.body


def id_list(chat_id, id_list):
    tracks_list=Track.objects.filter(pk__in=id_list)
    for track in tracks_list:
        if track.telegram_id is None or track.telegram_id == "":
            import urllib
            testfile = urllib.URLopener()
            path = temp_file_name()
            testfile.retrieve(track.link, path)
            filename=path
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, files={'audio': open(filename, 'rb')}, data={"duration":300,"chat_id":chat_id, 'performer':track.artist, 'title':track.title})
            print r.content
            r_js = json.loads(r.content)
            f_id = r_js["result"]["audio"]["file_id"]
            track.telegram_id = f_id
            track.save()
            os.remove(filename)
        else:
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, data={"duration":track.duration,"chat_id":chat_id, 'performer':track.artist, 'title':track.title, 'audio':track.telegram_id})
            print r.content

def random_list(chat_id, size):
    tracks_list=Track.objects.raw("SELECT * FROM music_track ORDER BY RANDOM() LIMIT %d"%int(size))
    for track in tracks_list:
        if track.telegram_id is None or track.telegram_id == "":
            import urllib
            testfile = urllib.URLopener()
            path = temp_file_name()
            testfile.retrieve(track.link, path)
            filename=path
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, files={'audio': open(filename, 'rb')}, data={"duration":300,"chat_id":chat_id, 'performer':track.artist, 'title':track.title})
            print r.content
            r_js = json.loads(r.content)
            f_id = r_js["result"]["audio"]["file_id"]
            track.telegram_id = f_id
            track.save()
            os.remove(filename)
        else:
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, data={"duration":track.duration,"chat_id":chat_id, 'performer':track.artist, 'title':track.title, 'audio':track.telegram_id})
            print r.content



# {"update_id":202480832,
# "message":{"message_id":8,"from":{"id":1398413,"first_name":"Igor","last_name":"Zygin"},"chat":{"id":1398413,"first_name":"Igor","last_name":"Zygin","type":"private"},"date":1450995712,"text":"asd"}}
def income_message(request):
        if request.method=='POST':
            print "POST"
            print request.body
            body = json.loads(request.body)
            chat_id = body["message"]["chat"]["id"]
            response = {}
            try:
                text = body["message"]["text"]
                print text
                text_list = text.split(" ")
                print text_list
                if text_list[0][0]=="/":
                    print 'command'
                    if text_list[0]=="/id":
                        print "/id"
                        id_list(chat_id, text_list[1:])
                    elif text_list[0]=="/random":
                        print "/random"
                        size = int(text_list[1]) if len(text_list)>1 else 10
                        random_list(chat_id, size)
                else:
                    plain_text(chat_id, text)
            except Exception as e:
                print e
                pass
            return JsonResponse(response)
        else:
            print "ELSE"
        return JsonResponse({'method': 'sendMessage', 'text':'GOT IT'})


