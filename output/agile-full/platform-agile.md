# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/agile-full/platform-agile.yaml`
Schema: `/Users/igor/code/yaml-md/samples/agile-full/model-schema.yaml`
Objects Indexed: 13

# Vision: A modern, scalable cash management platform that empowers commercial banking clients across Canada and the US
to self-manage their banking services, users, and approval workflows through a unified digital experience.
The platform eliminates manual processes, reduces operational overhead, and provides clients with real-time
control over their banking relationships while maintaining robust security and compliance standards.
 Payedge is ready to launch a brand-new Receivables service—something we've never offered before. A large commercial
client wants to bring 700 of their business partners (payors) onto the platform by June 2026. This isn't replacing
a manual process—we're creating a new digital service from scratch. And we can't launch without the right platform.

We need three things to succeed: First, an employee portal where our bank staff can efficiently enroll Canadian online
profiles and monitor 700 indirect client relationships. Second, a self-service portal where those 700 payors can
independently manage their users, set their approval rules, and process invoices. Third, a generic approval workflow
engine that supports flexible rules—single approver for small invoices, dual approval for large amounts, configurable
thresholds for each payor.

Today, none of this exists. We're manually managing users from our legacy Express system. We have no portal for
employees or payors. We have no approval engine—every service builds custom approval logic. We're at risk of losing
this client and missing the entire Receivables opportunity.

We're building the platform that makes this possible. Employee portal for efficient bank operations. Self-service
portal for payor independence. Generic approval workflow engine supporting flexible, configurable rules. Near
real-time Express integration so users flow automatically. A three-tier model that turns our client into a platform
for their partners.

This is our moment. By June 2026, we launch a new service with one large client, 700 payors, and 700 approval
workflows. We prove the model works. Then we scale—more clients, more services, corporate structure support, US
expansion. We're not just enabling Payedge. We're building the foundation for the next decade of commercial banking
innovation.
 2025-10-15

Futurestatedescription: A modern, scalable cash management platform that empowers commercial banking clients across Canada and the US
to self-manage their banking services, users, and approval workflows through a unified digital experience.
The platform eliminates manual processes, reduces operational overhead, and provides clients with real-time
control over their banking relationships while maintaining robust security and compliance standards.

Motivationalnarrative: Payedge is ready to launch a brand-new Receivables service—something we've never offered before. A large commercial
client wants to bring 700 of their business partners (payors) onto the platform by June 2026. This isn't replacing
a manual process—we're creating a new digital service from scratch. And we can't launch without the right platform.

We need three things to succeed: First, an employee portal where our bank staff can efficiently enroll Canadian online
profiles and monitor 700 indirect client relationships. Second, a self-service portal where those 700 payors can
independently manage their users, set their approval rules, and process invoices. Third, a generic approval workflow
engine that supports flexible rules—single approver for small invoices, dual approval for large amounts, configurable
thresholds for each payor.

Today, none of this exists. We're manually managing users from our legacy Express system. We have no portal for
employees or payors. We have no approval engine—every service builds custom approval logic. We're at risk of losing
this client and missing the entire Receivables opportunity.

We're building the platform that makes this possible. Employee portal for efficient bank operations. Self-service
portal for payor independence. Generic approval workflow engine supporting flexible, configurable rules. Near
real-time Express integration so users flow automatically. A three-tier model that turns our client into a platform
for their partners.

This is our moment. By June 2026, we launch a new service with one large client, 700 payors, and 700 approval
workflows. We prove the model works. Then we scale—more clients, more services, corporate structure support, US
expansion. We're not just enabling Payedge. We're building the foundation for the next decade of commercial banking
innovation.

Lastupdated: 2025-10-15

## Customerneeds: Enable Payedge to launch new Receivables service by delivering a dual-portal platform: (1) employee portal
for bank staff to manage client enrollment and monitor indirect client relationships; (2) self-service portal
for indirect clients (payors) to independently manage their users, permissions, and approval rules. Generic
approval workflow engine supports flexible invoice approval patterns (single/dual approver, thresholds).


