from django.conf.urls import url

from art import views

urlpatterns = [
    url(r'^artwork/get/$', views.get_artwork, name='get_artwork'),
    url(r'^artwork/delete/$', views.delete_artwork, name='delete_artwork'),
    url(r'^artwork/modal/get/$', views.get_artwork_modal, name='get_artwork_modal'),
]
