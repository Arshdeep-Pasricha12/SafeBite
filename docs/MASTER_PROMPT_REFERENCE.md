<USER_REQUEST>
# SAFEBITE — COMPLETE PROJECT IMPLEMENTATION MASTER PROMPT

## 1. ROLE AND MISSION

Act as a senior full-stack software engineer, system architect, data engineer, browser-extension developer, QA engineer, and DevOps engineer.

You are working on an existing project called **SafeBite — Restaurant Food Safety Transparency Platform**.

Your task is to inspect the entire existing codebase, understand its current implementation, identify incomplete and mocked features, and transform it into a functional, reliable, testable, and demonstrable application.

Do not start from scratch. Do not replace the existing application with a generic template. Preserve working functionality, existing branding, useful components, and the current architecture wherever reasonable.

You must implement changes in the actual repository, execute builds and tests, resolve failures, and document all remaining limitations.

The final project must provide:

1. A functioning restaurant discovery and food-safety transparency platform.
2. Real, traceable restaurant inspection data wherever legally and technically available.
3. An explainable and testable food-safety assessment engine.
4. A free Chrome browser extension that can display SafeBite safety information alongside supported online food-delivery websites.
5. A companion ordering demonstration that reliably demonstrates the complete safety-notification workflow.
6. Working customer, restaurant-owner, and administrator workflows.
7. Automated testing, including unit, integration, regression, mutation, and end-to-end testing as appropriate.
8. Reproducible development, production-build, Git, and Docker workflows.
9. Genuine screenshots, test reports, and a consolidated PDF documenting the implemented system.

Do not stop after proposing an architecture. Inspect, implement, run, verify, and document.

---

## 2. PRODUCT VISION

Restaurants may continue operating on food-delivery platforms even after official inspections identify hygiene violations or authorities issue notices or enforcement actions.

Customers often cannot conveniently access or understand these inspection histories while deciding where to order food.

SafeBite addresses this problem by making restaurant food-safety information accessible at the point of decision.

A customer should be able to:

- Find a restaurant.
- View its available official inspection history.
- Understand recorded violations and enforcement actions.
- See an explainable food-safety risk assessment.
- Understand whether the data is recent and trustworthy.
- Receive a contextual safety notification while browsing a supported food-delivery website.
- Review the evidence behind the notification before making a decision.

**Core principle:** A restaurant's presence on a delivery platform is not evidence that it is safe. Similarly, missing inspection records are not evidence that a restaurant is unsafe or safe.

SafeBite is an independent information and risk-transparency platform. Its calculated assessments must never be presented as official government certifications.

---

## 3. FIRST: AUDIT THE EXISTING CODEBASE

Before editing files, thoroughly inspect the repository.

Inspect:

- Frontend components, pages, routes, styling, and API clients.
- Backend application structure and API routes.
- Database models, migrations, and existing database contents.
- Authentication and role-based access control.
- Restaurant discovery and inspection-history functionality.
- Safety-score calculations and notification logic.
- Existing sample datasets and data-import scripts.
- Environment variables and configuration.
- Dependency manifests and lockfiles.
- Dockerfiles and Docker Compose configuration.
- Existing tests, test fixtures, scripts, and documentation.
- Git status, branch, and uncommitted changes.

Create:

- `docs/IMPLEMENTATION_AUDIT.md`
- `docs/FEATURE_STATUS.md`
- `docs/TECHNICAL_DECISIONS.md`

Classify every major feature as:

- Implemented and verified.
- Implemented but not verified.
- Partially implemented.
- Mocked or hardcoded.
- Not implemented.
- Blocked by an external dependency.

Trace the actual frontend-to-backend-to-database flow. A page or endpoint existing does not prove that the feature works.

Identify the existing stack and versions before changing dependencies. Run baseline builds and tests where possible.

Preserve the user's existing work. Never delete the database, reset Git history, or overwrite uncommitted changes without an explicit reason and safe recovery plan.

---

## 4. TECHNOLOGY STACK

The existing project is expected to use:

- React, Vite, Tailwind CSS, Axios, and React Router.
- Python, FastAPI, Pydantic, and Uvicorn.
- SQLAlchemy ORM.
- SQLite for local development.
- JWT authentication and password hashing.
- Docker and Docker Compose.

Verify all of these assumptions from the repository.

Use the existing compatible stack. Add or upgrade dependencies only when justified.

Use the following testing technologies where appropriate:

- pytest and FastAPI TestClient for backend tests.
- React Testing Library and the existing frontend test runner for UI tests.
- Playwright for browser-based end-to-end testing.
- A suitable Python mutation-testing tool such as mutmut for critical backend logic.
- Coverage reporting and JUnit XML output where supported.

Use a browser-extension architecture compatible with Chrome Manifest V3.

Use database migrations, preferably Alembic if equivalent migration management does not already exist.

Keep the system modular, maintainable, and compatible with free local development tools.

---

## 5. RESTAURANT DATA: REPLACE MOCK DATA WITH TRACEABLE RECORDS

This is a critical requirement.

The existing application may contain synthetic restaurant records, fake inspection histories, hardcoded safety scores, or placeholder data. Identify these and prevent them from being presented as genuine official records.

### 5.1 Find legitimate data sources

Investigate accessible official sources, prioritizing:

- FSSAI resources and publicly available food-safety information.
- State food-safety departments.
- Municipal and local health department inspection records.
- Official enforcement notices, penalties, suspensions, and closures.
- Government open-data portals.
- Other authorized public inspection datasets.

For Indian restaurants, verify what information is actually available, the geographic coverage, access requirements, update frequency, licensing conditions, and permissible uses.

Do not assume that a comprehensive, freely accessible, real-time FSSAI API exists.

Do not fabricate API endpoints or bypass access controls. Do not scrape websites in violation of their terms.

Prefer official APIs or downloadable public datasets. Where no suitable source exists, implement an adapter that can later accept authorized datasets.

Document each investigated source, including its availability, limitations, retrieval method, and last verification date.

### 5.2 Build a real data-ingestion pipeline

Implement a reusable import system that can:

1. Retrieve or accept an authorized dataset.
2. Validate the file structure and required fields.
3. Normalize restaurant names, addresses, dates, violation classifications, and official statuses.
4. Identify duplicate records.
5. Associate inspections with the correct restaurant branch.
6. Preserve source identifiers and original record references.
7. Record the source URL, publication date, retrieval time, and verification status.
8. Detect ambiguous restaurant matches.
9. Report rejected rows and validation failures.
10. Support repeatable imports without creating duplicate records.
11. Support incremental updates when the source permits them.
12. Produce a detailed import summary.

Use exact official identifiers wherever possible. Never merge restaurant branches solely because their names are similar. Send ambiguous matches for administrator review.

An import should be transactional where appropriate and recover safely from failure.

### 5.3 Required provenance fields

Every inspection record should preserve, where available:

- Source authority.
- Source dataset or document.
- Original source record identifier.
- Inspection date.
- Publication date.
- Date retrieved by SafeBite.
- Last verification timestamp.
- Inspection result.
- Violation details.
- Corrective action.
- Official enforcement status.
- Original source link.
- Verification status.

Clearly distinguish an inspection's date from the date SafeBite imported it.

### 5.4 Data states

Support explicit data states such as:

- Verified source record.
- Partially verified record.
- Unverified record.
- No verified inspection history.
- Stale or overdue information.
- Conflicting information.
- Pending administrative review.

If real records are available only for certain cities or restaurants, show that limitation honestly.

Never generate fake records to achieve a target restaurant count.

Synthetic records may exist only in isolated development/test fixtures or an explicitly labelled demonstration dataset. They must never be presented as official findings.

Create:

- `docs/DATA_SOURCES.md`
- `docs/DATA_IMPORT_GUIDE.md`
- An administrator-facing import interface.
- A command-line import utility.
- An import validation and preview workflow.
- Automated import and data-integrity tests.

If external access is unavailable, implement the complete ingestion framework and demonstrate it with clearly labelled synthetic test fixtures. State exactly which real sources remain unconnected.

---

## 6. RESTAURANT DISCOVERY AND INSPECTION HISTORY

Complete and verify the existing restaurant discovery functionality.

Implement or improve:

- Restaurant browsing with pagination.
- Search by restaurant name.
- Filtering by city, locality, cuisine, risk category, and inspection status.
- Sorting by assessment score, inspection date, and restaurant name.
- Restaurant and branch details.
- Inspection-history timeline.
- Detailed violation descriptions.
- Corrective actions and enforcement status where documented.
- Source attribution and original source links.
- Data-freshness indicators.
- Data-coverage indicators.
- Loading, empty, error, and retry states.
- Responsive desktop and mobile layouts.

Every restaurant branch must have a distinct identity where necessary.

Do not let a restaurant owner overwrite official findings. Owners may request corrections and submit evidence, but an authorized review process must handle changes to official-record mappings.

Use the backend and database for real application functionality. Do not leave major screens powered by hardcoded frontend arrays.

---

## 7. EXPLAINABLE FOOD-SAFETY ASSESSMENT ENGINE

Build a deterministic, configurable, thoroughly tested assessment engine.

### 7.1 Risk factors

Consider available evidence concerning:

- Violation severity.
- Critical versus non-critical findings.
- Recency of inspections.
- Repeated violations.
- Corrective actions.
- Subsequent inspection results.
- Official suspension, closure, or other enforcement actions.
- Data completeness, reliability, and freshness.

Use official definitions and classifications where available. Do not invent legal interpretations or unsupported regulatory meanings.

### 7.2 Scoring policy

Use a normalized score from 0 to 100 only when there is sufficient evidence to justify a meaningful score.

Document:

- The formula.
- Factor weights.
- Thresholds.
- Severity rules.
- Missing-data behavior.
- Stale-data behavior.
- Repeat-violation handling.
- Enforcement-action handling.
- Policy version.

Higher scores may represent lower recorded risk, but the score must never override a serious active official enforcement action.

If the evidence is insufficient, return an explicit insufficient-data status rather than a reassuring score.

### 7.3 Customer-facing labels

Support understandable states such as:

- Elevated concern.
- Caution advised.
- No major recorded concerns in available records.
- Insufficient data.
- Verification overdue.

Each assessment must explain:

- Why the status was assigned.
- Which records influenced the decision.
- Which factors were missing.
- When the information was last updated.
- Where the customer can inspect the original evidence.

Never display a calculated status as an official food-safety certificate.

Store the assessment-policy version used to produce each result, and make calculations reproducible.

### 7.4 Required test cases

Test:

- Score boundaries.
- Critical-violation overrides.
- Repeated violations.
- Recent versus old inspections.
- Missing inspection history.
- Stale data.
- Conflicting records.
- Corrective actions.
- Expired or superseded enforcement actions.
- Multiple branches.
- Unverified records.
- Invalid dates and missing severity information.

---

## 8. FREE CHROME BROWSER EXTENSION

This is the primary integration mechanism for displaying SafeBite information alongside an existing online food-delivery website without relying on paid APIs.

Build a separate browser-extension directory, for example:

`browser-extension/`

Use Chrome Manifest V3.

The extension must communicate with the existing SafeBite backend using an explicitly configured API base URL.

### 8.1 Research before implementing site-specific behavior

Inspect the current delivery websites and determine whether a permitted, technically reliable integration is feasible.

Investigate:

- Available restaurant names and branch identifiers in the visible page.
- Stable page structures and permitted integration mechanisms.
- Relevant website terms and restrictions.
- Browser-extension permission requirements.
- Whether a restaurant detail page can be reliably identified.
- Whether the integration can operate without authenticated API interception.

Prefer the minimum required permissions and supported extension mechanisms.

Do not assume the DOM structure is stable. Do not depend on undocumented private APIs.

Do not scrape authenticated data, steal cookies, intercept credentials, bypass access controls, or inject scripts into payment flows.

If the website prohibits the required behavior, do not implement that behavior. Provide a clearly documented compatible alternative.

### 8.2 Extension functionality

The extension should:

1. Detect when the user is on a supported restaurant listing or restaurant detail page.
2. Extract only the minimum restaurant information needed from permitted visible page content.
3. Normalize the restaurant name and, where possible, location.
4. Query SafeBite for matching restaurants.
5. Show an extension panel, badge, or popup with the result.
6. Display the assessment and the reason for it.
7. Link to the full SafeBite inspection history.
8. Show a clear insufficient-data state when matching fails.
9. Allow the user to refresh the assessment.
10. Handle API errors and network failures gracefully.
11. Avoid sending unnecessary customer information to SafeBite.
12. Avoid collecting or storing full delivery orders or payment information.

The extension must never claim that an order event occurred when it merely detected a restaurant page.

