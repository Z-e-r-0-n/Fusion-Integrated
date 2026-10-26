# Employee Leave Management: behavior and verification

ELM integrates with Fusion's module registry, authentication, permissions, directory cache, HTTP client and application shell. The implementation remains partial; the verification below covers selected workflows rather than complete specification conformance.

## Implemented behavior

- Request ownership, status, route and charged days are assigned on the server. Pending requests are immutable through ordinary PATCH/DELETE operations.
- CL/SCL working-day counting, CL half-days, published RH dates and externally sourced vacation dates are validated. Requests are currently restricted to one calendar year.
- Substitute consent gates authority decisions. Only the current assigned authority can process a request; an intermediate negative recommendation still proceeds to the final authority.
- Final approval deducts balance once. Pending withdrawal terminates the workflow without a deduction.
- Pre-start cancellation creates a separate review request; rejection preserves the original leave, and approval refunds it.
- EL/COL/VL extensions charge only the additional period after approval. Resumption review records the actual return date and adjusts the balance for an early or late return without inventing a generic leave-closure transition.
- Employees see their own balances. Administrator corrections require a reason and evidence reference and record an audit delta.
- Hierarchy changes require configuration permission and record audit events. Holiday/RH calendar replacement validates the complete payload before atomically activating the replacement; ELM cannot publish academic vacation data.
- The request screen supports application, assigned decisions, consent, withdrawal and history. Balance/category/policy views use actual API fields. Hierarchy/calendar maintenance currently uses APIs.

## API entry points

All paths below are relative to `/api/v1/elm/` and require Fusion authentication and the ELM module grant.

| Path | Action |
| --- | --- |
| `requests/` | List visible requests; POST a new application |
| `requests/{id}/decide/` | POST `decision` and optional `notes` |
| `requests/{id}/withdraw/` | POST to withdraw a pending owned request |
| `requests/{id}/substitute-response/` | POST boolean `accept` as the nominated employee |
| `requests/{id}/renominate/` | POST `substitute` after declined consent |
| `requests/{id}/amend/` | POST `operation`: CANCELLATION, EXTENSION or RESUMPTION; extension needs `end_date`, resumption needs `actual_return_date` and `notes` |
| `balances/{id}/adjust/` | POST `balance`, `reason`, `evidence` with balance-management permission |
| `routes/` | Administrator hierarchy configuration |
| `calendar/publish/` | POST `year`, `kind` (CLOSED/RH), a complete `dates` array and `source` |
| `types/`, `policies/` | Read catalogues; maintain configuration with policy-management permission |

Decision values are APPROVE/REJECT at the final authority, RECOMMEND/NOT_RECOMMEND at the first intermediate authority, and FORWARD at later intermediate steps. Permission alone does not grant access to someone else's assigned decision. Substitute consent must already be complete.

Apply migrations and synchronize the permission manifest using the project's standard management commands before configuring categories, hierarchy and calendars. Employee and authority IDs refer to Fusion's directory projection. Calendar publication supports an empty date list to intentionally clear the selected year's selected holiday kind.

## Verification

- Backend regression suite: 412 passing tests, including 32 ELM cases.
- Frontend suite: 42 passing tests, including seven ELM request-screen tests.
- Production frontend compilation/build, Django checks, migration-state checks, permission manifest and lint are checked separately.
- An isolated migration smoke check inserts a 13-character category after migration 0002, applies the remaining ELM migrations and confirms the value survives. The temporary database is removed afterwards.
- OpenAPI is regenerated from the current code. Explicit action-payload contracts above supplement the generated schema.

Tests use isolated PostgreSQL data and a stubbed IAM boundary. Existing installed dependencies were reused. A fresh lockfile install, live IAM login and full browser end-to-end workflow have not been verified.

## Remaining work

Annual credit/carry/conversion processing, offline-sanction synchronization, SLA scheduling/escalation and external attendance delivery remain incomplete. Task/history events are persisted locally; they do not establish external notification or attendance delivery. The YearEndRun table is scaffolding rather than an operational annual-processing job.

The administrative frontend, complete requirement/role coverage, cross-year applications, full action-schema annotations, concurrency/load testing and broader deployment verification remain open. Directory lookups still access the directory projection directly rather than consistently using its public contracts. Existing legacy data needs reconciliation before deployment, especially duplicate balance/configuration rows and older requests without computed workflow fields. A passing test suite does not establish deployment readiness.
