# ELM module registry
MODULE = {
    "code": "elm",
    "label": "Employee Leave Management",
    "icon": "CalendarMinus",
    "base_path": "/api/v1/elm",
    "nav_section": "HR",
    "sort_order": 5,
    "status": "active",
}

NAV_ITEMS = [
    {"code": "elm.leave_requests", "label": "Leave Requests",
     "icon": "CalendarMinus", "to": "/api/v1/elm/requests",
     "required_permission": "elm.leave_requests.view",
     "sort_order": 10},
    {"code": "elm.leave_balances", "label": "Leave Balances",
     "icon": "CalendarCheck", "to": "/api/v1/elm/balances",
     "required_permission": "elm.leave_balances.view",
     "sort_order": 20},
    {"code": "elm.leave_types", "label": "Leave Types",
     "icon": "Tag", "to": "/api/v1/elm/types",
     "required_permission": "elm.leave_types.view",
     "sort_order": 30},
    {"code": "elm.leave_policies", "label": "Leave Policies",
     "icon": "FileText", "to": "/api/v1/elm/policies",
     "required_permission": "elm.leave_policies.view",
     "sort_order": 40},
]

SYSTEM_PERMISSIONS = [
    "elm.leave_requests.auto_approve",
    "elm.leave_requests.manual_approve",
    "elm.leave_balances.update",
    "elm.leave_policies.edit",
]