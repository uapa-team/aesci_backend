from ..models import AssignmentStudent
from ..serializers import AssignmentStudentSerializer

import os
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class AssignmentStudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows student to update urls on assignments.
    """
    queryset = AssignmentStudent.objects.all()
    serializer_class = AssignmentStudentSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        links = []

        for fil in files:
            path = default_storage.save("tmp", ContentFile(fil.read()))

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
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # Create File inside folder studentFiles
            file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
            file1.SetContentFile(path)
            file1.Upload()
            
            print(file1['id'])
            links.append(file1['id'])
            # Remove file from storage
            os.remove(tmp_file)

        # Get partial value
        partial = kwargs.pop('partial', False)
        
        # Get object with pk
        instance = self.get_object()

        # Merge old links with new ones
        # data = instance.link + request.data['link']
        data = instance.link + links
        data = { "link":data }
        
        print(data)
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response(serializer.data)
