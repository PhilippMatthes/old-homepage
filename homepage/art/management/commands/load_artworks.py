from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from os import listdir
from os.path import isfile, join

from art.models import Artwork, Video
from homepage.settings import BASE_DIR


def load_artworks():
    files_dir = BASE_DIR + "/.." + "/files"
    files = [f for f in listdir(files_dir) if isfile(join(files_dir, f))]
    for file in files:
        is_thumbnail = file.endswith(".jpg") and file.replace(".jpg", ".mp4") in files
        if is_thumbnail:
            continue
        if file.endswith("mp4"):
            thumbnail = file.replace(".mp4", ".jpg")
            with open(files_dir + "/" + thumbnail, "rb") as t:
                with open(files_dir + "/" + file, "rb") as f:
                    Video.objects.create(
                        file=SimpleUploadedFile(
                            name=file,
                            content=f.read(),
                        ),
                        thumbnail=SimpleUploadedFile(
                            name=thumbnail,
                            content=t.read(),
                        )
                    )
            continue
        with open(files_dir + "/" + file, "rb") as f:
            Artwork.objects.create(file=SimpleUploadedFile(
                name=file,
                content=f.read()
            ))


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_artworks()
