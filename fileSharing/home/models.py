from django.db import models
import uuid
import os
# Create your models here.

def getPath(obj,file):
    return os.path.join(str(obj.folder.uuid),file)

class Folder(models.Model):
    uuid = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateField(auto_now=True)

class Files(models.Model):
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    file = models.FileField(upload_to=getPath)
    created_at = models.DateField(auto_now=True)

