from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment, Teacher, GroupStudent, Student, AssignmentStudent
from ..serializers import AssignmentSerializer

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import os

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to create assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace', 'delete',]

    def get_queryset(self, pk=None):
        if Teacher.objects.filter(username=self.request.query_params["username"]).exists():
            # Return assignments related to Teacher
            return Assignment.objects.filter(usernameTeacher=self.request.query_params["username"])
        return Assignment.objects.all() 

    def update(self, request, *args, **kwargs):

        # Get object with pk
        instance = self.get_object()

        #print(request.data["nameAssignment"])

        name = request.data["nameAssignment"]
        date = request.data["dateAssignment"]
        dateLimit = request.data["dateLimitAssignment"]
        description = request.data["description"]
        numGroup = request.data["numGroup_id"]
        teacher = request.data["usernameTeacher_id"]
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
            studentFiles = os.environ.get('ASSIGNMENT_FOLDER')
            # Path to temp file
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            # Create File inside folder studentFiles
            file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
            file1.SetContentFile(path)
            file1.Upload()
            
            #print(file1['id'])
            links.append(file1['id'])
            # Remove file from storage
            os.remove(tmp_file)


        
        # Get partial value
        partial = kwargs.pop('partial', False)
        

        # Merge old links with new ones
        # data = instance.link + request.data['link']

        if instance.link is None:
            fileData = links
        else:
            fileData = instance.link + links

        if links == []:
            data = {"usernameTeacher":teacher,"nameAssignment":name,"numGroup":numGroup,"dateAssignment":date,
            "dateLimitAssignment":dateLimit,"description":description }
        else:
            data = {"usernameTeacher":teacher,"nameAssignment":name,"numGroup":numGroup,"dateAssignment":date,
            "dateLimitAssignment":dateLimit,"description":description ,"link":fileData }
        
        #print(data)
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        print("Hola")
        
#        try:
#            instance = self.get_object()
#            instance.delete()
#            self.perform_destroy(instance)
#        except Http404:
#            pass
#        return Response(status=status.HTTP_204_NO_CONTENT)
