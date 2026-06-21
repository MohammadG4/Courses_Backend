from rest_framework import viewsets, permissions
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from .permissions import IsInstructorOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        # 1. Admin sees everything
        if user.is_authenticated and getattr(user, 'role', '') == 'ADMIN':
            return Course.objects.all()

        # 2. Instructor sees only their own courses
        if user.is_authenticated and getattr(user, 'role', '') == 'INSTRUCTOR':
            return Course.objects.filter(instructor=user)

        # 3. Students (or unauthenticated) see published courses based on subdomain
        host = self.request.META.get('HTTP_HOST', '')
        subdomain = host.split('.')[0] if '.' in host else None
        
        if subdomain and subdomain not in ['localhost', '127', 'www']:
            return Course.objects.filter(instructor__subdomain=subdomain, is_published=True)
        
        # Fallback if no specific subdomain is accessed
        return Course.objects.none()

    def perform_create(self, serializer):
        # Automatically set the instructor to the logged-in user making the request
        serializer.save(instructor=self.request.user)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]