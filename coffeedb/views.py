from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse, Http404
from django.core.files.storage import default_storage


@staff_member_required
def protected_media(request, path):
    if not default_storage.exists(path):
        raise Http404
    file = default_storage.open(path)
    filename = path.split('/')[-1]
    response = StreamingHttpResponse(file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
