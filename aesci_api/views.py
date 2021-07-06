import requests, os

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_auth_ldap.backend import LDAPBackend

from .models import Course
from .serializers import CourseSerializer

# Create your views here.

def get_token(request):
    """get a user with JWT auth"""
    jwt_obj = JWTAuthentication()
    header = jwt_obj.get_header(request)
    return jwt_obj.get_raw_token(header)

class LoginView(APIView):
    """Input user/password, return JWT"""
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        if username is None or password is None:
            #User empty
            return Response({"Error":"Usuario o contraseña vacios"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({"Error":"El usuario no existe"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #search LDAP's user
        user = LDAPBackend().authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"Error": "Usuario no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #Create Token
        res = requests.post(f'{os.environ.get("URL_API")}token/', request.data)
        payload = res.json()  
        payload['username'] = user.username
        payload['role'] = user.groups.first().name

        return Response( payload, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAdminUser]
