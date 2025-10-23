# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ddd-part/bff-example.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ddd-part/strategic-ddd.schema.yaml`
Objects Indexed: 7

<a id="bff_web"></a>
# Bff Scope: WebAppBFF

Id: bff_web
Name: WebAppBFF
Client Type: web
Serves Interface: Web application SPA (Single Page Application) for desktop and tablet browsers
Owned By Team: Web Frontend Team
Team Type: frontend
Architecture Layer: integration
Pattern Type: bff

Aggregates From Contexts: bc_user_management bc_order_management bc_product_catalog

Upstream Dependencies: api_gateway

Calls: application_service bounded_context_api

## Provides

### Endpoints

| Endpoint | Path | Method | Description |
| -------- | ---- | ------ | ----------- |
| Aggregates user profile + recent orders for dashboard view | /api/web/users/dashboard | GET | Aggregates user profile + recent orders for dashboard view |
| Product details + user's purchase history for this product | /api/web/products/detail/{productId} | GET | Product details + user's purchase history for this product |
| Complete checkout summary with user, cart items, and pricing | /api/web/checkout/summary | GET | Complete checkout summary with user, cart items, and pricing |

### Transformations

| Transformation | From Context | Transformation Type | Description |
| -------------- | ------------ | ------------------- | ----------- |
| Convert UserId value object to string, Status enum to human-readable label | bc_user_management | format_conversion | Convert UserId value object to string, Status enum to human-readable label |
| Enrich order summary with user display name from user context | bc_order_management | data_enrichment | Enrich order summary with user display name from user context |
| Flatten product hierarchy for simplified web display | bc_product_catalog | denormalization | Flatten product hierarchy for simplified web display |

Client Optimizations: Field selection: Only include fields needed by web UI Image size reduction: Return web-optimized image URLs Pagination: Default 20 items per page for desktop list views Caching headers: Set appropriate cache TTLs for static data

### Data Aggregation: parallel Dashboard endpoint makes parallel calls to:
1. UserQueries.getUserSummary(userId) → User profile
2. OrderQueries.listRecentOrders(userId) → Recent orders
Then combines results into single DashboardDTO response


| Strategy | Example |
| -------- | ------- |
| parallel | Dashboard endpoint makes parallel calls to:
1. UserQueries.getUserSummary(userId) → User profile
2. OrderQueries.listRecentOrders(userId) → Recent orders
Then combines results into single DashboardDTO response
 |

## Responsibilities: true true true

| Data Aggregation | Client Specific Orchestration | Presentation Logic | Format Translation | Business Logic | Transaction Management | Direct Persistence |
| ---------------- | ----------------------------- | ------------------ | ------------------ | -------------- | ---------------------- | ------------------ |
| true | true | true | true | false | false | false |

## Anti Patterns: false false false

| Shared Business Logic | Generic Cross Cutting Concerns | Direct Database Access | Serving Multiple Client Types |
| --------------------- | ------------------------------ | ---------------------- | ----------------------------- |
| false | false | false | false |