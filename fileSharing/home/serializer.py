import shutil
from zipfile import ZipFile
from rest_framework import serializers
from .models import *
import shutil


class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 100000, allow_empty_file=False,use_url=False)
    )
    folder = serializers.CharField(required=False)

    def zipFiles(self,folder):
        shutil.make_archive(f'files/static/zips/{folder}','zip',f'files/static/{folder}')

    def create(self, validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')
        fileList = []
        for file in files:
            fileObj = Files.objects.create(folder=folder,file=file)
            fileList.append(fileObj)
        self.zipFiles(folder.uuid)
        return {
        "files":[],
        "folder":str(folder.uuid)
        }