### 8.3 Restaurant matching

Matching must not rely on restaurant name alone when ambiguity exists.

Use available evidence such as:

- Exact provider restaurant identifier, if legitimately available.
- Restaurant name.
- Branch address.
- City and locality.
- Other reliable public identifiers.

If the extension cannot confidently identify the correct branch, show an ambiguous-match warning and ask the user to select the correct SafeBite restaurant.

Never display another branch's inspection findings as if they belong to the selected branch.

### 8.4 Extension notification states

Use messages such as:

**Elevated concern**

"SafeBite found a verified official inspection record reporting [finding] on [date]. Review the evidence before ordering."

**No major recorded concerns**

"No major concerns were recorded in the verified inspection records available through [date]. This does not guarantee current food safety."

**Insufficient data**

"SafeBite could not verify sufficient inspection information for this restaurant. Its food-safety risk cannot currently be assessed."

**Ambiguous match**

"Multiple restaurants may match this listing. Confirm the branch before viewing its inspection history."

All text must be populated dynamically from actual backend responses.

### 8.5 Extension user interface

Create a professional, compact extension popup and, where permitted, a contextual restaurant-page panel.

Display:

- SafeBite branding.
- Restaurant and branch name.
- Assessment status.
- Assessment explanation.
- Latest inspection date.
- Source freshness.
- A link to the complete history.
- A retry or refresh action.
- A clear data-unavailable state.

Do not obscure the delivery website's controls or modify payment and checkout behavior.

### 8.6 Free demonstration

If live delivery websites are inaccessible, incompatible, or prohibit the intended integration, build an extension development/demo mode using a local SafeBite demonstration page.

The demonstration must exercise the actual extension-to-backend request and actual assessment logic.

Clearly label the local integration as a demonstration. Do not claim it is a live Swiggy or Zomato integration.

Document the exact supported site behavior, permissions, installation procedure, limitations, and testing method in:

`docs/BROWSER_EXTENSION.md`

---

## 9. COMPANION ORDERING DEMONSTRATION

Build a small, clearly labelled ordering demonstration inside SafeBite.

This is the guaranteed way to demonstrate the complete safety-checking workflow without external platform access.

Implement:

1. Browse available demo restaurants.
2. Select a restaurant and branch.
3. Open a simulated order or checkout screen.
4. Retrieve the restaurant's current assessment from the backend.
5. Show the assessment before the simulated order is confirmed.
6. Allow the user to inspect the underlying inspection history.
7. Display a warning, a qualified reassuring message, or an insufficient-data message.
8. Allow the user to proceed, cancel, or return to the restaurant details.
9. Record a minimal demonstration event for testing and audit purposes.
10. Clearly identify the workflow as simulated.

Do not imply that an actual order was placed on Swiggy, Zomato, or another external platform.

The companion demonstration must use the same restaurant-matching, inspection-query, and assessment services as the browser extension.

Do not hardcode warning messages or create a separate assessment implementation just for the demo.

---

## 10. DELIVERY PROVIDER ARCHITECTURE

Create an extensible adapter architecture for future authorized delivery-platform integrations.

Investigate documented official integration mechanisms, but do not make the application depend on paid credentials.

Support a common provider interface that can later accommodate:

- Restaurant identifier mapping.
- Authenticated incoming events, where supported.
- Event validation.
- Idempotency.
- Restaurant assessment lookup.
- Notification generation.
- Delivery status and error reporting.

If an authorized provider integration becomes available, implement it through a separate adapter without changing the core assessment engine.

If real provider access is not available, mark the integration as pending approval and retain the functioning browser extension and companion demonstration.

Never fabricate API responses, credentials, webhooks, successful delivery events, or third-party integration status.

Document the exact distinction between:

- A live authorized provider integration.
- Browser-based contextual assessment.
- A simulated demonstration event.

---

## 11. USER ROLES AND WORKFLOWS

Audit and complete the existing role-based application.

### Customer

- Register and log in.
- Browse and search restaurants.
- View inspection histories.
- Read risk assessments and source evidence.
- Access correction/reporting mechanisms.
- View notification history where implemented.
- Manage notification preferences.

### Restaurant owner

- Register and create restaurant listings.
- Edit appropriate business information.
- Manage branches where supported.
- Track listing-approval status.
- Submit supporting evidence.
- Request corrections to inaccurate restaurant or inspection mappings.
- View administrative decisions.