Valueproposition: Enable Payedge to launch new Receivables service by delivering a dual-portal platform: (1) employee portal
for bank staff to manage client enrollment and monitor indirect client relationships; (2) self-service portal
for indirect clients (payors) to independently manage their users, permissions, and approval rules. Generic
approval workflow engine supports flexible invoice approval patterns (single/dual approver, thresholds).


Targetcustomers: Existing Canadian commercial clients (Payedge initiative) requiring online Receivables service enrollment Indirect clients (payors) managed by direct commercial clients, requiring receivable-approval service access Mid-market and large commercial clients with complex organizational structures and approval hierarchies Small business clients needing basic receivables and payment management capabilities Future: US-based commercial clients requiring cross-border receivables capabilities

Problemsbeingsolved: Payedge Receivables initiative cannot launch without platform support for client onboarding and user management No existing receivables service to digitize - this is a new service offering requiring greenfield platform Legacy Express platform (big ball of mud) cannot be modified or extended for new receivables service Express manages users for direct clients but has no concept of indirect clients (payors) No capability to onboard and manage indirect clients (payors) who need to approve invoices Bank employees lack portal to manage online profile enrollment and view indirect client relationships Indirect clients cannot self-manage their users, permissions, and approval rules for invoice processing No generic approval workflow engine - each service implements custom approval logic No configurable approval rules for receivables workflows (single, dual, threshold-based approvals) No unified view for bank employees to monitor three-tier relationship: Bank → Direct Client → Indirect Clients (payors)

## Solutionintent: Build a domain-driven, API-first platform with clear bounded contexts for client management, service enrollment,
user management, and permission/approval orchestration. Leverage event-driven architecture for cross-context
communication and maintain loose coupling with external account systems through adapter patterns.
 Modern microservices architecture with domain-driven design principles, event-driven integration patterns,
and cloud-native deployment. API-first design with dual data integration strategies: near real-time event
streaming (Express user events) and daily batch synchronization (SRF account data). Data engineering
capabilities for managing data replication, transformation, and quality from external systems. Identity
federation with dual providers: A-and-P (direct clients via Express) and Okta (indirect clients). Data
residency and sovereignty considerations for multi-region deployment.


Approach: Build a domain-driven, API-first platform with clear bounded contexts for client management, service enrollment,
user management, and permission/approval orchestration. Leverage event-driven architecture for cross-context
communication and maintain loose coupling with external account systems through adapter patterns.

Technicaldirection: Modern microservices architecture with domain-driven design principles, event-driven integration patterns,
and cloud-native deployment. API-first design with dual data integration strategies: near real-time event
streaming (Express user events) and daily batch synchronization (SRF account data). Data engineering
capabilities for managing data replication, transformation, and quality from external systems. Identity
federation with dual providers: A-and-P (direct clients via Express) and Okta (indirect clients). Data
residency and sovereignty considerations for multi-region deployment.


Keycapabilities: Employee portal for bank staff to manage Canadian online profile enrollment (primary use case for MVP) Employee portal provides unified view into direct clients and their indirect client (payor) relationships Online profile with single primary client (MVP); secondary client support deferred to post-MVP Indirect client (payor) profile creation and management (~700 BUSINESS payors for MVP large client) Indirect client types: BUSINESS ONLY (business name + related persons with roles) - NO individuals in MVP ~1050 indirect client users across 700 business payors (average 1.5 users per business) Dual identity provider strategy: Okta for indirect clients (MVP), A-and-P for direct clients (via Express) Full user lifecycle management for indirect clients in Okta: create, update, activate, deactivate, lock, unlock Platform creates and manages indirect client users in Okta (platform owns identity lifecycle) Anti-corruption layer: consume Express user events (add, update) - Express WILL BE MODIFIED to publish events Near real-time user synchronization from Express via event streaming - unidirectional (Express → Platform) for direct client users Daily batch synchronization from SRF for client-owned accounts (account list, status, updates) Data engineering capabilities for managing data replication from Express and SRF Online profile with site-id linking to Express profile for user replication (direct client users only) Direct client users managed in Express with A-and-P authentication - platform replicates for permission/approval enforcement Indirect client users fully managed in platform with Okta authentication - NEW capability Self-service portal for indirect clients to manage their own users (via platform → Okta integration), permissions, and approval rules Receivable-approval service for indirect clients with self-service invoice approval workflows Generic approval workflow engine: single approver OR multiple approvers (parallel only) Approval workflow lifecycle: submit → pending → approved/rejected/expired Approval rule configuration: approver count (1 or N), amount thresholds (parallel approval when multiple approvers required) Parallel approval: ALL required approvers must approve (no sequential approval in MVP) Three-tier relationship management: Bank → Direct Client (large client) → Indirect Clients (700 business payors) Bank-managed permission and approval rules for large client (MVP); platform stores and enforces rules Account enrollment supporting Canadian DDA accounts for payor invoice payments

