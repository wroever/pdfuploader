import uuid
from django.db import models
from django.conf import settings

class StoredFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='pdfuploader1')
    uploaded_dtm = models.DateTimeField(auto_now_add=True)
    size_bytes = models.IntegerField()

    def get_name(self):
        return str(self.file).lstrip(settings.AWS_STORAGE_BUCKET_NAME)
    name = property(get_name)