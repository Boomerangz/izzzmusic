from audiofield.models import AudioFile
from audiofield.widgets import CustomerAudioFileWidget
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, TemplateView, RedirectView
from music.models import Track

__author__ = 'igorzygin'



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



def income_message(request):
        if request.method=='POST':
            print "POST"
            message = request.POST['message']
            print message
        else:
            print "ELSE"
        return "GOT IT"