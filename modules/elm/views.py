from modules.elm.workflows import substitute_response, renominate

from modules.elm.workflows import submit, withdraw
from rest_framework.decorators import action

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import LeaveRequest, LeaveBalance, LeaveType, LeavePolicy
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer, LeaveTypeSerializer, LeavePolicySerializer
from fusion_auth.permissions import HasModuleGrant, HasPermission, IsAuthenticatedPrincipal
from rest_framework import status
from datetime import timedelta
import calendar
from django.utils import timezone
from django.db.models import F


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing leave requests.
    """
    http_method_names = ['get', 'post', 'head', 'options']
    queryset = LeaveRequest.objects.all()
    def get_queryset(self):
        from django.db.models import Q
        principal = getattr(self.request, 'principal', None)
        if not principal:
            return LeaveRequest.objects.none()
        queryset = LeaveRequest.objects.all().select_related('leave_type').prefetch_related('events')
        if principal.has_permission('elm.leave_records.manage'):
            return queryset.order_by('-created_at')
        scope = Q(employee=principal.user_id) | Q(substitute=principal.user_id)
        if principal.has_permission('elm.leave_requests.approve'):
            scope |= Q(route__contains=principal.user_id)
        return queryset.filter(scope).order_by('-created_at')
    serializer_class = LeaveRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'withdraw', 'renominate', 'amend']:
            permission_classes = [IsAuthenticatedPrincipal, HasModuleGrant('elm'), HasPermission('elm.leave_requests.apply')]
        elif self.action == 'decide':
            permission_classes = [IsAuthenticatedPrincipal, HasModuleGrant('elm'), HasPermission('elm.leave_requests.approve')]
        else:
            permission_classes = [IsAuthenticatedPrincipal, HasModuleGrant('elm'), HasPermission('elm.leave_requests.view')]
        return [cls() for cls in permission_classes]

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            req = submit(serializer.validated_data, request.principal)
            return Response(self.get_serializer(req).data, status=201)

    def perform_create(self, serializer):
        """
        Set created_at timestamp and associate with employee.
        """
        serializer.save(employee=self.request.principal.user_id)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        obj = self.get_object()
        req = withdraw(obj.pk, request.principal)
        return Response(self.get_serializer(req).data)
    @action(detail=True, methods=['post'])
    def decide(self, request, pk=None):
        from modules.elm.decisions import decide as decide_leave
        obj = self.get_object()
        req = decide_leave(obj.pk, request.principal, request.data.get('decision', ''), request.data.get('notes', ''))
        return Response(self.get_serializer(req).data)
    @action(detail=True, methods=['post'], url_path='substitute-response')
    def substitute_response(self, request, pk=None):
        obj = self.get_object()
        req = substitute_response(obj.pk, request.principal, request.data.get('accept'))
        return Response(self.get_serializer(req).data)
    @action(detail=True, methods=['post'])
    def renominate(self, request, pk=None):
        obj = self.get_object()
        req = renominate(obj.pk, request.principal, request.data.get('substitute'))
        return Response(self.get_serializer(req).data)
    def update(self, request, *args, **kwargs):
        """
        Handle leave request updates with validation.
        """
        instance = self.get_object()
        if instance.status in ['APPROVED', 'CANCELLED']:
            return Response({"error": "Cannot modify approved or cancelled requests"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class LeaveBalanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing leave balances.
    """
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer

    def get_permissions(self):
        """
        Apply role-based access controls.
        """
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), HasModuleGrant("elm")(), HasPermission("elm.leave_balances.manage")()]
        return [permissions.IsAuthenticated(), HasModuleGrant("elm")(), HasPermission("elm.leave_balances.view")()]

    def perform_update(self, serializer):
        """
        Update leave balance with proper accounting.
        """
        instance = self.get_object()
        # Example: Deduct balance for approved leave
        if serializer.validated_data.get('approved', False):
            instance.balance = F('balance') - serializer.validated_data.get('days', 0)
            instance.save(update_fields=['balance'])


class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing leave types.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticatedPrincipal, HasModuleGrant("elm"), HasPermission("elm.leave_types.view"), HasPermission("elm.leave_policies.manage")]


class LeavePolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing leave policies.
    """
    queryset = LeavePolicy.objects.all()
    serializer_class = LeavePolicySerializer
    permission_classes = [IsAuthenticatedPrincipal, HasModuleGrant("elm"), HasPermission("elm.leave_policies.view"), HasPermission("elm.leave_policies.manage")]

    def get_queryset(self):
        """
        Filter policies by leave type if specified.
        """
        queryset = super().get_queryset()
        type_filter = self.request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        return queryset

# Add year-end processing and SLA reminder logic here