Owners must never be able to independently alter official inspection findings, change the scoring policy, or assign themselves an official safety status.

### Administrator

- Review restaurant applications.
- Approve, reject, or request changes.
- Review ambiguous restaurant matches.
- Review correction requests.
- Import and validate datasets.
- View import history and rejected records.
- Monitor data freshness and source health.
- Review administrative audit logs.
- Reprocess failed imports safely.

Enforce permissions on the backend for every protected operation.

---

## 12. DATABASE AND API COMPLETION

Audit the existing database models and extend them without unnecessary duplication.

Support appropriate entities for:

- Users and roles.
- Restaurants and branches.
- External restaurant identifiers.
- Inspection records.
- Violations.
- Corrective actions.
- Enforcement actions.
- Data sources and source records.
- Import jobs and rejected rows.
- Assessment results and policy versions.
- Listing applications and moderation decisions.
- Correction requests.
- Notifications.
- Integration events.
- Audit logs.

Use appropriate foreign keys, indexes, uniqueness constraints, transactions, and database integrity rules.

Implement safe schema migrations. Do not automatically erase or reseed an existing database on startup.

Keep SQLite suitable for local development and make PostgreSQL configuration possible without claiming untested production compatibility.

Review the existing API before adding new routes.

Implement or complete APIs for:

- Authentication.
- Restaurant search and details.
- Inspection histories.
- Violation details.
- Assessment explanations.
- Data-source status.
- Dataset imports.
- Administrative workflows.
- Correction requests.
- Notifications.
- Restaurant matching.
- Browser-extension requests.
- Simulated order events.

Use validation, pagination, appropriate status codes, clear error responses, and backend authorization.

Keep FastAPI's OpenAPI documentation accurate.

---

## 13. SECURITY AND PRIVACY

Verify and improve:

- Password hashing.
- JWT validation and expiry.
- Role-based authorization.
- Environment-based secrets.
- CORS restrictions.
- Input validation.
- Rate limiting where appropriate.
- Secure webhook validation if implemented.
- Replay protection and event idempotency.
- File upload size and format limits.
- SQL and injection protections through appropriate ORM practices.
- Error handling without secret leakage.
- Audit logging.
- Data minimization.
- Browser-extension permissions.
- Safe handling of restaurant matching and external URLs.

Never commit API keys, passwords, private certificates, or production tokens.

The browser extension must send only the minimum information needed to identify a restaurant. Do not collect customer credentials, payment details, or private delivery-account information.

---

## 14. FRONTEND QUALITY AND USER EXPERIENCE

Inspect every existing page and interactive control.

Complete the relevant screens:

- Landing page.
- Restaurant discovery.
- Search and filtering.
- Restaurant details.
- Inspection history.
- Violation details.
- Risk explanation.
- Source freshness and data coverage.
- Login and registration.
- Restaurant-owner dashboard.
- Administrator dashboard.
- Data-import preview and results.
- Correction requests.
- Notification history.
- Companion ordering demonstration.
- Browser-extension installation and usage guide.

Use a consistent, professional, responsive interface that preserves SafeBite branding.

Ensure that every visible button performs a real action or is explicitly marked unavailable.

Implement loading states, empty states, validation messages, retry behavior, and clear API error handling.

Do not leave major screens populated by fake frontend data.

---

## 15. TESTING STRATEGY

Create:

`docs/TESTING_STRATEGY.md`

Implement and execute the following testing layers as supported by the existing stack.

### 15.1 Unit tests

Use pytest for backend logic and appropriate frontend unit-testing tools.

Cover:

- Restaurant normalization and matching.
- Safety-score calculations.
- Critical finding overrides.
- Repeat-violation logic.
- Stale and missing data.
- Import validation.
- Deduplication.
- Notification generation.
- Role and permission checks.
- Event idempotency.
- Frontend risk labels.
- Extension response handling.

Use boundary-value analysis and equivalence partitioning for scores, dates, risk categories, import fields, and restaurant matching.

### 15.2 Integration tests

Test interactions among:

- API endpoints and database.
- Authentication and protected routes.
- Restaurants and inspection records.
- Import pipelines and persistent data.
- Source metadata and frontend/API responses.
- Assessment logic and notifications.
- Correction requests and administrative review.
- Browser-extension requests and backend matching.
- Simulated order events and generated notifications.

