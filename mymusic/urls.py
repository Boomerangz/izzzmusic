from django.conf.urls import patterns, include, url
from django.contrib import admin
from music.views import MusicView, MusicUploadView, add_audio

from django.conf.urls.static import static
from mymusic import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mymusic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^music/upload', add_audio),
    url(r'^music/', MusicView.as_view()),



) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)