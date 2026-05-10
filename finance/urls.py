from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RevenueDashboardViewSet

router = DefaultRouter()
router.register(r'finance/dashboard/revenue', RevenueDashboardViewSet, basename='revenue')

urlpatterns = [
    path('', include(router.urls)),
]