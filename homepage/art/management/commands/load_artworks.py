from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from os import listdir
from os.path import isfile, join

from art.models import Artwork
from homepage.settings import BASE_DIR


def load_artworks():
    files_dir = BASE_DIR + "/.." + "/files"
    for file in [f for f in listdir(files_dir) if isfile(join(files_dir, f))]:
        with open(files_dir + "/" + file, "rb") as f:
            Artwork.objects.create(file=SimpleUploadedFile(
                name=file,
                content=f.read()
            ))


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_artworks()
