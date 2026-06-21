from rest_framework import serializers
from .models import Course, Module, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'file_size_mb': {'required': False},
            'order': {'required': False},
        }

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'order', 'lessons', 'course']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    instructor = serializers.ReadOnlyField(source='instructor.email')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'is_published', 'cover_image', 'instructor', 'modules']