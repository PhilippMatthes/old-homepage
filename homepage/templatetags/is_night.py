from django import template
from django.utils import timezone
from datetime import datetime, time

register = template.Library()

@register.filter
def is_night(now):
    now = timezone.now().time()
    begin_time = time(19,00)
    end_time = time(10,00)
    if begin_time < end_time:
        return now >= begin_time and now <= end_time
    else:
        return now >= begin_time or now <= end_time
