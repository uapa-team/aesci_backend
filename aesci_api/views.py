from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django_auth_ldap.backend import LDAPBackend

from .models import Course
from .serializers import CourseSerializer

# Create your views here.
class LoginView(APIView):
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
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'username': username,
            'role': user.groups.first().name
            } , status=status.HTTP_200_OK)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permissions = [permissions.IsAdminUser]
