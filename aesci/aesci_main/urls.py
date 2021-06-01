from django.urls import path
from . import views

urlpatterns = [
    path('', views.check, name='check'),
    path('login', views.login, name='Get token'),
    path('logout', views.api_logout, name='Destroy token')
]