Differentiators: Dual-portal architecture: Employee portal for bank operations + self-service portal for indirect clients Dual identity provider strategy: A-and-P (direct clients via Express) + Okta (indirect clients via platform) Full user lifecycle management for indirect clients via Okta integration (platform-owned) Employee portal provides end-to-end visibility: direct client enrollment through indirect client monitoring Three-tier client hierarchy: Direct commercial clients can onboard and monitor their indirect clients (payors) Indirect clients have full self-service capabilities: manage users (via Okta), permissions, approval rules independently Generic approval workflow engine with flexible rules: single/dual approver, sequential/parallel, amount thresholds Approval workflow supports receivable-approval service for indirect clients (invoice approval) Flexible client identification: SRF for direct clients, IND for indirect clients (person or business) Platform enables new business model: clients can offer receivables services to their business partners Future: Corporate structure support via secondary client linking (post-MVP) Future: Migrate direct client users to Okta when Express is decommissioned

## Boundaries

Inscope: MVP: Employee portal for bank staff to manage Canadian online profile enrollment MVP: Employee portal view into direct client + indirect client (payor) relationships and profiles MVP: Onboard ONE large Canadian commercial client to online Receivables service via employee portal MVP: Onboard ~700 indirect clients (payors - BUSINESS ONLY, no individual persons) for the large Receivables client MVP: ~1050 indirect client users (average 1.5 users per indirect client business) MVP: Online profile with single primary client (no secondary client support in MVP) MVP: Receivable-approval service for indirect clients with self-service invoice approval workflows MVP: Generic approval workflow engine for invoice approval by indirect clients MVP: Configurable approval rules: single approver, multiple approvers (parallel approval only) MVP: Approval thresholds (amount-based) determine single vs multiple approver requirements MVP: Approval workflow states: pending, approved, rejected, expired MVP: Parallel approval only - all required approvers must approve (no sequential approval in MVP) MVP: Okta identity provider for indirect client user authentication (NOT A-and-P) MVP: Full user lifecycle management for indirect clients: create, update, activate, deactivate, lock, unlock MVP: Platform creates and manages indirect client users in Okta (platform owns lifecycle) MVP: Near real-time user replication from legacy Express platform (add/update user events) for DIRECT client users MVP: Express platform will be modified to publish user events (add, update) MVP: Daily batch synchronization from SRF for accounts owned by client (account list, status) MVP: Online profile with site-id link to Express profile for user synchronization (direct clients only) MVP: Bank-managed permission and approval rules for the large client (not client self-service) Client profile management (online profiles for direct clients, indirect profiles for payors) Indirect client profile creation (BUSINESS ONLY with related persons: signing-officer, administrator, director) User lifecycle management for both direct and indirect client users (~1050 indirect users) Future: Individual person indirect clients (deferred to post-MVP) Self-service capabilities for indirect clients: manage their own users, permissions, and approval rules Self-service portal for indirect clients (payors) separate from employee portal Account enrollment supporting Canadian DDA accounts (for payor invoice payments) Integration with Okta for indirect client user authentication and lifecycle management (MVP) Integration with A-and-P identity provider for direct client users (via Express - existing) Integration with legacy Express platform for near real-time user event synchronization (direct client users only) Integration with SRF for direct client data (primary client only in MVP), support for IND for indirect clients Geographic coverage: Canada (MVP), with architecture supporting future US and UK expansion Note: No existing receivables service to migrate - this is new service launch Future: Secondary client linking for complex corporate structures (head office/subsidiary, holding/child) Future: Account enrollment from multiple clients (primary + secondary) Future: Self-service enrollment for direct clients (post-MVP) Future: Migrate direct client users from A-and-P to Okta (post-MVP, when Express is decommissioned) Future: Additional cash management services (BTR, Interac Send, other online services)

