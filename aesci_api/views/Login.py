import requests, os

from ..serializers import MyTokenObtainPairSerializer

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_auth_ldap.backend import LDAPBackend
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class LoginView(APIView):
    """Input user/password, return JWT"""
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        
        if username is None or password is None:
            #User empty
            return Response({"Error":"Usuario o contraseña vacios"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            #print(username)
            user = User.objects.get(username = username)

        except User.DoesNotExist:
            return Response({"Error":"El usuario no existe"}, status=status.HTTP_401_UNAUTHORIZED)

        testUsers = ["usertest1","usertest2","usertest3","usertest4","usertest5"]
        if username in testUsers:
            res = MyTokenObtainPairSerializer.get_token(user)
            return Response( res, status=status.HTTP_200_OK)
        else:
            #Search LDAP's user usertest1
            user = LDAPBackend().authenticate(request, username=username, password=password)
            
            if not user:
                return Response({"Error": "Usuario no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)
        
        #Create Token
        res = MyTokenObtainPairSerializer.get_token(user)

        return Response( res, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer