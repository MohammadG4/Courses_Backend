from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class PlatformTier(models.Model):
    """Defines the fee tiers (e.g., 0-5GB = 10% fee)"""
    name = models.CharField(max_length=50)
    max_storage_mb = models.DecimalField(max_digits=10, decimal_places=2)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 10.00 for 10%

    def __str__(self):
        return f"{self.name} ({self.fee_percentage}%)"

class Purchase(models.Model):
    """Records every successful transaction"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} bought {self.course.title}"

class InstructorRevenue(models.Model):
    """The math breakdown for the instructor's dashboard"""
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revenues')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee_percent = models.DecimalField(max_digits=5, decimal_places=2)
    platform_fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Revenue for {self.instructor.email} - ${self.net_amount}"