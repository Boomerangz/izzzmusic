import json
import os
from audiofield.models import AudioFile
from audiofield.widgets import CustomerAudioFileWidget
from django.db.models import Q
from django.forms import ModelForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, TemplateView, RedirectView
import requests
from music.models import Track
from mymusic import settings

__author__ = 'igorzygin'


TEMP_FILE_NAME = 'file.mp3'


class MusicView(ListView):
    model = Track
    template_name = 'music_list2.html'


class MusicUploadView(TemplateView):
    template_name = 'music_upload.html'

    def post(self, request):
        form = CustomerAudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        return redirect('/music/')



def add_audio(request):
    template = 'music_upload.html'
    form = CustomerAudioFileForm()

    # Add audio
    if request.method == 'POST':
        form = CustomerAudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponseRedirect('/')

        # To retain frontend widget, if form.is_valid() == False
        form.fields['audio_file'].widget = CustomerAudioFileWidget()

    data = {
       'audio_form': form,
    }

    return render_to_response(template, data,
           context_instance=RequestContext(request))


class CustomerAudioFileForm(ModelForm):
    class Meta:
        model = Track
        fields = ['audio_file']




def plain_text(chat_id, text):
    tracks=Track.objects.filter(Q(artist__contains=text,album__contains=text, title__contains=text))
    track_strs = ["%d %s %s"%(t.id, t.artist,t.title) for t in tracks]
    tracks_string = track_strs.join("\n")
    r = requests.post('https://api.telegram.org/bot%s/sendMessage'%settings.BOT_TOKEN, data={"chat_id":chat_id, 'text':tracks_string})
    print r


def id_list(chat_id, id_list):
    tracks_list=Track.objects.filter(pk__in=id_list)
    for track in tracks_list:
        if track.telegram_id is None or track.telegram_id == "":
            import urllib
            testfile = urllib.URLopener()
            testfile.retrieve(track.link, TEMP_FILE_NAME)
            filename=TEMP_FILE_NAME
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, files={'audio': open(filename, 'rb')}, data={"duration":300,"chat_id":chat_id, 'performer':track.artist, 'title':track.title}, headers=headers)
            print r.content
            r_js = json.loads(r.content)
            f_id = r_js["result"]["audio"]["file_id"]
            track.telegram_id = f_id
            track.save()
            os.remove(filename)
         else:
            r = requests.post('https://api.telegram.org/bot%s/sendAudio'%settings.BOT_TOKEN, data={"duration":300,"chat_id":chat_id, 'performer':track.artist, 'title':track.title, 'audio':track.telegram_id}, headers=headers)
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
                text_list = text.split(" ")
                if text_list[0][0]=="/":
                    if text_list[0]=="/id":
                        id_list(chat_id, text_list[1:])
                else:
                    plain_text(chat_id, text)
            except:
                pass
            return JsonResponse(response)
        else:
            print "ELSE"
        return JsonResponse({'method': 'sendMessage', 'text':'GOT IT'})


