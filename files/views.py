from django.contrib.auth.decorators import login_required
from django_sendfile import sendfile






@login_required
def serve_file(request, file_path):
    return sendfile(request, 'instructions/' + file_path)