Use an isolated test database. Mock external services only at their boundaries.

### 15.3 Regression tests

Create regression tests for existing features and every discovered bug.

Verify:

- Registration and login.
- Restaurant browsing.
- Search and filtering.
- Inspection timelines.
- Owner listing workflows.
- Administrative approvals.
- Database migrations.
- Existing API contracts.
- Data persistence across application restarts.

Run the complete regression suite after major changes.

### 15.4 Mutation testing

Use a suitable tool such as mutmut, where supported, on critical business logic.

Target:

- Risk thresholds.
- Severity overrides.
- Repeat-violation aggregation.
- Stale-data conditions.
- Authorization checks.
- Notification-generation conditions.

Report killed, surviving, and excluded mutations honestly.

Run mutation testing in an isolated environment and ensure temporary mutations do not remain in the project source.

### 15.5 End-to-end testing

Use Playwright for actual browser workflows.

Test:

1. Customer authentication.
2. Restaurant discovery.
3. Opening a restaurant detail page.
4. Viewing an inspection history.
5. Displaying an elevated-concern assessment.
6. Displaying an insufficient-data state.
7. Submitting a restaurant listing.
8. Administrator review and approval/rejection.
9. Dataset import and validation.
10. Companion ordering demonstration.
11. Generated safety notification.
12. Responsive interface behavior.

Where technically feasible, test the Chrome extension using a local supported test page and the actual SafeBite backend. If full extension automation is not practical, document the limitation and provide a reproducible manual test procedure.

Use isolated, clearly labelled synthetic fixtures for tests.

### 15.6 Test reports and evidence

Produce:

- `docs/TEST_CASES.md`
- `docs/TEST_RESULTS.md`
- Machine-readable JUnit reports where supported.
- Coverage reports.
- Mutation-testing reports where supported.
- Genuine screenshots of test execution and results.

Document test IDs, purpose, input, expected result, actual result, status, and evidence references.

Do not fabricate test results or claim that unexecuted tests passed.

---

## 16. VERSION CONTROL AND REPRODUCIBLE BUILDS

Inspect the existing Git repository and preserve its current state.

Document:

- Branch strategy.
- Feature-branch workflow.
- Meaningful commit conventions.
- Pull-request and review workflow.
- Safe rollback procedures.
- Files excluded from version control.

Use `.gitignore` to exclude environment secrets, caches, generated build output, and temporary test databases while preserving required source data.

Do not force-push, reset history, or delete branches without authorization.

Create or update:

`docs/VERSION_CONTROL.md`

Verify:

- Frontend dependency installation.
- Frontend production build.
- Backend dependency installation.
- Backend startup.
- Health endpoint.
- Database migration and initialization.
- Frontend-to-backend communication.
- Docker image builds.
- Docker Compose startup.
- Service health checks.
- Graceful behavior when external services are unavailable.

Use existing lockfiles and package-manager conventions.

Separate development and production configuration where appropriate.

Document exact commands for setup, migrations, builds, testing, and startup in the README.

Capture genuine screenshots of Git status, branch and commit history, successful builds, running containers, API connectivity, and the application in the browser.

Create:

`docs/BUILD_AND_RUN.md`

---

## 17. DEMONSTRATION WORKFLOW

Create:

`docs/DEMO_GUIDE.md`

The demo must work without paid API credentials.

Demonstrate this sequence:

1. Start the backend, frontend, and database.
2. Open SafeBite.
3. Search for a restaurant.
4. Open its detailed page.
5. View the inspection timeline and source attribution.
6. Explain a recorded violation and the resulting risk assessment.
7. Open a restaurant with insufficient or outdated inspection information.
8. Demonstrate dataset import and validation.
9. Demonstrate the restaurant-owner or administrator workflow.
10. Open the local delivery-order demonstration.
11. Select a restaurant and trigger the safety check.
12. Show the dynamically generated notification.
13. If supported, open the Chrome extension on the local demonstration page and verify the same backend assessment.
14. Explain what is live, what uses real source data, and what is simulated.

Provide local demo credentials only where needed. Never commit production secrets.

The demonstration must not depend on a live Swiggy/Zomato account, paid API, or unapproved partner integration.

