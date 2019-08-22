
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from art.models import Artwork, Video
from ui.views import stream_video_url


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


def get_artwork_modal(request):
    artwork_id = request.GET.get("artwork_id")
    if not artwork_id:
        return JsonResponse({"success": False})
    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except ObjectDoesNotExist:
        return JsonResponse({"success": False})
    return JsonResponse({
        "success": True,
        "html": render_to_string("art/modal.html", context={"artwork": artwork, "user": request.user})
    })


def delete_artwork(request):
    artwork_id = request.POST.get("artwork_id")
    if not artwork_id:
        return JsonResponse({"success": False})
    try:
        artwork = Artwork.objects.get(id=artwork_id)
    except ObjectDoesNotExist:
        return JsonResponse({"success": False})
    if not request.user:
        return JsonResponse({"success": False})
    if not request.user.is_superuser:
        return JsonResponse({"success": False})
    artwork.delete()
    return JsonResponse({"success": True})


def stream_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return stream_video_url(request, video.file.path)

