from ..models import AssignmentStudent, GroupStudent, Student
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
    serializer_class = AssignmentStudentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if Student.objects.filter(username=self.request.query_params["username"]).exists():
        # Return assignments related to Student
            querysetGS = GroupStudent.objects.filter(username=self.request.query_params["username"])
            groupsList = []

            print(querysetGS)
            for element in querysetGS:
                querysetHGS = AssignmentStudent.objects.filter(GroupStudent_id=element.id)
                for elementHGS in querysetHGS:
                    groupsList.append(elementHGS)
            
             # Sort assignment by date
            groupsList.sort(key=lambda x: x.Assignment.dateAssignment, reverse=True)

            return groupsList

        # Return None if student does not have assignments
        return None

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
            
            links.append(file1['id'])
            # Remove file from storage
            os.remove(tmp_file)

        # Get partial value
        partial = kwargs.pop('partial', False)
        
        # Get object with pk
        instance = AssignmentStudent.objects.get(pk=kwargs['pk'])

        # Merge old links with new ones
        # data = instance.link + request.data['link']
        if instance.link is None:
            data = links
        else:
            data = instance.link + links
        data = { "link":data }
        
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response(serializer.data)
