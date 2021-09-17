import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from rest_framework.views import APIView

drive = GoogleDrive(GoogleAuth())
file_path = "file.txt"
# Set up folder ID 
studentFiles = os.environ.get('STUDENT_FOLDER')
# Create File inside folder studentFiles
file1 = drive.CreateFile({'parents': [{'id': studentFiles}]})
file1.SetContentFile(file_path)
file1.Upload()

# class UploadFile(APIView):
#     """Input file, return url to save in Drive"""
#     def post(self, request):