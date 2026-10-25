

from conftest import make_session

import pytest
from rest_framework.test import APIClient
from modules.elm.tests.test_submission import seed
from modules.elm.models import LeaveRequest, LeaveBalance

pytestmark = pytest.mark.django_db

def api_as(stub_iam, user_id, permissions):
    stub_iam(make_session(user_id=user_id, kind='staff', modules=('elm',), permissions=permissions))
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token abc')
    return client


def test_anonymous_requests_are_denied():
    response = APIClient().get('/api/v1/elm/requests/')
    assert response.status_code == 401


def test_api_submission_protects_server_fields(stub_iam):
    leave_type, applicant = seed()
    client = api_as(stub_iam, 101, ('elm.leave_requests.view', 'elm.leave_requests.apply'))
    response = client.post('/api/v1/elm/requests/', {
        'leave_type': leave_type.pk,
        'start_date': '2026-11-02',
        'end_date': '2026-11-02',
        'purpose': 'Family',
        'employee': 999,
        'status': 'APPROVED',
        'route': [999]
    }, format='json')
    assert response.status_code == 201, response.data
    assert response.data['employee'] == 101
    assert response.data['status'] == 'PENDING'
    assert response.data['route'] == [201]


def test_api_assigned_authority_approval(stub_iam):
    client, request_id, leave_type = created_request(stub_iam)
    authority_client = api_as(stub_iam, 201, ('elm.leave_requests.view', 'elm.leave_requests.approve'))
    response = authority_client.post(f'/api/v1/elm/requests/{request_id}/decide/', data={'decision': 'APPROVE'}, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 'APPROVED'
    assert LeaveBalance.objects.get(employee=101, leave_type=leave_type, year=2026).balance == 7


def test_api_pending_request_cannot_be_patched(stub_iam):
    client, request_id, leave_type = created_request(stub_iam)
    response = client.patch(f'/api/v1/elm/requests/{request_id}/', data={'status': 'APPROVED'}, format='json')
    assert response.status_code == 405
    assert LeaveRequest.objects.get(pk=request_id).status == 'PENDING'


def created_request(stub_iam):
    leave_type, applicant = seed()
    client = api_as(stub_iam, 101, ('elm.leave_requests.view', 'elm.leave_requests.apply'))
    response = client.post('/api/v1/elm/requests/', {
        'leave_type': leave_type.pk,
        'start_date': '2026-11-02',
        'end_date': '2026-11-02',
        'purpose': 'Family',
        'employee': 999,
        'status': 'APPROVED',
        'route': [999]
    }, format='json')
    assert response.status_code == 201, response.data
    return (client, response.data['id'], leave_type)
