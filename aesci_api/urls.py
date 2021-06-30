from django import urls
from django.db.models import base
from django.urls import include, path

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view())
]