---

## 18. SCREENSHOTS OF DEVELOPED FUNCTIONALITIES

Create:

`docs/project-evidence/screenshots/`

Capture screenshots of the actual running application and tools, including:

- Landing page.
- Restaurant discovery.
- Search and filtering.
- Restaurant detail page.
- Inspection history timeline.
- Violation details.
- Assessment explanation.
- Missing or stale data state.
- Authentication and role-based interfaces.
- Owner dashboard.
- Administrator dashboard.
- Data-import preview and results.
- Companion order flow.
- Safety notification.
- Browser-extension popup or panel.
- Extension demonstration page.
- Mobile-responsive view.
- Unit and integration test results.
- Regression-test results.
- Mutation-testing results where supported.
- End-to-end test results.
- Production build.
- Docker Compose services.
- Git branch and commit evidence.

Use reproducible test fixtures where necessary and label them as demonstration data.

Every screenshot must correspond to a real execution. Do not generate fake browser screenshots, fabricated terminal output, or synthetic test-result images.

Create a screenshot index with a short description, the workflow demonstrated, and the data provenance.

---

## 19. TOOLS AND TECHNOLOGIES DOCUMENTATION

Create:

`docs/TOOLS_AND_TECHNOLOGIES.md`

List only technologies actually used in the final implementation.

For each, explain:

- Purpose.
- Where it is used.
- Relevant version.
- Whether it is locally executable.
- Whether it requires credentials.
- Whether it is fully implemented or optional.

Include the frontend, backend, database, ORM, authentication, data providers, browser extension, testing frameworks, mutation-testing tool, browser automation, Docker, Git, and reporting tools as applicable.

Distinguish implemented functionality from planned or blocked integrations.

---

## 20. CONSOLIDATED PROJECT EVIDENCE PDF

Generate a consolidated PDF at:

`docs/project-evidence/SafeBite_Project_Evidence.pdf`

It must include:

1. Project title and brief overview.
2. Implemented functionality and genuine application screenshots.
3. Integration-testing screenshots and results.
4. Regression-testing screenshots and results.
5. Mutation-testing evidence and limitations.
6. Unit and end-to-end test evidence.
7. Version-management and Git screenshots.
8. Frontend/backend build evidence.
9. Docker and system-startup evidence.
10. Tools and technologies used.
11. A short section explaining the browser-extension architecture and companion demo.
12. Actual external integration limitations.
13. Instructions for reproducing the results.

Keep screenshots readable and use concise captions.

Do not add unrelated theoretical material merely to increase document length.

Use an appropriate available PDF-generation library or document-generation capability. After generation, verify that the file exists, opens correctly, contains the expected pages, and includes readable screenshots.

If PDF generation is blocked, preserve the complete organized evidence and document the exact remaining action. Never claim that an ungenerated PDF exists.

---

## 21. REQUIRED DOCUMENTATION

Maintain these files:

- `README.md`
- `docs/IMPLEMENTATION_AUDIT.md`
- `docs/FEATURE_STATUS.md`
- `docs/TECHNICAL_DECISIONS.md`
- `docs/DATA_SOURCES.md`
- `docs/DATA_IMPORT_GUIDE.md`
- `docs/BROWSER_EXTENSION.md`
- `docs/TESTING_STRATEGY.md`
- `docs/TEST_CASES.md`
- `docs/TEST_RESULTS.md`
- `docs/VERSION_CONTROL.md`
- `docs/BUILD_AND_RUN.md`
- `docs/DEMO_GUIDE.md`
- `docs/TOOLS_AND_TECHNOLOGIES.md`

Also generate the consolidated project evidence PDF and organize screenshots and machine-readable test reports.

Do not duplicate the same documentation unnecessarily. Keep references between files consistent.

---

## 22. DEFINITION OF DONE

The project is ready for demonstration only after the following have been verified.

### Application

- [ ] Existing functionality has been audited.
- [ ] Major frontend screens use the actual backend.
- [ ] Restaurant discovery and inspection history work.
- [ ] Data provenance and verification status are visible.
- [ ] Synthetic records are never presented as official findings.
- [ ] Risk assessments are deterministic and explainable.
- [ ] Missing or stale data does not produce unjustified reassurance.
- [ ] Data imports validate and preserve provenance.
- [ ] Administrative workflows work.
- [ ] Backend permissions are tested.
- [ ] Companion ordering demonstration works.
- [ ] Browser extension communicates with the actual backend.
- [ ] Unsupported live integrations are clearly disclosed.
- [ ] Notification content is generated from assessment results.
- [ ] Application errors are handled appropriately.

