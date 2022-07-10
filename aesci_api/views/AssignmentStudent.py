from ..models import AssignmentStudent, GroupStudent, Student, Teacher, Assignment
from ..serializers import AssignmentStudentSerializer

import os
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import F

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
                querysetHGS = AssignmentStudent.objects.filter(GroupStudent_id=element.idGroupStudent)
                for elementHGS in querysetHGS:
                    groupsList.append(elementHGS)
            
             # Sort assignment by date
            groupsList.sort(key=lambda x: x.Assignment.dateAssignment, reverse=True)

            return groupsList

        elif Teacher.objects.filter(username=self.request.query_params["username"]).exists():

            AssignmentObject = Assignment.objects.get(idAssignment=self.request.query_params["assignment"])
            
            querysetAS = AssignmentStudent.objects.filter(Assignment=AssignmentObject)
            print(querysetAS)
            assignmentsList = []
            #assignmentsList.append(AssignmentObject)
            
            for element in querysetAS:
                assignmentsList.append(element)
                #assignmentsList.append([element, "True"])
                print(element)
            print(assignmentsList)
            return assignmentsList

        # Return None if student does not have assignments
        return None

    def update(self, request, *args, **kwargs):
        files = request.FILES.getlist('file')
        links = []

        # Get object with pk
        instance = AssignmentStudent.objects.get(pk=kwargs['pk'])
        currentLinks =''.join(request.data["links"])
        linksString1 = currentLinks.replace('[','')
        linksString2 = linksString1.replace(']','')
        linksString3 = linksString2.replace('"','')
        linksString4 = linksString3.replace(' ','')
        currentLinksList = list(linksString4.split(","))

        if (instance.link is None) or len(instance.link)<=8:

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

                linkPlusFileName = file1['alternateLink'] + ';' + fil.name

                links.append(linkPlusFileName)
                # Remove file from storage
                os.remove(tmp_file)

            # Get partial value
            partial = kwargs.pop('partial', False)


            # Merge old links with new ones
            # data = instance.link + request.data['link']
            if instance.link is None:
                data = links
            else:
                if currentLinksList == ['']:                
                    data = links
                else:                
                    data = currentLinksList + links 
            data = { "link":data }
        
            # Set up serializer
            serializer = self.get_serializer(instance, data, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Execute serializer
            self.perform_update(serializer)

            return Response(serializer.data)
        else:
            return Response({"Error": "Limite excedido"}, status=status.HTTP_401_UNAUTHORIZED)
