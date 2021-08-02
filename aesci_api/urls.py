from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'assignments', AssignmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'groups', GroupCoViewSet)
router.register(r'groupsrel', GroupRelTeacherStudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]