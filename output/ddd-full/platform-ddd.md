# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ddd-full/platform-ddd.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ddd-full/ddd-schema.yaml`
Objects Indexed: 70

<a id="sys_cash_mgmt_platform"></a>
# System: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Description: 
Version: 0.2.0

## Domains

| Domain | Type | Strategic Importance | Description |
| ------ | ---- | -------------------- | ----------- |
| [Service Profiles](#dom_service_profiles) | core | critical | Core domain managing SERVICE PROFILES for clients (not clients themselves - client data from SRF/GID). Three profile types: servicing, online (direct client), indirect (payor). Service enrollment managed through application services (stand-alone like BTR, online like Receivables, indirect like receivable-approval). Indirect client management is part of this domain since indirect clients exist only to serve indirect service profiles.
 |
| [User Management](#dom_user_management) | core | critical | User lifecycle for direct clients (Express sync) and indirect clients (Okta managed). Identity provider integration with dual providers. Permission and approval policy management (AWS IAM-inspired). Policies define WHO can DO WHAT on WHICH resources.
 |
| [Approval Workflows](#dom_approval_workflows) | core | critical | Generic approval workflow execution engine. Executes approval workflows based on policies defined in User Management domain. Parallel approval only (MVP). Reusable across all services. Critical for business operations requiring approval controls.
 |
| [External Data](#dom_external_data) | supporting | important | Provides SERVING LAYER (read-only) for Service Profile domain to access external data: client demographics (SRF), account data (SRF), and user data (Express). Consumes gold copy data created by data engineering pipelines. Serving layer abstracts external systems from domain model.
 |

## Bounded Contexts

| Bounded Context | Domain Ref | Description | Bounded Context Ref | Use Case | Transaction Boundary |
| --------------- | ---------- | ----------- | ------------------- | -------- | -------------------- |
| [Service Profile Management](#bc_service_profile_management) | dom_service_profiles | Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).
 |  |  |  |
| [Indirect Client Management](#bc_indirect_client_management) | dom_service_profiles | Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.
 |  |  |  |
| [ServicingProfileApplicationService](#svc_app_servicing_profile) |  | Orchestrates servicing profile lifecycle: create, add/modify services, enroll accounts, suspend. Coordinates with validation service, repositories, and event publishing.
 | bc_service_profile_management | Manage servicing profiles and service enrollment | true |
| [OnlineProfileApplicationService](#svc_app_online_profile) |  | Orchestrates online profile lifecycle: create with Express linking, enroll online services, onboard indirect clients, manage accounts. Bank-managed via employee portal (MVP).
 | bc_service_profile_management | Manage online profiles and indirect client onboarding | true |
| [IndirectProfileApplicationService](#svc_app_indirect_profile) |  | Orchestrates indirect profile lifecycle: create, enroll indirect services, link payment accounts, manage self-service permission/approval policies.
 | bc_service_profile_management | Manage indirect profiles and self-service policy configuration | true |
| [Users](#bc_users) | dom_user_management | Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.
 |  |  |  |
| [Identity Integration](#bc_identity_integration) | dom_user_management | Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.
 |  |  |  |
| [Policy](#bc_policy) | dom_user_management | Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.
 |  |  |  |
| [Approval Engine](#bc_approval_engine) | dom_approval_workflows | Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.
 |  |  |  |
| [Account Data Sync](#bc_account_data_sync) |  | Data engineering ETL infrastructure. Daily batch from SRF for client-owned accounts. Creates GOLD COPY of account data consumed by serving layer. Detects new/closed accounts. Data quality checks. Infrastructure supporting External Data domain.
 |  |  |  |
| [External Data Serving](#bc_external_data_serving) | dom_external_data | SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.
 |  |  |  |
| [Client Data Service](#svc_app_client_data) |  | Application service providing read-only access to client demographics gold copy from SRF. Service Profile domain consumes this for profile creation and client validation.
 | bc_external_data_serving |  |  |
| [Account Data Service](#svc_app_account_data) |  | Application service providing read-only access to account data gold copy from SRF daily batch. Service Profile domain consumes this for account enrollment and validation.
 | bc_external_data_serving |  |  |
| [User Data Service](#svc_app_user_data) |  | Application service providing read-only access to user data gold copy from Express events. User Management domain (bc_users) consumes this for direct client user synchronization and Policy domain (bc_policy) consumes for permission/approval enforcement.
 | bc_external_data_serving |  |  |

## Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="dom_service_profiles"></a>
## Domain: Service Profiles

Id: dom_service_profiles
Name: Service Profiles
Type: core
Description: Core domain managing SERVICE PROFILES for clients (not clients themselves - client data from SRF/GID). Three profile types: servicing, online (direct client), indirect (payor). Service enrollment managed through application services (stand-alone like BTR, online like Receivables, indirect like receivable-approval). Indirect client management is part of this domain since indirect clients exist only to serve indirect service profiles.

Strategic Importance: critical
Investment Strategy: 
Notes: 

### Bounded Contexts

| Bounded Context | Domain Ref | Description |
| --------------- | ---------- | ----------- |
| [Service Profile Management](#bc_service_profile_management) | dom_service_profiles | Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).
 |
| [Indirect Client Management](#bc_indirect_client_management) | dom_service_profiles | Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.
 |

<a id="bc_service_profile_management"></a>
### Bounded Context: Service Profile Management

Id: bc_service_profile_management
Name: Service Profile Management
Domain Ref: [Service Profiles](#dom_service_profiles)
Description: Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Application Services

| Application Service | Bounded Context Ref | Use Case | Description | Transaction Boundary |
| ------------------- | ------------------- | -------- | ----------- | -------------------- |
| [ServicingProfileApplicationService](#svc_app_servicing_profile) | bc_service_profile_management | Manage servicing profiles and service enrollment | Orchestrates servicing profile lifecycle: create, add/modify services, enroll accounts, suspend. Coordinates with validation service, repositories, and event publishing.
 | true |
| [OnlineProfileApplicationService](#svc_app_online_profile) | bc_service_profile_management | Manage online profiles and indirect client onboarding | Orchestrates online profile lifecycle: create with Express linking, enroll online services, onboard indirect clients, manage accounts. Bank-managed via employee portal (MVP).
 | true |
| [IndirectProfileApplicationService](#svc_app_indirect_profile) | bc_service_profile_management | Manage indirect profiles and self-service policy configuration | Orchestrates indirect profile lifecycle: create, enroll indirect services, link payment accounts, manage self-service permission/approval policies.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_service_profile_management"></a>
#### Aggregate: Service Profile Management

Id: bc_service_profile_management
Name: Service Profile Management
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_service_profile_management"></a>
##### Entity: Service Profile Management

Id: bc_service_profile_management
Name: Service Profile Management
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_service_profile_management"></a>
###### Value Object: Service Profile Management

Id: bc_service_profile_management
Name: Service Profile Management
Bounded Context Ref: 
Description: Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_service_profile_management"></a>
##### Repository: Service Profile Management

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_service_profile_management | Service Profile Management |  |  |  |  |

<a id="bc_service_profile_management"></a>
##### Domain Event: Service Profile Management

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_service_profile_management | Service Profile Management |  |  | Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).
 |  |  |

<a id="bc_service_profile_management"></a>
#### Domain Service: Service Profile Management

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_service_profile_management | Service Profile Management |  | Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).
 |  |

<a id="svc_app_servicing_profile"></a>
#### Application Service: ServicingProfileApplicationService

Id: svc_app_servicing_profile
Name: ServicingProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Use Case: Manage servicing profiles and service enrollment
Transaction Boundary: true
Authorization: 

##### Orchestrates

| Orchestrate | Type | Ref |
| ----------- | ---- | --- |
| aggregate agg_servicing_profile | aggregate | agg_servicing_profile |
| domain_service svc_dom_profile_validation | domain_service | svc_dom_profile_validation |
| repository repo_servicing_profile | repository | repo_servicing_profile |

<a id="svc_app_servicing_profile"></a>
##### Domain Event: ServicingProfileApplicationService

Id: svc_app_servicing_profile
Name: ServicingProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Description: Orchestrates servicing profile lifecycle: create, add/modify services, enroll accounts, suspend. Coordinates with validation service, repositories, and event publishing.

Immutable: 
Timestamp Included: 

<a id="svc_app_servicing_profile"></a>
###### Aggregate: ServicingProfileApplicationService

Id: svc_app_servicing_profile
Name: ServicingProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_servicing_profile"></a>
###### Entity: ServicingProfileApplicationService

Id: svc_app_servicing_profile
Name: ServicingProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_servicing_profile"></a>
###### Value Object: ServicingProfileApplicationService

Id: svc_app_servicing_profile
Name: ServicingProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Description: Orchestrates servicing profile lifecycle: create, add/modify services, enroll accounts, suspend. Coordinates with validation service, repositories, and event publishing.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_servicing_profile"></a>
###### Repository: ServicingProfileApplicationService

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_servicing_profile | ServicingProfileApplicationService | [Service Profile Management](#bc_service_profile_management) |  |  |  |

<a id="svc_app_online_profile"></a>
#### Application Service: OnlineProfileApplicationService

Id: svc_app_online_profile
Name: OnlineProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Use Case: Manage online profiles and indirect client onboarding
Transaction Boundary: true
Authorization: 

##### Orchestrates

| Orchestrate | Type | Ref |
| ----------- | ---- | --- |
| aggregate agg_online_profile | aggregate | agg_online_profile |
| aggregate agg_indirect_client | aggregate | agg_indirect_client |
| domain_service svc_dom_profile_validation | domain_service | svc_dom_profile_validation |
| domain_service svc_dom_sequence_generator | domain_service | svc_dom_sequence_generator |
| repository repo_online_profile | repository | repo_online_profile |
| repository repo_indirect_client | repository | repo_indirect_client |

<a id="svc_app_online_profile"></a>
##### Domain Event: OnlineProfileApplicationService

Id: svc_app_online_profile
Name: OnlineProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Description: Orchestrates online profile lifecycle: create with Express linking, enroll online services, onboard indirect clients, manage accounts. Bank-managed via employee portal (MVP).

Immutable: 
Timestamp Included: 

<a id="svc_app_online_profile"></a>
###### Aggregate: OnlineProfileApplicationService

Id: svc_app_online_profile
Name: OnlineProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_online_profile"></a>
###### Entity: OnlineProfileApplicationService

Id: svc_app_online_profile
Name: OnlineProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_online_profile"></a>
###### Value Object: OnlineProfileApplicationService

Id: svc_app_online_profile
Name: OnlineProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Description: Orchestrates online profile lifecycle: create with Express linking, enroll online services, onboard indirect clients, manage accounts. Bank-managed via employee portal (MVP).

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_online_profile"></a>
###### Repository: OnlineProfileApplicationService

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_online_profile | OnlineProfileApplicationService | [Service Profile Management](#bc_service_profile_management) |  |  |  |

<a id="svc_app_indirect_profile"></a>
#### Application Service: IndirectProfileApplicationService

Id: svc_app_indirect_profile
Name: IndirectProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Use Case: Manage indirect profiles and self-service policy configuration
Transaction Boundary: true
Authorization: 

##### Orchestrates

| Orchestrate | Type | Ref |
| ----------- | ---- | --- |
| aggregate agg_indirect_profile | aggregate | agg_indirect_profile |
| repository repo_indirect_profile | repository | repo_indirect_profile |
| repository repo_indirect_client | repository | repo_indirect_client |

<a id="svc_app_indirect_profile"></a>
##### Domain Event: IndirectProfileApplicationService

Id: svc_app_indirect_profile
Name: IndirectProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Description: Orchestrates indirect profile lifecycle: create, enroll indirect services, link payment accounts, manage self-service permission/approval policies.

Immutable: 
Timestamp Included: 

<a id="svc_app_indirect_profile"></a>
###### Aggregate: IndirectProfileApplicationService

Id: svc_app_indirect_profile
Name: IndirectProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_indirect_profile"></a>
###### Entity: IndirectProfileApplicationService

Id: svc_app_indirect_profile
Name: IndirectProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_indirect_profile"></a>
###### Value Object: IndirectProfileApplicationService

Id: svc_app_indirect_profile
Name: IndirectProfileApplicationService
Bounded Context Ref: [Service Profile Management](#bc_service_profile_management)
Description: Orchestrates indirect profile lifecycle: create, enroll indirect services, link payment accounts, manage self-service permission/approval policies.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_indirect_profile"></a>
###### Repository: IndirectProfileApplicationService

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_indirect_profile | IndirectProfileApplicationService | [Service Profile Management](#bc_service_profile_management) |  |  |  |

<a id="bc_service_profile_management"></a>
#### Factory: Service Profile Management

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_service_profile_management | Service Profile Management |  |  |  |  |  |

<a id="bc_service_profile_management"></a>
#### Specification: Service Profile Management

Id: bc_service_profile_management
Name: Service Profile Management
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_service_profile_management"></a>
#### Context Mapping: Service Profile Management

Id: bc_service_profile_management
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="bc_indirect_client_management"></a>
### Bounded Context: Indirect Client Management

Id: bc_indirect_client_management
Name: Indirect Client Management
Domain Ref: [Service Profiles](#dom_service_profiles)
Description: Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_indirect_client_management"></a>
#### Aggregate: Indirect Client Management

Id: bc_indirect_client_management
Name: Indirect Client Management
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_indirect_client_management"></a>
##### Entity: Indirect Client Management

Id: bc_indirect_client_management
Name: Indirect Client Management
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_indirect_client_management"></a>
###### Value Object: Indirect Client Management

Id: bc_indirect_client_management
Name: Indirect Client Management
Bounded Context Ref: 
Description: Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_indirect_client_management"></a>
##### Repository: Indirect Client Management

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_indirect_client_management | Indirect Client Management |  |  |  |  |

<a id="bc_indirect_client_management"></a>
##### Domain Event: Indirect Client Management

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_indirect_client_management | Indirect Client Management |  |  | Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.
 |  |  |

<a id="bc_indirect_client_management"></a>
#### Domain Service: Indirect Client Management

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_indirect_client_management | Indirect Client Management |  | Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.
 |  |

<a id="bc_indirect_client_management"></a>
#### Application Service: Indirect Client Management

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| bc_indirect_client_management | Indirect Client Management |  |  |  |  |

<a id="bc_indirect_client_management"></a>
#### Factory: Indirect Client Management

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_indirect_client_management | Indirect Client Management |  |  |  |  |  |

<a id="bc_indirect_client_management"></a>
#### Specification: Indirect Client Management

Id: bc_indirect_client_management
Name: Indirect Client Management
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_indirect_client_management"></a>
#### Context Mapping: Indirect Client Management

Id: bc_indirect_client_management
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="dom_user_management"></a>
## Domain: User Management

Id: dom_user_management
Name: User Management
Type: core
Description: User lifecycle for direct clients (Express sync) and indirect clients (Okta managed). Identity provider integration with dual providers. Permission and approval policy management (AWS IAM-inspired). Policies define WHO can DO WHAT on WHICH resources.

Strategic Importance: critical
Investment Strategy: 
Notes: 

### Bounded Contexts

| Bounded Context | Domain Ref | Description |
| --------------- | ---------- | ----------- |
| [Users](#bc_users) | dom_user_management | Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.
 |
| [Identity Integration](#bc_identity_integration) | dom_user_management | Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.
 |
| [Policy](#bc_policy) | dom_user_management | Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.
 |

<a id="bc_users"></a>
### Bounded Context: Users

Id: bc_users
Name: Users
Domain Ref: [User Management](#dom_user_management)
Description: Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_users"></a>
#### Aggregate: Users

Id: bc_users
Name: Users
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_users"></a>
##### Entity: Users

Id: bc_users
Name: Users
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_users"></a>
###### Value Object: Users

Id: bc_users
Name: Users
Bounded Context Ref: 
Description: Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_users"></a>
##### Repository: Users

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_users | Users |  |  |  |  |

<a id="bc_users"></a>
##### Domain Event: Users

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_users | Users |  |  | Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.
 |  |  |

<a id="bc_users"></a>
#### Domain Service: Users

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_users | Users |  | Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.
 |  |

<a id="bc_users"></a>
#### Application Service: Users

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| bc_users | Users |  |  |  |  |

<a id="bc_users"></a>
#### Factory: Users

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_users | Users |  |  |  |  |  |

<a id="bc_users"></a>
#### Specification: Users

Id: bc_users
Name: Users
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_users"></a>
#### Context Mapping: Users

Id: bc_users
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="bc_identity_integration"></a>
### Bounded Context: Identity Integration

Id: bc_identity_integration
Name: Identity Integration
Domain Ref: [User Management](#dom_user_management)
Description: Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_identity_integration"></a>
#### Aggregate: Identity Integration

Id: bc_identity_integration
Name: Identity Integration
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_identity_integration"></a>
##### Entity: Identity Integration

Id: bc_identity_integration
Name: Identity Integration
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_identity_integration"></a>
###### Value Object: Identity Integration

Id: bc_identity_integration
Name: Identity Integration
Bounded Context Ref: 
Description: Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_identity_integration"></a>
##### Repository: Identity Integration

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_identity_integration | Identity Integration |  |  |  |  |

<a id="bc_identity_integration"></a>
##### Domain Event: Identity Integration

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_identity_integration | Identity Integration |  |  | Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.
 |  |  |

<a id="bc_identity_integration"></a>
#### Domain Service: Identity Integration

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_identity_integration | Identity Integration |  | Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.
 |  |

<a id="bc_identity_integration"></a>
#### Application Service: Identity Integration

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| bc_identity_integration | Identity Integration |  |  |  |  |

<a id="bc_identity_integration"></a>
#### Factory: Identity Integration

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_identity_integration | Identity Integration |  |  |  |  |  |

<a id="bc_identity_integration"></a>
#### Specification: Identity Integration

Id: bc_identity_integration
Name: Identity Integration
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_identity_integration"></a>
#### Context Mapping: Identity Integration

Id: bc_identity_integration
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="bc_policy"></a>
### Bounded Context: Policy

Id: bc_policy
Name: Policy
Domain Ref: [User Management](#dom_user_management)
Description: Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_policy"></a>
#### Aggregate: Policy

Id: bc_policy
Name: Policy
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_policy"></a>
##### Entity: Policy

Id: bc_policy
Name: Policy
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_policy"></a>
###### Value Object: Policy

Id: bc_policy
Name: Policy
Bounded Context Ref: 
Description: Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_policy"></a>
##### Repository: Policy

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_policy | Policy |  |  |  |  |

<a id="bc_policy"></a>
##### Domain Event: Policy

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_policy | Policy |  |  | Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.
 |  |  |

<a id="bc_policy"></a>
#### Domain Service: Policy

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_policy | Policy |  | Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.
 |  |

<a id="bc_policy"></a>
#### Application Service: Policy

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| bc_policy | Policy |  |  |  |  |

<a id="bc_policy"></a>
#### Factory: Policy

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_policy | Policy |  |  |  |  |  |

<a id="bc_policy"></a>
#### Specification: Policy

Id: bc_policy
Name: Policy
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_policy"></a>
#### Context Mapping: Policy

Id: bc_policy
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="dom_approval_workflows"></a>
## Domain: Approval Workflows

Id: dom_approval_workflows
Name: Approval Workflows
Type: core
Description: Generic approval workflow execution engine. Executes approval workflows based on policies defined in User Management domain. Parallel approval only (MVP). Reusable across all services. Critical for business operations requiring approval controls.

Strategic Importance: critical
Investment Strategy: 
Notes: 

### Bounded Contexts

| Bounded Context | Domain Ref | Description |
| --------------- | ---------- | ----------- |
| [Approval Engine](#bc_approval_engine) | dom_approval_workflows | Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.
 |

<a id="bc_approval_engine"></a>
### Bounded Context: Approval Engine

Id: bc_approval_engine
Name: Approval Engine
Domain Ref: [Approval Workflows](#dom_approval_workflows)
Description: Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_approval_engine"></a>
#### Aggregate: Approval Engine

Id: bc_approval_engine
Name: Approval Engine
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_approval_engine"></a>
##### Entity: Approval Engine

Id: bc_approval_engine
Name: Approval Engine
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_approval_engine"></a>
###### Value Object: Approval Engine

Id: bc_approval_engine
Name: Approval Engine
Bounded Context Ref: 
Description: Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_approval_engine"></a>
##### Repository: Approval Engine

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_approval_engine | Approval Engine |  |  |  |  |

<a id="bc_approval_engine"></a>
##### Domain Event: Approval Engine

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_approval_engine | Approval Engine |  |  | Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.
 |  |  |

<a id="bc_approval_engine"></a>
#### Domain Service: Approval Engine

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_approval_engine | Approval Engine |  | Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.
 |  |

<a id="bc_approval_engine"></a>
#### Application Service: Approval Engine

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| bc_approval_engine | Approval Engine |  |  |  |  |

<a id="bc_approval_engine"></a>
#### Factory: Approval Engine

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_approval_engine | Approval Engine |  |  |  |  |  |

<a id="bc_approval_engine"></a>
#### Specification: Approval Engine

Id: bc_approval_engine
Name: Approval Engine
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_approval_engine"></a>
#### Context Mapping: Approval Engine

Id: bc_approval_engine
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="dom_external_data"></a>
## Domain: External Data

Id: dom_external_data
Name: External Data
Type: supporting
Description: Provides SERVING LAYER (read-only) for Service Profile domain to access external data: client demographics (SRF), account data (SRF), and user data (Express). Consumes gold copy data created by data engineering pipelines. Serving layer abstracts external systems from domain model.

Strategic Importance: important
Investment Strategy: 
Notes: 

### Bounded Contexts

| Bounded Context | Domain Ref | Description |
| --------------- | ---------- | ----------- |
| [External Data Serving](#bc_external_data_serving) | dom_external_data | SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.
 |

<a id="bc_external_data_serving"></a>
### Bounded Context: External Data Serving

Id: bc_external_data_serving
Name: External Data Serving
Domain Ref: [External Data](#dom_external_data)
Description: SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.

Ubiquitous Language: 
Team Ownership: 

#### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

#### Application Services

| Application Service | Bounded Context Ref | Description |
| ------------------- | ------------------- | ----------- |
| [Client Data Service](#svc_app_client_data) | bc_external_data_serving | Application service providing read-only access to client demographics gold copy from SRF. Service Profile domain consumes this for profile creation and client validation.
 |
| [Account Data Service](#svc_app_account_data) | bc_external_data_serving | Application service providing read-only access to account data gold copy from SRF daily batch. Service Profile domain consumes this for account enrollment and validation.
 |
| [User Data Service](#svc_app_user_data) | bc_external_data_serving | Application service providing read-only access to user data gold copy from Express events. User Management domain (bc_users) consumes this for direct client user synchronization and Policy domain (bc_policy) consumes for permission/approval enforcement.
 |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="bc_external_data_serving"></a>
#### Aggregate: External Data Serving

Id: bc_external_data_serving
Name: External Data Serving
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

##### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

##### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

##### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

##### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="bc_external_data_serving"></a>
##### Entity: External Data Serving

Id: bc_external_data_serving
Name: External Data Serving
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="bc_external_data_serving"></a>
###### Value Object: External Data Serving

Id: bc_external_data_serving
Name: External Data Serving
Bounded Context Ref: 
Description: SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="bc_external_data_serving"></a>
##### Repository: External Data Serving

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| bc_external_data_serving | External Data Serving |  |  |  |  |

<a id="bc_external_data_serving"></a>
##### Domain Event: External Data Serving

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| bc_external_data_serving | External Data Serving |  |  | SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.
 |  |  |

<a id="bc_external_data_serving"></a>
#### Domain Service: External Data Serving

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| bc_external_data_serving | External Data Serving |  | SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.
 |  |

<a id="svc_app_client_data"></a>
#### Application Service: Client Data Service

Id: svc_app_client_data
Name: Client Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Use Case: 
Transaction Boundary: 
Authorization: 

<a id="svc_app_client_data"></a>
##### Domain Event: Client Data Service

Id: svc_app_client_data
Name: Client Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Description: Application service providing read-only access to client demographics gold copy from SRF. Service Profile domain consumes this for profile creation and client validation.

Immutable: 
Timestamp Included: 

<a id="svc_app_client_data"></a>
###### Aggregate: Client Data Service

Id: svc_app_client_data
Name: Client Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_client_data"></a>
###### Entity: Client Data Service

Id: svc_app_client_data
Name: Client Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_client_data"></a>
###### Value Object: Client Data Service

Id: svc_app_client_data
Name: Client Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Description: Application service providing read-only access to client demographics gold copy from SRF. Service Profile domain consumes this for profile creation and client validation.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_client_data"></a>
###### Repository: Client Data Service

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_client_data | Client Data Service | [External Data Serving](#bc_external_data_serving) |  |  |  |

<a id="svc_app_account_data"></a>
#### Application Service: Account Data Service

Id: svc_app_account_data
Name: Account Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Use Case: 
Transaction Boundary: 
Authorization: 

<a id="svc_app_account_data"></a>
##### Domain Event: Account Data Service

Id: svc_app_account_data
Name: Account Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Description: Application service providing read-only access to account data gold copy from SRF daily batch. Service Profile domain consumes this for account enrollment and validation.

Immutable: 
Timestamp Included: 

<a id="svc_app_account_data"></a>
###### Aggregate: Account Data Service

Id: svc_app_account_data
Name: Account Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_account_data"></a>
###### Entity: Account Data Service

Id: svc_app_account_data
Name: Account Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_account_data"></a>
###### Value Object: Account Data Service

Id: svc_app_account_data
Name: Account Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Description: Application service providing read-only access to account data gold copy from SRF daily batch. Service Profile domain consumes this for account enrollment and validation.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_account_data"></a>
###### Repository: Account Data Service

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_account_data | Account Data Service | [External Data Serving](#bc_external_data_serving) |  |  |  |

<a id="svc_app_user_data"></a>
#### Application Service: User Data Service

Id: svc_app_user_data
Name: User Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Use Case: 
Transaction Boundary: 
Authorization: 

<a id="svc_app_user_data"></a>
##### Domain Event: User Data Service

Id: svc_app_user_data
Name: User Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Description: Application service providing read-only access to user data gold copy from Express events. User Management domain (bc_users) consumes this for direct client user synchronization and Policy domain (bc_policy) consumes for permission/approval enforcement.

Immutable: 
Timestamp Included: 

<a id="svc_app_user_data"></a>
###### Aggregate: User Data Service

Id: svc_app_user_data
Name: User Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

###### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

###### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

###### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="svc_app_user_data"></a>
###### Entity: User Data Service

Id: svc_app_user_data
Name: User Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

###### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="svc_app_user_data"></a>
###### Value Object: User Data Service

Id: svc_app_user_data
Name: User Data Service
Bounded Context Ref: [External Data Serving](#bc_external_data_serving)
Description: Application service providing read-only access to user data gold copy from Express events. User Management domain (bc_users) consumes this for direct client user synchronization and Policy domain (bc_policy) consumes for permission/approval enforcement.

Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="svc_app_user_data"></a>
###### Repository: User Data Service

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| svc_app_user_data | User Data Service | [External Data Serving](#bc_external_data_serving) |  |  |  |

<a id="bc_external_data_serving"></a>
#### Factory: External Data Serving

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| bc_external_data_serving | External Data Serving |  |  |  |  |  |

<a id="bc_external_data_serving"></a>
#### Specification: External Data Serving

Id: bc_external_data_serving
Name: External Data Serving
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_external_data_serving"></a>
#### Context Mapping: External Data Serving

Id: bc_external_data_serving
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators:

<a id="sys_cash_mgmt_platform"></a>
## Bounded Context: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Domain Ref: 
Description: 
Ubiquitous Language: 
Team Ownership: 

### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

### Domain Services

| Domain Service | Bounded Context Ref | Description | Stateless |
| -------------- | ------------------- | ----------- | --------- |
| [ProfileValidationService](#svc_dom_profile_validation) | bc_service_profile_management | Validates profile creation rules across contexts. Checks client existence via External Data serving layer, validates business rules, ensures site-id linking.
 | true |
| [SequenceGeneratorService](#svc_dom_sequence_generator) | bc_service_profile_management | Generates unique sequence numbers within parent scope (e.g., online profile sequence within client, indirect client sequence within client).
 | true |
| [PolicyEvaluatorService](#svc_dom_policy_evaluator) | bc_policy | Evaluates permission and approval policies for authorization decisions. Determines if user has permission and if approval is required.
 | true |

### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

### Context Mappings

| Context Mapping | Upstream Context | Downstream Context | Relationship Type | Description |
| --------------- | ---------------- | ------------------ | ----------------- | ----------- |
| [Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).](#cm_service_profile_to_external_data) | bc_external_data_serving | bc_service_profile_management | customer_supplier | Service Profile Management (downstream) consumes external data from External Data Serving (upstream) for profile creation, account enrollment, and validation. Read-only access to gold copies via three application services: svc_app_client_data (SRF demographics), svc_app_account_data (SRF batch), svc_app_user_data (Express events).
 |
| [Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.](#cm_approval_engine_to_policy) | bc_policy | bc_approval_engine | customer_supplier | Approval Engine (downstream) consumes permission and approval policies from Policy (upstream). Evaluates policies owned by service profiles to determine approval requirements and enforce rules during workflow execution. Policies use users/user groups from bc_users as subjects.
 |
| [Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.](#cm_receivable_approval_to_approval_engine) | bc_service_profile_management | bc_approval_engine | customer_supplier | Service Profile Management (via Receivable-Approval Enrollment application service) triggers invoice approvals via generic Approval Engine. Approval Engine provides reusable workflow execution.
 |
| [Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).](#cm_service_profile_to_indirect_clients) | bc_service_profile_management | bc_indirect_client_management | customer_supplier | Direct client service profile onboards indirect clients. One-to-many (1 profile → 700 indirect clients, MVP).
 |
| [Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.](#cm_identity_integration_to_express) | express_platform | bc_identity_integration | anti_corruption_layer | Express publishes user events. Identity Integration consumes via ACL to protect domain from Express complexity (big ball of mud). Unidirectional: Express → Platform.
 |
| [SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.](#cm_account_sync_to_srf) | srf_system | bc_account_data_sync | anti_corruption_layer | SRF provides daily batch. Account Data Sync consumes via ACL to protect domain from SRF complexity. Creates gold copy.
 |

<a id="sys_cash_mgmt_platform"></a>
### Domain: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Type: 
Description: 
Strategic Importance: 
Investment Strategy: 
Notes: 

#### Bounded Contexts

| Bounded Context | Domain Ref | Description | Bounded Context Ref | Use Case | Transaction Boundary |
| --------------- | ---------- | ----------- | ------------------- | -------- | -------------------- |
| [Service Profile Management](#bc_service_profile_management) | dom_service_profiles | Manages SERVICE PROFILES (not clients). Links to client data (SRF/GID/IND). Three types: servicing, online, indirect. Enrolls services and accounts through application services. Consumes account and client data from serving layers (read-only).
 |  |  |  |
| [Indirect Client Management](#bc_indirect_client_management) | dom_service_profiles | Manages indirect clients (BUSINESS payors only, MVP). Part of Service Profiles domain since indirect clients exist only for indirect service profiles. IND identification, business info, related persons. Self-service user/permission/approval management.
 |  |  |  |
| [ServicingProfileApplicationService](#svc_app_servicing_profile) |  | Orchestrates servicing profile lifecycle: create, add/modify services, enroll accounts, suspend. Coordinates with validation service, repositories, and event publishing.
 | bc_service_profile_management | Manage servicing profiles and service enrollment | true |
| [OnlineProfileApplicationService](#svc_app_online_profile) |  | Orchestrates online profile lifecycle: create with Express linking, enroll online services, onboard indirect clients, manage accounts. Bank-managed via employee portal (MVP).
 | bc_service_profile_management | Manage online profiles and indirect client onboarding | true |
| [IndirectProfileApplicationService](#svc_app_indirect_profile) |  | Orchestrates indirect profile lifecycle: create, enroll indirect services, link payment accounts, manage self-service permission/approval policies.
 | bc_service_profile_management | Manage indirect profiles and self-service policy configuration | true |
| [Users](#bc_users) | dom_user_management | Manages users and user groups. Direct client users (replicated from Express) and indirect client users (managed in Okta). ~1050 indirect users across 700 business payors (MVP). Users and user groups used as subjects in permission/approval policies.
 |  |  |  |
| [Identity Integration](#bc_identity_integration) | dom_user_management | Anti-corruption layer for dual identity providers. Consumes Express user events (add, update) via streaming. Integrates with Okta APIs for indirect client users.
 |  |  |  |
| [Policy](#bc_policy) | dom_user_management | Permission and approval policy management (AWS IAM-inspired). Policies owned by service profiles. Subject (user/user group from bc_users), action (URN), resource (accounts/services). Approval policy adds approver count and thresholds. Defines WHO can DO WHAT on WHICH resources. Policies consumed by Approval Engine for workflow execution.
 |  |  |  |
| [Approval Engine](#bc_approval_engine) | dom_approval_workflows | Generic approval workflow execution engine. Executes workflows based on policies from Permission Management. Parallel approval only (MVP). Single or multiple approvers. Amount-based thresholds. States: pending, approved, rejected, expired. Reusable across all services.
 |  |  |  |
| [Account Data Sync](#bc_account_data_sync) |  | Data engineering ETL infrastructure. Daily batch from SRF for client-owned accounts. Creates GOLD COPY of account data consumed by serving layer. Detects new/closed accounts. Data quality checks. Infrastructure supporting External Data domain.
 |  |  |  |
| [External Data Serving](#bc_external_data_serving) | dom_external_data | SERVING LAYER providing READ-ONLY access to gold copy external data from SRF and Express. Service Profile domain consumes this for profile creation, account enrollment, and user synchronization. Three application services provide specialized access: client demographics, account data, and user data.
 |  |  |  |
| [Client Data Service](#svc_app_client_data) |  | Application service providing read-only access to client demographics gold copy from SRF. Service Profile domain consumes this for profile creation and client validation.
 | bc_external_data_serving |  |  |
| [Account Data Service](#svc_app_account_data) |  | Application service providing read-only access to account data gold copy from SRF daily batch. Service Profile domain consumes this for account enrollment and validation.
 | bc_external_data_serving |  |  |
| [User Data Service](#svc_app_user_data) |  | Application service providing read-only access to user data gold copy from Express events. User Management domain (bc_users) consumes this for direct client user synchronization and Policy domain (bc_policy) consumes for permission/approval enforcement.
 | bc_external_data_serving |  |  |

<a id="sys_cash_mgmt_platform"></a>
### Aggregate: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Bounded Context Ref: 
Root Ref: 
Lifecycle Hooks: 
Size Estimate: 

#### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

#### Value Objects

| Value Object | Bounded Context Ref | Description | Immutable | Is Abstract | Extends |
| ------------ | ------------------- | ----------- | --------- | ----------- | ------- |
| [ClientId](#vo_client_id) | bc_service_profile_management | Client identifier as URN: {system}:{client_number} where system is srf, gid, or ind. Example: srf:12345, gid:G789, ind:IND001
 | true |  |  |
| [ProfileId](#vo_profile_id_base) | bc_service_profile_management | Base class for profile identifiers. All profiles stored as URN for polymorphic handling. Subclasses: ServicingProfileId, OnlineProfileId, IndirectProfileId.
 | true | true |  |
| [ServicingProfileId](#vo_servicing_profile_id) | bc_service_profile_management | Servicing profile identifier: ServicingProfileId(clientId). Stored as URN.
 | true |  | vo_profile_id_base |
| [OnlineProfileId](#vo_online_profile_id) | bc_service_profile_management | Online profile identifier: OnlineProfileId(clientId, sequence). Sequence unique within client. Stored as URN.
 | true |  | vo_profile_id_base |
| [IndirectProfileId](#vo_indirect_profile_id) | bc_service_profile_management | Indirect profile identifier: IndirectProfileId(clientId, indirectClientId). Stored as URN. IndirectClientId has its own sequence within client.
 | true |  | vo_profile_id_base |
| [IndirectClientId](#vo_indirect_client_id) | bc_indirect_client_management | Indirect client identifier: IndirectClientId(clientId, sequence). Sequence unique within client.
 | true |  |  |

Consistency Rules:

Invariants:

On Create:

On Update:

On Delete:

#### Repositories

| Repository | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | ------------------- | ------------- | -------------------- | -------------------- |
| [ServicingProfileRepository](#repo_servicing_profile) | bc_service_profile_management | agg_servicing_profile | SQL (PostgreSQL) | Single table for servicing profile with foreign key to service_enrollments and account_enrollments. Profile ID is derived from client_id (no sequence).
 |
| [OnlineProfileRepository](#repo_online_profile) | bc_service_profile_management | agg_online_profile | SQL (PostgreSQL) | Single table for online profile with composite key (client_id, sequence). Foreign keys to service_enrollments and account_enrollments. Index on site_id for Express linking.
 |
| [IndirectProfileRepository](#repo_indirect_profile) | bc_service_profile_management | agg_indirect_profile | SQL (PostgreSQL) | Single table for indirect profile with composite key (parent_client_id, indirect_client_id).
 |
| [PermissionStatementRepository](#repo_permission_statement) | bc_policy | agg_permission_statement | SQL (PostgreSQL) | Table with indexes on profile_id and subject for policy evaluation queries.
 |
| [ApprovalStatementRepository](#repo_approval_statement) | bc_policy | agg_approval_statement | SQL (PostgreSQL) | Table with indexes on profile_id and action for approval requirement queries.
 |
| [IndirectClientRepository](#repo_indirect_client) | bc_indirect_client_management | agg_indirect_client | SQL (PostgreSQL) | Single table for indirect client with composite key (parent_client_id, sequence). Foreign key to related_persons table.
 |
| [UserRepository](#repo_user) | bc_users | agg_user | SQL (PostgreSQL) | Table with indexes on profile_id and email for user queries.
 |
| [UserGroupRepository](#repo_user_group) | bc_users | agg_user_group | SQL (PostgreSQL) | Table for user groups with join table for user_group_memberships.
 |

#### Domain Events

| Domain Event | Bounded Context Ref | Aggregate Ref | Description |
| ------------ | ------------------- | ------------- | ----------- |
| [PermissionStatementCreated](#evt_permission_statement_created) | bc_policy | agg_permission_statement | Published when a permission statement is created for a service profile. Contains profile_id (owner), subject (user/user group), action URN, resource, and effect (ALLOW/DENY).
 |
| [PermissionStatementUpdated](#evt_permission_statement_updated) | bc_policy | agg_permission_statement | Published when a permission statement is updated. May include changes to subject, action, resource, or effect.
 |
| [PermissionStatementDeleted](#evt_permission_statement_deleted) | bc_policy | agg_permission_statement | Published when a permission statement is deleted. Consumers should revoke cached permissions.
 |
| [ApprovalStatementCreated](#evt_approval_statement_created) | bc_policy | agg_approval_statement | Published when an approval statement is created for a service profile. Extends permission statement with approver count, amount thresholds, and approver list.
 |
| [ApprovalStatementUpdated](#evt_approval_statement_updated) | bc_policy | agg_approval_statement | Published when an approval statement is updated. May include changes to approver count, approvers, or thresholds.
 |
| [ApprovalStatementDeleted](#evt_approval_statement_deleted) | bc_policy | agg_approval_statement | Published when an approval statement is deleted. Consumers should remove approval requirements.
 |
| [ApprovalWorkflowStarted](#evt_approval_workflow_started) | bc_approval_engine |  | Published when an approval workflow is initiated. Contains workflow ID, approval statement reference, requester, resource being approved, and approver list.
 |
| [ApprovalCompleted](#evt_approval_completed) | bc_approval_engine |  | Published when an approval workflow reaches terminal state (approved, rejected, or expired). Contains final workflow state and outcome.
 |

<a id="sys_cash_mgmt_platform"></a>
#### Entity: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Bounded Context Ref: 
Aggregate Ref: 
Is Aggregate Root: 
Identity Field: 
Identity Generation: 

Invariants:

Lifecycle States:

##### Aggregates

| Aggregate | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | ------------------- | -------- | ------------- |
| [ServicingProfile](#agg_servicing_profile) | bc_service_profile_management | ent_servicing_profile | medium |
| [OnlineProfile](#agg_online_profile) | bc_service_profile_management | ent_online_profile | large |
| [IndirectProfile](#agg_indirect_profile) | bc_service_profile_management | ent_indirect_profile | medium |
| [PermissionStatement](#agg_permission_statement) | bc_policy | ent_permission_statement | small |
| [ApprovalStatement](#agg_approval_statement) | bc_policy | ent_approval_statement | small |
| [IndirectClient](#agg_indirect_client) | bc_indirect_client_management | ent_indirect_client | small |
| [User](#agg_user) | bc_users | ent_user | small |
| [UserGroup](#agg_user_group) | bc_users | ent_user_group | small |

<a id="sys_cash_mgmt_platform"></a>
##### Value Object: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Bounded Context Ref: 
Description: 
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [ServicingProfile](#ent_servicing_profile) | bc_service_profile_management | agg_servicing_profile | true | profile_id | derived |
| [OnlineProfile](#ent_online_profile) | bc_service_profile_management | agg_online_profile | true | profile_id | derived |
| [IndirectProfile](#ent_indirect_profile) | bc_service_profile_management | agg_indirect_profile | true | profile_id | derived |
| [ServiceEnrollment](#ent_service_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [AccountEnrollment](#ent_account_enrollment) | bc_service_profile_management |  | false | enrollment_id | auto_generated |
| [PermissionStatement](#ent_permission_statement) | bc_policy | agg_permission_statement | true | statement_id | auto_generated |
| [ApprovalStatement](#ent_approval_statement) | bc_policy | agg_approval_statement | true | statement_id | auto_generated |
| [IndirectClient](#ent_indirect_client) | bc_indirect_client_management | agg_indirect_client | true | indirect_client_id | derived |
| [RelatedPerson](#ent_related_person) | bc_indirect_client_management |  | false | person_id | auto_generated |
| [User](#ent_user) | bc_users | agg_user | true | user_id | external |
| [UserGroup](#ent_user_group) | bc_users | agg_user_group | true | group_id | auto_generated |
| [UserGroupMembership](#ent_user_group_membership) | bc_users |  | false | membership_id | auto_generated |

<a id="sys_cash_mgmt_platform"></a>
#### Repository: Commercial Banking Cash Management Platform

| Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| sys_cash_mgmt_platform | Commercial Banking Cash Management Platform |  |  |  |  |

<a id="sys_cash_mgmt_platform"></a>
#### Domain Event: Commercial Banking Cash Management Platform

| Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| sys_cash_mgmt_platform | Commercial Banking Cash Management Platform |  |  |  |  |  |

<a id="sys_cash_mgmt_platform"></a>
### Domain Service: Commercial Banking Cash Management Platform

| Id | Name | Bounded Context Ref | Description | Stateless |
| --- | ---- | ------------------- | ----------- | --------- |
| sys_cash_mgmt_platform | Commercial Banking Cash Management Platform |  |  |  |

<a id="sys_cash_mgmt_platform"></a>
### Application Service: Commercial Banking Cash Management Platform

| Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| sys_cash_mgmt_platform | Commercial Banking Cash Management Platform |  |  |  |  |

<a id="sys_cash_mgmt_platform"></a>
### Factory: Commercial Banking Cash Management Platform

| Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| sys_cash_mgmt_platform | Commercial Banking Cash Management Platform |  |  |  |  |  |

<a id="sys_cash_mgmt_platform"></a>
### Specification: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Name: Commercial Banking Cash Management Platform
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="sys_cash_mgmt_platform"></a>
### Context Mapping: Commercial Banking Cash Management Platform

Id: sys_cash_mgmt_platform
Upstream Context: 
Downstream Context: 
Relationship Type: 
Integration Pattern: 
Translation Map: 
Acl Details: 
Notes: 

Shared Elements:

Facades:

Adapters:

Translators: