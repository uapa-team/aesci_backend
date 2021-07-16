from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]