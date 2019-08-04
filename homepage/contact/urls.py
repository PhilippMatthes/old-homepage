from django.conf.urls import url

from contact import views


urlpatterns = [
    url(r'^message/send/$', views.send_message, name='send_contact_message'),
]