Outofscope: Core banking functionality (account opening, transaction processing) Payment processing and execution (platform manages enrollment only) Credit decisioning and underwriting Fraud detection and anti-money laundering (AML) processing Customer Relationship Management (CRM) functionality Product catalog management (services are externally defined) Billing and invoicing for banking services Document management and archival

Constraints: Express platform (legacy) will require modification to publish user events (add, update) Express already has self-serve user management - cannot change or replace this functionality (only add event publishing) Must replicate users from Express to platform via event streaming (add/update user events only) SRF integration limited to daily batch synchronization for account data (no real-time API available) Must integrate with existing Canadian banking platform (SRF) and Capital Markets platform (GID) Must support existing identity provider (A-and-P) before migrating to Okta Data sovereignty requirements for client data in Canada vs. US Regulatory compliance requirements differ by jurisdiction (Canada vs. US states) Must coexist with legacy cash management systems during transition period Limited control over account system APIs and data quality Account data updates via daily batch feeds (low velocity), not real-time

Assumptions: MVP: Bank employee portal sufficient for onboarding one large client (no client self-service required) MVP: 700 business payors (NO individuals) with ~1050 users can be onboarded within MVP timeline (June 2026) MVP: All indirect clients are businesses - individual person indirect clients deferred to post-MVP MVP: Parallel approval sufficient - sequential approval not required Okta is available and approved for use in MVP (indirect client authentication) Platform can integrate with Okta APIs for full user lifecycle management Okta supports required MFA and security policies for commercial banking Express platform can be modified to publish user events (add, update) without disrupting existing functionality Express continues to handle user management for direct clients via existing self-serve capabilities Express uses A-and-P for direct client user authentication (existing integration) Platform replicates Express users via near real-time event streaming (add, update events) for direct clients Express site-id is stable and can be used as linking key for user synchronization (direct clients) Platform does NOT manage direct client users - this remains in Express with A-and-P (anti-corruption layer pattern) Platform DOES fully manage indirect client users in Okta - new functionality not in Express Dual identity provider approach is acceptable: A-and-P (direct clients via Express) + Okta (indirect clients via platform) Daily batch feeds from SRF for client-owned accounts are sufficient for account enrollment management SRF provides complete list of accounts owned by client (daily batch, no real-time API) Indirect clients (business payors) have technical capability for self-service portal with Okta authentication Permission and approval models are consistent enough across services to use generic engine Bank-managed permission/approval rules acceptable for MVP; client self-service in future releases

Dependencies: Legacy Express platform - WILL BE MODIFIED to publish user events (add, update) via event streaming Express continues to own user management for direct clients via existing self-serve UI Platform consumes Express user events (add, update) via event streaming - unidirectional (Express → Platform) A-and-P identity provider for direct client user authentication (via Express integration) Okta identity provider for indirect client user authentication and lifecycle management (MVP) Platform must integrate with Okta APIs for user lifecycle operations (create, update, activate, deactivate, lock, unlock) SRF system for Canadian client demographics and daily batch account synchronization (client-owned accounts) SRF provides daily batch feed of accounts owned by client (account list, status, updates) DDA systems (Canadian) for deposit account information (payor payment accounts) ACH/GSAN systems for payment account information (receivables) GID system for Capital Markets client identification (future) Future: Additional account systems (OLB, MTG, RIBS, TSYS) for expanded services

## Strategicalignment

Businessobjectives: Enable Payedge to launch new Receivables service (not replacing existing service - this is greenfield) Provide employee portal for bank staff to efficiently manage online profile enrollment and monitor relationships Unlock new business model: allow commercial clients to extend receivables services to their business partners (payors) Empower indirect clients with self-service portal for user lifecycle, permission, and approval workflow management Adopt Okta for indirect client authentication and lifecycle management (modern identity platform) Provide generic approval workflow engine supporting flexible rules (single/dual approver, thresholds) Reduce operational costs for receivables onboarding through employee portal efficiency and payor self-service Create reusable platform components (dual portals, Okta integration, approval engine, three-tier model) for future services Reduce risk through standardized permission and approval controls for receivables workflows Establish modern identity foundation (Okta) for future migration of direct client users from A-and-P

