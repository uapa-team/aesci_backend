from rest_framework import viewsets, permissions

from ..models import Course, GroupCo
from ..serializers import GroupCoSerializer


class GroupCoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admin to create groups.
    """
    serializer_class = GroupCoSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
            queryset = GroupCo.objects.all()
            query_set = queryset.filter(course=self.request.data['course']).order_by('-numGroup')
            return query_set
