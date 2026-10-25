from modules.elm.workflows import get_request
from modules.elm.models import LeaveRequest
from rest_framework.exceptions import ValidationError, PermissionDenied

def amendment_base(pk, principal):
    base = get_request(pk)
    if base.employee != principal.user_id:
        raise PermissionDenied("User does not have permission to amend this request.")
    if base.operation != 'LEAVE' or base.status != 'APPROVED':
        raise ValidationError("Request must be of type 'LEAVE' and status 'APPROVED' for amendment.")
    if LeaveRequest.objects.filter(base_request=base, status='PENDING').exists():
        raise ValidationError("Only one pending amendment is allowed for this request.")
    return base


from modules.elm.models import LeaveRequest
from modules.elm.validation import resolve_route

def new_child(base, operation, **overrides):
    attrs = {
        'employee': getattr(base, 'employee'),
        'employee_kind': getattr(base, 'employee_kind'),
        'unit': getattr(base, 'unit'),
        'leave_type': getattr(base, 'leave_type'),
        'start_date': getattr(base, 'start_date'),
        'end_date': getattr(base, 'end_date'),
        'purpose': getattr(base, 'purpose'),
        'half_day': getattr(base, 'half_day'),
        'station_leave': getattr(base, 'station_leave'),
        'station_details': getattr(base, 'station_details'),
        'medical_evidence': getattr(base, 'medical_evidence'),
        'days': getattr(base, 'days'),
        'operation': operation,
        'base_request': base,
        'status': 'PENDING',
        'substitute': None,
        'substitute_status': 'NONE',
        'step': 0,
        'route': resolve_route(base.employee, base.leave_type.type)
    }
    attrs.update(overrides)
    return LeaveRequest.objects.create(**attrs)


from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from modules.elm.workflows import emit, notify_task

@transaction.atomic
def cancel_request(pk, principal):
    base = amendment_base(pk, principal)
    if timezone.localdate() >= base.start_date:
        raise ValidationError("Pre-start cancellation is unavailable.")
    child = new_child(base, 'CANCELLATION')
    emit(child, principal.user_id, 'CANCELLATION_REQUESTED')
    notify_task(child)
    return child


from modules.elm.workflows import get_request, emit
from modules.elm.validation import account
from django.utils import timezone
from rest_framework.exceptions import ValidationError

def approve_cancellation(req, actor, notes=''):
    base = get_request(req.base_request_id)
    if base.status != 'APPROVED' or timezone.localdate() >= base.start_date:
        raise ValidationError("Base request must be approved and start date in the future.")
    if base.amendments.filter(operation='EXTENSION', status='APPROVED').exists():
        raise ValidationError("Cannot cancel a request with approved extensions.")
    row = account(base.employee, base.leave_type, base.start_date.year, base.employee_kind)
    row.balance += base.days
    row.last_updated = timezone.now()
    row.save()
    base.status = 'CANCELLED'
    base.save()
    req.status = 'APPROVED'
    req.approved_at = timezone.now()
    req.save()
    emit(req, actor, 'CANCELLATION_APPROVED', delta=base.days, recipient=req.employee, notes=notes)
    return req
