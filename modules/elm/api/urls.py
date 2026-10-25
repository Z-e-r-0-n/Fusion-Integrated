from django.urls import include, path
from rest_framework.routers import DefaultRouter

from modules.elm.views import (
    LeaveBalanceViewSet,
    LeavePolicyViewSet,
    LeaveRequestViewSet,
    LeaveTypeViewSet,
)

# ELM API URL configuration


router = DefaultRouter()
router.register(r"types", LeaveTypeViewSet)
router.register(r"balances", LeaveBalanceViewSet)
router.register(r"requests", LeaveRequestViewSet)
router.register(r"policies", LeavePolicyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
