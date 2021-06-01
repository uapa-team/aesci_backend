from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.status import *
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend

# Create your views here.
def check(request):
    return HttpResponse({"Ok?": "Ok!"}, status=HTTP_200_OK)

def login(request):
    # pylint: disable=no-member
    #body = json.loads(request.body)
    username = body['username']
    password = body['password']

    if username is None or password is None:
        return HttpResponse({'error': 'Contraseña o usuario vacío o nulo.'},
                            status=HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse({'error': 'Error en ActasDB, usuario sin permisos en la aplicación.'},
                            status=HTTP_403_FORBIDDEN)
    
    user = LDAPBackend().authenticate(request, username=username, password=password)
    if not user:
        return HttpResponse({'error': 'Error en LDAP, contraseña o usuario no válido.'},
                            status=HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return HttpResponse({'token': token.key, 'group': user.groups.first().name},
                        status=HTTP_200_OK)



def api_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return HttpResponse({'successful': 'Logout Success'}, status=HTTP_200_OK)