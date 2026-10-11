// Module registry
export const MODULE_REGISTRY = [
  // ...existing modules
  {
    name: 'elm',
    routes: '/elm/*',
    permissions: ['elm.leave_requests.view', 'elm.leave_balances.view', 'elm.leave_types.view', 'elm.leave_policies.view'],
    import: () => import('../modules/elm/routes')
  },
  // ...placement module (ensure it remains unchanged)
];