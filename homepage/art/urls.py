from django.conf.urls import url

from art import views

urlpatterns = [
    url(r'^artwork/get/$', views.get_artwork, name='get_artwork'),
]
