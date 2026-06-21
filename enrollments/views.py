from rest_framework import viewsets, permissions
from .models import Enrollment, Progress
from .serializers import EnrollmentSerializer, ProgressSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own enrollments
        return Enrollment.objects.filter(student=self.request.user)

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        if course_id and Enrollment.objects.filter(student=request.user, course_id=course_id).exists():
            from rest_framework.response import Response
            from rest_framework import status
            return Response(
                {"detail": "You are already enrolled in this course."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Auto-assign the logged-in user as the student
        serializer.save(student=self.request.user)

class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Progress.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)