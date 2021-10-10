from rest_framework import viewsets, permissions
from rest_framework.response import Response

from ..models import AssignmentStudent
from ..serializers import AssignmentStudentSerializer


class AssignmentStudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows student to update urls on assignments.
    """
    queryset = AssignmentStudent.objects.all()
    serializer_class = AssignmentStudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Get partial value
        partial = kwargs.pop('partial', False)
        
        # Get object with pk
        instance = self.get_object()

        # Merge old links with new ones
        data = instance.link + request.data['link']
        data = { "link":data}
        
        # Set up serializer
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Execute serializer
        self.perform_update(serializer)

        return Response(serializer.data)
