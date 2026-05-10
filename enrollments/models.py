from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments') # 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments') # 
    enrolled_at = models.DateTimeField(auto_now_add=True) # 

    class Meta:
        # Prevent a student from enrolling in the same course twice
        unique_together = ('student', 'course') 

    def __str__(self):
        return f"{self.student.email} enrolled in {self.course.title}"

class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress') # 
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress') # 
    is_completed = models.BooleanField(default=False) # 
    completed_at = models.DateTimeField(auto_now=True) # 

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.email} - {self.lesson.title} - {'Completed' if self.is_completed else 'Pending'}"