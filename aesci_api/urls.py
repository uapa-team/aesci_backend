from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)
from rest_framework import routers

from .views import *
from .views import CreateAssignment

router = routers.DefaultRouter()

router.register(r'assignments', AssignmentViewSet, basename="assignment")
router.register(r'assignmentstudents', AssignmentStudentViewSet, basename="assignmentstudent")
router.register(r'courses', CourseViewSet)
router.register(r'groups', GroupCoViewSet, basename="group")
router.register(r'groupstudents', GroupStudentViewSet, basename="groupstudent")
router.register(r'groupteachers', GroupTeacherViewSet, basename="groupteacher")
router.register(r'rubrics', RubricViewSet, basename="rubric")
router.register(r'studentoutcomes', StudentOutcomeViewSet, basename="studentoutcome")
router.register(r'performanceindicators', PerformanceIndicatorViewSet, basename="performanceindicator")
router.register(r'indicatormeasures', IndicatorMeasureViewSet, basename="indicatormeasure")
router.register(r'indicatorgroups', IndicatorGroupViewSet, basename="indicatorgroup")
router.register(r'indicatorassignments', IndicatorAssignmentViewSet, basename="indicatorassignment")
router.register(r'evaluationassignments', EvaluationAssignmentViewSet, basename="evaluationassignment")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('assignmentgroups/', AssignmentGroupView.as_view()),
    path('uploadstudents/', UploadStudentsView.as_view()),
    path('createstudents/', CreateStudentsView.as_view()),
    path('createassignment/', CreateAssignment.CreateAssignmentView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]