from rest_framework import viewsets, permissions
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # 1. Intercept the Host header (e.g., 'dr-walid.localhost:8000') [cite: 63]
        host = self.request.META.get('HTTP_HOST', '')
        
        # 2. Extract the subdomain
        subdomain = host.split('.')[0] if '.' in host else None
        
        # 3. Dynamically filter the queryset based on the subdomain [cite: 63]
        if subdomain and subdomain != 'localhost' and subdomain != '127':
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