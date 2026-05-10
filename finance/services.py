# finance/services.py
from django.db.models import Sum
from .models import PlatformTier, InstructorRevenue, Purchase
from courses.models import Lesson

def calculate_instructor_revenue(purchase):
    instructor = purchase.course.instructor
    
    # 1. Calculate total storage used by this instructor
    total_storage = Lesson.objects.filter(
        module__course__instructor=instructor
    ).aggregate(total=Sum('file_size_mb'))['total'] or 0

    # 2. Find the correct tier
    tier = PlatformTier.objects.filter(
        max_storage_mb__gte=total_storage
    ).order_by('max_storage_mb').first()
    
    # Fallback to the highest tier if usage exceeds all tiers
    if not tier:
        tier = PlatformTier.objects.order_by('-max_storage_mb').first()

    fee_percent = tier.fee_percentage if tier else 10.00 # Default 10%
    
    # 3. Math
    fee_amount = (purchase.amount_paid * fee_percent) / 100
    net_amount = purchase.amount_paid - fee_amount

    # 4. Save the record
    return InstructorRevenue.objects.create(
        instructor=instructor,
        course=purchase.course,
        purchase=purchase,
        gross_amount=purchase.amount_paid,
        platform_fee_percent=fee_percent,
        platform_fee_amount=fee_amount,
        net_amount=net_amount
    )