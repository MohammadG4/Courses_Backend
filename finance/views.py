from rest_framework import viewsets, permissions
from .models import InstructorRevenue
from .serializers import InstructorRevenueSerializer

class RevenueDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstructorRevenueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show revenue related to the logged-in instructor
        return InstructorRevenue.objects.filter(instructor=self.request.user)