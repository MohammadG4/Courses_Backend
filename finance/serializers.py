from rest_framework import serializers
from .models import InstructorRevenue

class InstructorRevenueSerializer(serializers.ModelSerializer):
    course_title = serializers.ReadOnlyField(source='course.title')
    student_email = serializers.ReadOnlyField(source='purchase.student.email')

    class Meta:
        model = InstructorRevenue
        fields = ['id', 'course_title', 'student_email', 'gross_amount', 'platform_fee_percent', 'net_amount', 'purchase']