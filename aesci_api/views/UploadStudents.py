import pandas 
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from ..models import GroupCo, GroupStudent, Student
# Create your views here.

class UploadStudentsView(APIView):
    """Create relations between groups and students"""
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        cod_asignatura = request.data['codAsignatura']
        groups = [[]]

        path = default_storage.save("tmp.xlsx", ContentFile(file.read()))
        
        # Take columns to use them
        data_frame_courses = pandas.read_excel(path, engine='openpyxl',sheet_name='Sheet2', usecols=['COD_ASIGNATURA','ASIGNATURA','GRUPO_ASIGNATURA','CORREO'], skiprows=[0])
        
        # Filter by course
        df_course_filtered = data_frame_courses[data_frame_courses['COD_ASIGNATURA']==str(cod_asignatura)]
        print(df_course_filtered)

        # Split email to username
        df_course_filtered['CORREO'] = df_course_filtered['CORREO'].apply(lambda x: x.split('@')[0])
        print(df_course_filtered)

        # Take amount of groups in course
        length_group = len(pandas.unique(df_course_filtered['GRUPO_ASIGNATURA']))
        
        for i in range(1,length_group+1):
            df_group_filtered = df_course_filtered[df_course_filtered['GRUPO_ASIGNATURA']==str(i)]
            groups.insert(i,df_group_filtered['CORREO'].tolist())
        
        for i in range(1,length_group+1):
            id_course = GroupCo.objects.filter(course=cod_asignatura).filter(numGroup=i)
            # id_course = GroupCo.objects.filter(course=cod_asignatura).filter(numGroup=i).values('id')
            for group in id_course:
                num_group = group.id    
                num_group_filtered = GroupCo.objects.get(id =num_group)
            for student in groups[i]:
                print(student)
                student_filtered = Student.objects.get(username=student)
                GroupStudent.objects.create(numGroup=num_group_filtered, username=student_filtered)

        # Path to temp file
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        os.remove(tmp_file)

        return Response( cod_asignatura, status=status.HTTP_200_OK)