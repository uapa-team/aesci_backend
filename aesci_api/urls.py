from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)
from rest_framework import routers
from aesci_api.views.IndicatorMeasure import IndicatorMeasureViewSet
from aesci_api.views.PerformanceIndicator import PerformanceIndicatorViewSet

from aesci_api.views.Rubric import RubricViewSet
from aesci_api.views.StudentOutcome import StudentOutcomeViewSet

from .views import *

router = routers.DefaultRouter()

router.register(r'assignments', AssignmentViewSet, basename="assignment")
router.register(r'courses', CourseViewSet)
router.register(r'rubrics', RubricViewSet)
router.register(r'studentOutcomes', StudentOutcomeViewSet)
router.register(r'performanceIndicators', PerformanceIndicatorViewSet)
router.register(r'indicatorMeasures', IndicatorMeasureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]