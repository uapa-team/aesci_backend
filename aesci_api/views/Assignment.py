from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.response import Response

from ..models import Assignment, Teacher, GroupStudent, Student, AssignmentStudent, IndicatorGroup, IndicatorAssignment
from ..serializers import AssignmentSerializer

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db import connection

import os

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows teachers to create assignments.
    """
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]    

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

        indicators =''.join(request.data["idIndicators"])
        indicatorsString1 = indicators.replace('[','')
        indicatorsString2 = indicatorsString1.replace(']','')
        indicatorsString3 = indicatorsString2.replace('"','')
        indicatorsString4 = indicatorsString3.replace(' ','')
        indicatorsList = list(indicatorsString4.split(","))

        currentLinks =''.join(request.data["links"])
        linksString1 = currentLinks.replace('[','')
        linksString2 = linksString1.replace(']','')
        linksString3 = linksString2.replace('"','')
        linksString4 = linksString3.replace(' ','')
        currentLinksList = list(linksString4.split(","))
        
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
            file1['title'] = fil.name # Change title of the file.
            file1.SetContentFile(path)
            file1.Upload()
                        
            links.append(file1['alternateLink'])
            # Remove file from storage
            os.remove(tmp_file)


        
        # Get partial value
        partial = kwargs.pop('partial', False)

        # Merge old links with new ones
        # data = instance.link + request.data['link']

	#Don't delete this comments, they'll be used later to delete the file from drive to
#        if instance.link is None:
#            pass
#        else:
#            #Evaluate if a file from assignment has been removed
#            for y in currentLinksList:
#                isTheFileStillThere = False
#                for x in instance.link:
#                    if x == y:
#                        isTheFileStillThere = True                
#                if isTheFileStillThere == False:
#                    print("%s is gonna be deleted", y) 
#                    currentLinksList.remove(y)

        fileData = []
        if instance.link is None:
            fileData = links
        else:
            fileData = currentLinksList + links     

        if links == []:
            data = {"usernameTeacher":teacher,"nameAssignment":name,"numGroup":numGroup,"dateAssignment":date,
            "dateLimitAssignment":dateLimit,"description":description }
            print("xd")
            print(fileData)
        else:
            data = {"usernameTeacher":teacher,"nameAssignment":name,"numGroup":numGroup,"dateAssignment":date,
            "dateLimitAssignment":dateLimit,"description":description ,"link":fileData }
            print("xd")
            print(fileData)
        
        #print(data)
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)
        
		#Now that assginment has been updated, let's update its indicators in indicatorAssignment
        idAssignmentRequest = instance.idAssignment

        indicatorGroup_listCheck = []
        checkPairs = []
        indicatorGroup_list = []		

        #Check if the indicators have changed for the update

        with connection.cursor() as cursor:     

            #Get the indicatorAssignment id  of all tuples in IndicatorAssignment associated with the request assignment                            
            query=f'SELECT "idIndicatorAssignment" FROM aesci_api_indicatorassignment WHERE "assignment_id" = \'{idAssignmentRequest}\''
            cursor.execute(query)
            currentIndicatorAssignments = cursor.fetchall()                        
                               
            #Get the indicatorGroup id with the group and indicators ids
            for i in indicatorsList:
                query2=f'SELECT "idIndicatorGroup" FROM aesci_api_indicatorgroup WHERE "performanceIndicator_id" = \'{i}\' and "numGroup_id" = \'{numGroup}\''
                cursor.execute(query2)
                result2 = cursor.fetchone()
                indicatorGroup_listCheck.append(result2)                                

            #Get the indicatorAssignment id  of tuples in IndicatorAssignment associated with the indicatorGroup in  indicatorGroup_listCheck
            updateIndicatorAssignments = []
            indicatorAssignmentsToCreate = []
            for i in indicatorGroup_listCheck:                
                query3=f'SELECT "idIndicatorAssignment" FROM aesci_api_indicatorassignment WHERE "assignment_id" = \'{idAssignmentRequest}\' and "indicatorGroup_id" = \'{i[0]}\''
                cursor.execute(query3)
                updateIndicatorAssignments.append(cursor.fetchall())                
                #If we didn't find any match is because there is a tuple that need to be created
                #we'll create it after delete the tuples that are not being used
                if updateIndicatorAssignments[-1] == []:
                    indicatorAssignmentsToCreate.append(i[0])

            #Check if elements in currentIndicatorAssignments are in updateIndicatorAssignments            
            for x in currentIndicatorAssignments:
                isCurrentValueThere = False
                for y in updateIndicatorAssignments:
                    #print(y)
                    if y == []:
                        print('this was empty')
                    else:                        
                        if x[0] == y[0][0]:                            
                            isCurrentValueThere = True
                            break
                #If the value wasn't there, then will be deleted
                if isCurrentValueThere==False:                
                    instance = IndicatorAssignment.objects.get(idIndicatorAssignment=x[0])
                    instance.delete()                    
					#EvluationAssignment elements with a fk correspondent to the just deleted instance
					#will be deleted too due to CASCADE
                                    
            #Create the missing tuples assignment, indicatorGroup in IndicatorAssignment
            #Get the assignmetn with the id
            assignmentObject = Assignment.objects.get(idAssignment=idAssignmentRequest)      
            #Create the missing indicatorAssignment          
            for idIndicatorGroup in indicatorAssignmentsToCreate:
                indicatorGroupObject = IndicatorGroup.objects.get(idIndicatorGroup=idIndicatorGroup)
                obj, _ = IndicatorAssignment.objects.get_or_create(indicatorGroup=indicatorGroupObject,assignment=assignmentObject)                

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):                   		
        instance = self.get_object()
        instance.delete()        
            #self.perform_destroy(instance)        
        return Response("Asignatura eliminada exitosamente", status=status.HTTP_200_OK)
