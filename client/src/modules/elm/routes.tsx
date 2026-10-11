// ELM routes
import type { RouteObject } from 'react-router-dom';

export const routes: RouteObject[] = [
  {
    path: 'requests',
    element: <LeaveRequestList />, 
    loader: async () => ({
      data: await useLeaveRequests().then(r => r.data),
      permissions: Principal.has_any_permission('elm.leave_requests.view')
    })
  },
  {
    path: 'balances',
    element: <LeaveBalanceDashboard />, 
    loader: async () => ({
      data: await useLeaveBalances().then(r => r.data),
      permissions: Principal.has_any_permission('elm.leave_balances.view')
    })
  },
  {
    path: 'types',
    element: <LeaveTypeCatalog />, 
    loader: async () => ({
      data: await useLeaveTypes().then(r => r.data),
      permissions: Principal.has_any_permission('elm.leave_types.view')
    })
  },
  {
    path: 'policies',
    element: <LeavePolicyEditor />, 
    loader: async () => ({
      data: await useLeavePolicies().then(r => r.data),
      permissions: Principal.has_any_permission('elm.leave_policies.view')
    })
  }
];