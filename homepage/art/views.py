from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from art.models import Artwork


def get_artwork(request):
    artwork_id = request.GET.get("artwork_id")
    if not artwork_id:
        return JsonResponse({"success": False})
    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except ObjectDoesNotExist:
        return JsonResponse({"success": False})
    return JsonResponse({
        "success": True,
        "html": artwork.rendered
    })
