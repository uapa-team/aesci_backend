from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'assignments', AssignmentViewSet, basename="assignment")
router.register(r'assignmentstudents', AssignmentStudentViewSet, basename="assignment")
router.register(r'courses', CourseViewSet)
router.register(r'groups', GroupCoViewSet, basename="group")
router.register(r'groupstudents', GroupStudentViewSet, basename="groupstudents")
router.register(r'groupteachers', GroupTeacherViewSet, basename="groupteacher")
router.register(r'rubric', RubricViewSet, basename="rubric")
router.register(r'outcomes', StudentOutcomeViewSet, basename="studentoutcome")
router.register(r'indicators', PerformanceIndicatorViewSet, basename="performanceindicator")
router.register(r'measures', IndicatorMeasureViewSet, basename="indicatormeasure")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]