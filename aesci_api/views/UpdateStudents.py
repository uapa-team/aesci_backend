from numpy import int64
import pandas 
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..models import Student
# Create your views here.

class UpdateStudentsView(APIView):
    """Create student's users"""
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']

        path = default_storage.save("tmp", ContentFile(file.read()))
        
        data_frame_updateStudents = pandas.read_excel(path, sheet_name='Sheet2')

       # Filter columns we need and then turn them into lists
        emails = data_frame_updateStudents['CORREO'].tolist()
        documentsType = data_frame_updateStudents['T_DOCUMENTO'].tolist()
        documents = data_frame_updateStudents['DOCUMENTO'].tolist()
        length_students = len(emails)

		#for each student found in our database update their document and documentType fields
        for i in range(length_students):
            if Student.objects.filter(email=emails[i]).exists():                 
                Student.objects.filter(email=emails[i]).update(document=documents[i], documentType=documentsType[i])                

        # Path to temp file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        os.remove(tmp_file)

        return Response( f'updateSuccess' , status=status.HTTP_200_OK)