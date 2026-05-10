from django.contrib import admin

from .models import PlatformTier, Purchase, InstructorRevenue

admin.site.register(PlatformTier)
admin.site.register(Purchase)
admin.site.register(InstructorRevenue)

# Register your models here.
