from django.conf.urls import patterns, include, url
from django.contrib import admin
from music.views import MusicView, add_audio, income_message

from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from mymusic import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mymusic.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', auth_views.login),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', add_audio),
    url(r'^message/', income_message),
    url(r'', MusicView.as_view()),





) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
