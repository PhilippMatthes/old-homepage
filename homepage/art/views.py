import mimetypes
import os
import re
from wsgiref.util import FileWrapper

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import StreamingHttpResponse

from art.models import Artwork, Video


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


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(video.file.path)
    content_type, encoding = mimetypes.guess_type(video.file.path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(video.file.path, 'rb'),
                                                      offset=first_byte,
                                                      length=length),
                                     status=206,
                                     content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(video.file.path, 'rb')),
                                     content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