Strategicthemes: Enable Payedge Receivables initiative (MVP priority) Three-tier client relationship management (Bank → Client → Payors) Self-service empowerment for indirect clients Digital transformation of commercial banking Platform thinking for service innovation and reuse Operational efficiency and cost reduction

Successmetrics:
- Name: MVP launch date Description: Platform ready to support one large Receivables client with 700 payors Target: 20260630 Unit: date
- Name: Direct client onboarding Description: Large Receivables client onboarded via employee portal (bank-managed, not self-service) Target: 1 Current: 0 Unit: clients
- Name: Indirect client (payor) onboarding Description: Number of business payors onboarded for the large Receivables client (NO individuals) Target: 700 Current: 0 Unit: payors
- Name: Okta user creation Description: Number of indirect client users created and managed in Okta by platform Target: 1050 Current: 0 Unit: users
- Name: Approval workflow configuration Description: Number of approval rules configured for indirect clients (single/dual approver, thresholds) Target: 700 Current: 0 Unit: rules
- Name: Invoice approval processing Description: Average time for indirect client to approve invoice via receivable-approval workflow Target: 24 Unit: hours
- Name: Express user sync latency Description: Time from user add/update event in Express to replication in platform (direct clients) Target: 5 Unit: minutes
- Name: Okta user lifecycle latency Description: Time from platform user create/update to Okta provisioning (indirect clients) Target: 2 Unit: seconds
- Name: Platform uptime Description: System availability for client-facing services Target: 99.95 Current: 0 Unit: percent
- Name: Indirect client self-service adoption Description: Percentage of indirect clients managing their own users (via Okta) and approval rules Target: 75 Current: 0 Unit: percent

Outcomes: Payedge successfully launches NEW Receivables service by June 2026 with one large client and 700 business payors Bank employees can efficiently manage online profile enrollment via employee portal Bank employees have unified view into direct clients and their indirect client relationships 700 indirect clients (BUSINESS payors only) successfully onboarded and using self-service portal with Okta authentication 1050 indirect client users created and managed in Okta via platform lifecycle operations (avg 1.5 users per business) 700 approval rules configured (single/dual approver, threshold-based) for receivables workflows Generic approval workflow engine processes invoice approvals with configurable rules Okta integration provides modern, secure identity foundation for indirect clients Near real-time user synchronization from Express platform eliminates manual user management for direct clients Indirect clients independently manage users (via platform → Okta), permissions, and approve invoices Dual identity provider strategy successfully implemented: A-and-P (direct via Express) + Okta (indirect via platform) Platform handles bank-managed permission and approval rules for large client Platform components (dual portals, Okta integration, approval engine, three-tier model) reusable for future services Foundation established for migrating direct client users to Okta (post-MVP), secondary client support, and US expansion

## Decisionframework

Guidingprinciples: Client empowerment first - enable self-service wherever possible Build for reuse - every component should serve multiple services Domain-driven design - clear boundaries, ubiquitous language, loose coupling API-first - all capabilities exposed through well-defined APIs Security and compliance are non-negotiable - build controls into the platform Design for multi-region from day one - not a future retrofit Eventual consistency is acceptable where real-time is not required Anti-corruption layer is mandatory for legacy system integration - protect domain from Express big ball of mud Do not modify legacy systems (Express) - consume via events, translate into domain model Separate concerns: Express owns direct client users, platform owns indirect client users

Tradeoffcriteria: Speed to market vs. perfect architecture - favor iterative delivery with solid foundations Feature richness vs. platform stability - stability wins, add features incrementally Custom solutions vs. generic patterns - always prefer generic, reusable patterns Real-time integration vs. batch - use batch where latency is acceptable to reduce coupling Build vs. buy - buy for identity, build for domain-specific capabilities

Alignmentmechanisms: Bi-weekly product review with stakeholders to validate priorities Architecture review board for technical decisions impacting multiple teams Quarterly roadmap review aligned with business objectives Regular user feedback sessions with commercial banking clients Cross-functional working groups for domain modeling and API design