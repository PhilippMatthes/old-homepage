from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse

from homepage import settings


def send_message(request):
    if not request.is_ajax():
        return JsonResponse({"success": False})

    text = request.POST.get("text")
    if not text:
        return JsonResponse({"success": False})

    text_to_send = f'Message:\n' \
                   f'{text}\n' \
                   f'\n' \
                   f'Meta Information:\n' \
                   f'{request.META}'

    try:
        send_mail("New Message from your homepage", text_to_send, settings.EMAIL_FROM, [settings.EMAIL_TO])
        return JsonResponse({"success": True})

    except BadHeaderError:
        return JsonResponse({"success": False})