### Quality and engineering

- [ ] Unit tests have been executed.
- [ ] Integration tests have been executed.
- [ ] Regression tests have been executed.
- [ ] Mutation testing has been executed where supported.
- [ ] End-to-end tests have been executed where feasible.
- [ ] Test failures and limitations are documented.
- [ ] Database migrations preserve existing data.
- [ ] Secrets are not committed.
- [ ] Frontend production build is verified.
- [ ] Backend startup and health check are verified.
- [ ] Docker build and startup are verified where supported.
- [ ] README setup instructions have been tested.

### Evidence and demonstration

- [ ] Genuine functionality screenshots exist.
- [ ] Genuine testing screenshots exist.
- [ ] Version-management evidence exists.
- [ ] Build and Docker evidence exists.
- [ ] Tools and technologies are documented.
- [ ] The demo guide works from a clean local startup.
- [ ] The consolidated PDF has been generated and checked.
- [ ] Remaining external dependencies are documented.

---

## 23. IMPLEMENTATION PRIORITIES

Implement the work in this order.

**Phase 1 — Audit and stabilization**

Inspect the codebase, establish the baseline, identify mock features, and fix existing build and runtime problems.

**Phase 2 — Reliable data and assessment**

Implement inspection-data provenance, import validation, restaurant matching, database integrity, data-freshness handling, and the explainable risk engine.

**Phase 3 — Complete application workflows**

Finish restaurant discovery, detail pages, authentication, administrative review, correction requests, and notification functionality.

**Phase 4 — Browser extension**

Build the Manifest V3 extension, backend integration, restaurant matching, notification UI, local demonstration mode, and documentation. Implement site-specific support only where permitted and technically verified.

**Phase 5 — Companion ordering demo**

Complete the simulated order flow using the same assessment service as the browser extension.

**Phase 6 — Testing and hardening**

Implement and run unit, integration, regression, mutation, and end-to-end tests. Fix discovered defects and record actual results.

**Phase 7 — Build and evidence**

Verify frontend/backend builds, Docker, Git workflow, and startup instructions. Capture screenshots, generate reports, and produce the consolidated PDF.

Do not skip a phase silently. If a requirement depends on external approval, unavailable source data, credentials, or unsupported tooling, finish the independent work and document the precise blocker.

---

## 24. FINAL REPORT

When finished, provide:

- A summary of the original codebase.
- The changes implemented.
- The previously mocked features that were replaced.
- The actual inspection-data sources configured and their coverage.
- The current state of the browser extension.
- The websites and workflows actually tested.
- The distinction between the browser extension, companion demo, and any live provider integration.
- Database migration instructions.
- Exact startup commands.
- Exact commands to run the test suites.
- Actual test, coverage, and mutation results.
- Actual build and Docker verification results.
- Paths to screenshots, reports, and the consolidated PDF.
- Any incomplete items and concrete steps to resolve them.

Do not claim success unless the corresponding feature, test, build, integration, or artifact has actually been verified.

Begin with the existing repository audit and proceed through implementation. Do not stop after planning. Do not ask for information that can be discovered from the codebase. Ask for credentials or approvals only when they are genuinely required for an external integration, and continue implementing everything else independently.
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-10-13T23:35:42+05:30.

The user's current state is as follows:
Other open documents:
- c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\backend\app\core\config.py (LANGUAGE_PYTHON)
- c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\design\architecture\safebite_architecture.drawio (LANGUAGE_UNSPECIFIED)
- c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\frontend\vite.config.js (LANGUAGE_JAVASCRIPT)
- c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\README.md (LANGUAGE_MARKDOWN)
- c:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\docker-compose.yml (LANGUAGE_YAML)
</ADDITIONAL_METADATA>
<USER_SETTINGS_CHANGE>
The user changed setting `Model Selection` from None to Claude Opus 4.6 (Thinking). No need to comment on this change if the user doesn't ask about it. If reporting what model you are, please use a human readable name instead of the exact string.
</USER_SETTINGS_CHANGE>