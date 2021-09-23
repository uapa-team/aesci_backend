import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

class UploadView(APIView):
    """Input file, return url to save in Drive"""
    def post(self, request):
        up_file = request.FILES['file']   
        path = default_storage.save("tmp", ContentFile(up_file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("./aesci_api/views/credentials.json")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else: 
            gauth.Authorize()

        drive = GoogleDrive(gauth)

        # Set up folder ID 
        studentFiles = os.environ.get('STUDENT_FOLDER')

        # Create File inside folder studentFiles
        file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
        file1.SetContentFile(path)
        file1.Upload()
        return Response(  status=status.HTTP_200_OK)
