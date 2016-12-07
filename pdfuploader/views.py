from django.template.response import TemplateResponse
from django.contrib import messages
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage

from models import *
import logging

logger = logging.getLogger('django')

def index(request, extra_context=None):
    return TemplateResponse(request, "index.html")

def upload(request, extra_context=None):

    if request.method == "POST":
        file = StoredFile(file=request.FILES['file'],
                          size_bytes=request.FILES['file'].size)
        try:
            file.save()
            key = default_storage.bucket.get_key(file.file)
            url = key.generate_url(3600) # Generate a public URL expiring in 1 hour
        except Exception as e:
            logger.error("Failed to complete file upload:\n" + str(e))
            return HttpResponse("Unable to complete upload.", status=500)
        return JsonResponse({ "name": file.name,
                              "public_url": url,
                              "size": file.size_bytes },
                            status=201 )

def document(request, id):

    if request.method == "GET":
        try:
            file = StoredFile.objects.get(id=id)
        except StoredFile.DoesNotExist:
            return redirect(reverse('index'))

        filename = file.name
        response = HttpResponse(file.file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response