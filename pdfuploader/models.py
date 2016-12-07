import uuid
from django.db import models

class StoredFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='pdfuploader1')
    uploaded_dtm = models.DateTimeField(auto_now_add=True)
    size_bytes = models.IntegerField()