from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView
)
from rest_framework import routers
from aesci_api.views.BarChart import BarChartView
from aesci_api.views.BarChartAllCourses import BarChartAllCoursesView
from aesci_api.views.GetCourseOutcomes import GetCourseOutcomesView
from aesci_api.views.IndicatorGroupBySO import IndicatorGroupBySOView

from aesci_api.views.RubricStudentOutcome import RubricStudentOutcomeViewSet

from .views import *
from .views import CreateAssignment
from .views import AssignmentGroupTeacher
from .views import PieChart

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
router.register(r'programs', ProgramViewSet, basename="program")
router.register(r'indicatorgroups', IndicatorGroupViewSet, basename="indicatorgroup")
router.register(r'indicatorassignments', IndicatorAssignmentViewSet, basename="indicatorassignment")
router.register(r'evaluationassignments', EvaluationAssignmentViewSet, basename="evaluationassignment")
router.register(r'rubricstudentoutcomes', RubricStudentOutcomeViewSet, basename="rubricstudentoutcome")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view()),
    path('assignmentgroups/', AssignmentGroupView.as_view()),
    path('assignmentgroupsteacher/', AssignmentGroupTeacher.AssignmentGroupTeacherView.as_view()),
    path('piechart/', PieChart.PieChartView.as_view()),
    path('uploadstudents/', UploadStudentsView.as_view()),
	path('uploadrubrics/', UploadRubricsView.as_view()),
    path('updatestudents/', UpdateStudentsView.as_view()),
    path('createstudents/', CreateStudentsView.as_view()),
    path('indicatorgroupsbyso/', IndicatorGroupBySOView.as_view()),
    path('createassignment/', CreateAssignment.CreateAssignmentView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('barchart/', BarChartView.as_view()),
    path('barchartallcourses/', BarChartAllCoursesView.as_view()),
    path('getcourseoutcomes/', GetCourseOutcomesView.as_view()),
]