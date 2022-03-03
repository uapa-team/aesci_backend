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

class CreateStudentsView(APIView):
    """Create student's users"""
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        codCareer = request.data['codCareer']

        path = default_storage.save("tmp", ContentFile(file.read()))
        
        # Take columns to use them
        data_frame_students = pandas.read_excel(path, sheet_name='Sheet2', usecols=['COD_PLAN','NOMBRES','APELLIDO1','APELLIDO2','CORREO'], skiprows=[0])

        # Filter by carreer
        data_frame_students = data_frame_students[data_frame_students['COD_PLAN']==int64(codCareer)]
        
        # Remove student duplicates
        data_frame_students = data_frame_students.drop_duplicates(subset='CORREO')

        # Fill out columns 
        data_frame_students['username'] = data_frame_students['CORREO'].apply(lambda x: x.split('@')[0])
        data_frame_students['name'] = data_frame_students['NOMBRES'] + ' ' + data_frame_students['APELLIDO1'] + ' ' + data_frame_students['APELLIDO2']
        # # print(data_frame_students)

        # Take amount of groups in course
        length_student = len(pandas.unique(data_frame_students['username']))
        
        names = data_frame_students['name'].tolist()
        usernames = data_frame_students['username'].tolist()
        emails = data_frame_students['CORREO'].tolist()


        for i in range(length_student):
            obj, _ = Student.objects.get_or_create(username=usernames[i], email=emails[i], name=names[i], departmentCourse=codCareer)

        # Path to temp file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        os.remove(tmp_file)

        return Response( f'{length_student} students created' , status=status.HTTP_200_OK)