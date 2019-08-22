from django.conf.urls import url

from ui import views

urlpatterns = [
    url(r'^iphone-video/stream/$', views.stream_iphone_video, name='stream_iphone_video'),
]
