# YAML Document Overview
Document: `samples/ddd-model.yaml`
Schema: `samples/ddd-schema.yaml`
Objects Indexed: 51

<a id="sys_job_seeker"></a>
# System: Job Seeker Application

Id: sys_job_seeker
Name: Job Seeker Application
Description: AI-powered job application assistant for data scientists
Version: 1.0.0

## Domains

| Domain | Id | Name | Type | Description | Strategic Importance | Investment Strategy | Notes |
| ------ | --- | ---- | ---- | ----------- | -------------------- | ------------------- | ----- |
| [Job Matching](#dom_job_matching) | dom_job_matching | Job Matching | core | Core domain for intelligently matching jobs to candidate profiles | critical | Best team, rigorous DDD, continuous refinement | This is where we provide competitive advantage |
| [Job Aggregation](#dom_job_aggregation) | dom_job_aggregation | Job Aggregation | supporting | Aggregate jobs from various sources and normalize data | important | Adequate quality, consider third-party scraping services | Necessary but not differentiating |
| [Career Development](#dom_career_development) | dom_career_development | Career Development | supporting | Help candidates improve skills and close gaps | important | Adequate quality, focus on actionable insights |  |
| [Application Tracking](#dom_application_tracking) | dom_application_tracking | Application Tracking | supporting | Track job applications and their status | standard | Simple implementation, standard patterns |  |
| [Notifications](#dom_notifications) | dom_notifications | Notifications | generic | Send notifications to users | low | Use third-party service (SendGrid, Twilio) |  |

## Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

## Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

<a id="dom_job_matching"></a>
## Domain: Job Matching

Id: dom_job_matching
Name: Job Matching
Type: core
Description: Core domain for intelligently matching jobs to candidate profiles
Strategic Importance: critical
Investment Strategy: Best team, rigorous DDD, continuous refinement
Notes: This is where we provide competitive advantage

### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |

<a id="bc_profile"></a>
### Bounded Context: Profile Management

Id: bc_profile
Name: Profile Management
Domain Ref: [Job Matching](#dom_job_matching)
Description: Manages candidate profile including skills, experience, preferences
Team Ownership: Core Matching Team

#### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |

#### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |

#### Domain Services

| Domain Service | Id |
| -------------- | --- |
| [Profile Scorer](#svc_dom_profile_scorer) | svc_dom_profile_scorer |

#### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [Import Resume](#svc_app_import_resume) | svc_app_import_resume |  |  |  |  |  |

#### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [Profile Created](#evt_profile_created) | evt_profile_created |  |  |  |  |  |  |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [Skills Changed](#evt_skills_changed) | evt_skills_changed |  |  |  |  |  |  |

#### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

#### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

#### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

#### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

#### Ubiquitous Language

##### Glossary

| Glossary | Term | Definition |
| -------- | ---- | ---------- |
| Candidate A job seeker using the system | Candidate | A job seeker using the system |
| Skills Technical and soft skills possessed by candidate | Skills | Technical and soft skills possessed by candidate |
| Profile Completeness Percentage of profile fields filled with quality information | Profile Completeness | Percentage of profile fields filled with quality information |

<a id="agg_candidate_profile"></a>
#### Aggregate: Candidate Profile

Id: agg_candidate_profile
Name: Candidate Profile
Bounded Context Ref: [Profile Management](#bc_profile)
Root Ref: [Candidate](#ent_candidate)
Lifecycle Hooks: 
Size Estimate: medium

##### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |

##### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Candidate Id](#vo_candidate_id) | vo_candidate_id |  |  |  |  |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Person Name](#vo_person_name) | vo_person_name |  |  |  |  |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [Education](#vo_education) | vo_education |  |  |  |  |
| [Experience](#vo_experience) | vo_experience |  |  |  |  |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |
| [Preferences](#vo_preferences) | vo_preferences |  |  |  |  |

Consistency Rules: Candidate must have valid email Skills list must not be empty for matching to work Location must be valid Canadian location

Invariants: Email uniqueness across all candidates Profile completeness score >= 60% for matching

On Create:

On Update:

On Delete:

##### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

##### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="ent_candidate"></a>
##### Entity: Candidate

Id: ent_candidate
Name: Candidate
Bounded Context Ref: [Profile Management](#bc_profile)
Aggregate Ref: [Candidate Profile](#agg_candidate_profile)
Is Aggregate Root: true
Identity Field: candidate_id
Identity Generation: auto_generated

###### Attributes

| Attribute | Name | Type | Value Object Ref | Required | Description |
| --------- | ---- | ---- | ---------------- | -------- | ----------- |
| candidate_id | candidate_id | CandidateId | vo_candidate_id | true |  |
| email | email | Email | vo_email | true |  |
| name | name | PersonName | vo_person_name | true |  |
| skills | skills | Skills | vo_skills | true |  |
| education | education | Education | vo_education | true |  |
| experience | experience | Experience | vo_experience | false |  |
| location | location | Location | vo_location | true |  |
| preferences | preferences | JobPreferences | vo_preferences | false |  |
| profile_completeness | profile_completeness | Percentage |  | false | Calculated score |

###### Business Methods

| Business Method | Name | Description | Returns |
| --------------- | ---- | ----------- | ------- |
| updateSkills | updateSkills | Update candidate's skills | void |
| calculateCompleteness | calculateCompleteness | Calculate profile completeness percentage | Percentage |
| isEligibleForMatching | isEligibleForMatching | Check if profile is complete enough for matching | boolean |

Invariants: Email must be unique Skills list must not be empty Completeness score must be accurate

Lifecycle States: draft active suspended

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

<a id="vo_email"></a>
###### Value Object: Email

Id: vo_email
Name: Email
Bounded Context Ref: [Profile Management](#bc_profile)
Description: Email address value object with validation
Immutability: true

###### Attributes

| Attribute | Name | Type | Required | Validation |
| --------- | ---- | ---- | -------- | ---------- |
| address | address | string | true | RFC 5322 email format |

Validation Rules: Must match email regex pattern Must have @ symbol and domain Normalized to lowercase

Equality Criteria: address

###### Side Effect Free Methods

| Side Effect Free Method | Name | Description | Returns |
| ----------------------- | ---- | ----------- | ------- |
| domain | domain | Extract domain part | string |
| localPart | localPart | Extract local part | string |

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="ent_job_posting"></a>
###### Entity: Job Posting

Id: ent_job_posting
Name: Job Posting
Bounded Context Ref: [Job Catalog](#bc_job_catalog)
Aggregate Ref: [Job Posting](#agg_job_posting)
Is Aggregate Root: true
Identity Field: job_id
Identity Generation: auto_generated

###### Attributes

| Attribute | Name | Type | Value Object Ref | Required |
| --------- | ---- | ---- | ---------------- | -------- |
| job_id | job_id | JobId | vo_job_id | true |
| title | title | JobTitle | vo_job_title | true |
| company | company | Company | vo_company | true |
| location | location | Location | vo_location | true |
| salary_range | salary_range | SalaryRange | vo_salary_range | false |
| requirements | requirements | Requirements | vo_requirements | true |
| description | description | Description | vo_description | true |
| source | source | Source | vo_source | true |
| posted_date | posted_date | Date |  | true |
| expiry_date | expiry_date | Date |  | false |

###### Business Methods

| Business Method | Name | Description | Returns |
| --------------- | ---- | ----------- | ------- |
| isExpired | isExpired | Check if job posting has expired | boolean |
| markExpired | markExpired | Mark job as expired | void |

Invariants:

Lifecycle States: active expired filled

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

<a id="bc_job_catalog"></a>
###### Bounded Context: Job Catalog

Id: bc_job_catalog
Name: Job Catalog
Domain Ref: [Job Aggregation](#dom_job_aggregation)
Description: Centralized catalog of all jobs from various sources
Team Ownership: Aggregation Team

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Ingest Jobs](#svc_app_ingest_jobs) | svc_app_ingest_jobs |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [Job Expired](#evt_job_expired) | evt_job_expired |  |  |  |  |  |  |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Ubiquitous Language

###### Glossary

| Glossary | Term | Definition |
| -------- | ---- | ---------- |
| Job Posting A job opportunity aggregated from external source | Job Posting | A job opportunity aggregated from external source |
| Source Where job posting came from | Source | Where job posting came from |
| Freshness How recently job was posted or updated | Freshness | How recently job was posted or updated |

<a id="dom_job_aggregation"></a>
###### Domain: Job Aggregation

Id: dom_job_aggregation
Name: Job Aggregation
Type: supporting
Description: Aggregate jobs from various sources and normalize data
Strategic Importance: important
Investment Strategy: Adequate quality, consider third-party scraping services
Notes: Necessary but not differentiating

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |

<a id="bc_scrapers"></a>
###### Bounded Context: Job Scrapers

Id: bc_scrapers
Name: Job Scrapers
Domain Ref: [Job Aggregation](#dom_job_aggregation)
Description: Scrape jobs from external sources
Ubiquitous Language: 
Team Ownership: Aggregation Team

###### Aggregates

| Aggregate | Id |
| --------- | --- |
| [Scraping Job](#agg_scraping_job) | agg_scraping_job |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Scraping Job](#repo_scraping_job) | repo_scraping_job |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Schedule Scraping](#svc_app_schedule_scraping) | svc_app_schedule_scraping |
| [Run Scraper](#svc_app_run_scraper) | svc_app_run_scraper |

###### Domain Events

| Domain Event | Id |
| ------------ | --- |
| [Scraping Completed](#evt_scraping_completed) | evt_scraping_completed |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="factory_candidate_profile"></a>
###### Factory: CandidateProfileFactory

Id: factory_candidate_profile
Name: CandidateProfileFactory
Bounded Context Ref: [Profile Management](#bc_profile)
Creates Type: aggregate
Creates Ref: [Candidate Profile](#agg_candidate_profile)
Location: domain_layer
Reconstitution: true

###### Creation Methods

| Creation Method | Name | Returns | Description |
| --------------- | ---- | ------- | ----------- |
| createFromResume | createFromResume | CandidateProfile | Parse resume and create initial profile |
| createManual | createManual | CandidateProfile | Create empty profile for manual completion |

<a id="factory_job_match"></a>
###### Factory: JobMatchFactory

Id: factory_job_match
Name: JobMatchFactory
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Creates Type: aggregate
Creates Ref: [Job Match](#agg_job_match)
Location: domain_layer
Reconstitution: false

###### Creation Methods

| Creation Method | Name | Returns | Description |
| --------------- | ---- | ------- | ----------- |
| createMatch | createMatch | JobMatch | Create new match result |

<a id="bc_matching"></a>
###### Bounded Context: Job Matching Engine

Id: bc_matching
Name: Job Matching Engine
Domain Ref: [Job Matching](#dom_job_matching)
Description: Intelligent matching of jobs to candidate profiles
Team Ownership: Core Matching Team

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [Scoring Algorithm](#svc_dom_scoring_algorithm) | svc_dom_scoring_algorithm |  |  |  |  |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |
| [Get Recommendations](#svc_app_get_recommendations) | svc_app_get_recommendations |  |  |  |  |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [Match Calculated](#evt_match_calculated) | evt_match_calculated |  |  |  |  |  |  |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Ubiquitous Language

###### Glossary

| Glossary | Term | Definition |
| -------- | ---- | ---------- |
| Match Score Calculated fit between candidate and job (0-100) | Match Score | Calculated fit between candidate and job (0-100) |
| Match Tier Classification of match quality | Match Tier | Classification of match quality |
| Match Criteria Factors considered in matching | Match Criteria | Factors considered in matching |

<a id="agg_job_match"></a>
###### Aggregate: Job Match

Id: agg_job_match
Name: Job Match
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Root Ref: [Job Match](#ent_job_match)
Lifecycle Hooks: 
Size Estimate: small

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Match Tier](#vo_match_tier) | vo_match_tier |  |  |  |  |
| [Match Criteria Scores](#vo_match_criteria_scores) | vo_match_criteria_scores |  |  |  |  |

Consistency Rules: Match score must be 0-100 Match tier must correspond to score (High: 80+, Medium: 50-79, Low: <50)

Invariants: Match score calculated from weighted criteria Match references valid candidate and job

On Create:

On Update:

On Delete:

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="ent_job_match"></a>
###### Entity: Job Match

Id: ent_job_match
Name: Job Match
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Aggregate Ref: [Job Match](#agg_job_match)
Is Aggregate Root: true
Identity Field: match_id
Identity Generation: auto_generated

###### Attributes

| Attribute | Name | Type | Required | Description | Value Object Ref |
| --------- | ---- | ---- | -------- | ----------- | ---------------- |
| match_id | match_id | MatchId | true |  |  |
| candidate_id | candidate_id | CandidateId | true | Reference by ID only |  |
| job_id | job_id | JobId | true | Reference by ID only |  |
| match_score | match_score | MatchScore | true |  | vo_match_score |
| match_tier | match_tier | MatchTier | true |  | vo_match_tier |
| criteria_scores | criteria_scores | CriteriaScores | true |  | vo_match_criteria_scores |
| calculated_at | calculated_at | DateTime | true |  |  |

###### Business Methods

| Business Method | Name | Description | Returns |
| --------------- | ---- | ----------- | ------- |
| recalculate | recalculate | Recalculate match score (if profile or job changed) | void |

Invariants: Score matches tier (80+ = High, 50-79 = Medium, <50 = Low) Criteria scores sum to total score

Lifecycle States:

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Value Object: match_id

Id: 
Name: match_id
Bounded Context Ref: 
Description: 
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: match_id

Id: 
Name: match_id
Domain Ref: 
Description: 
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: match_id

Id: 
Name: match_id
Type: MatchId
Description: 
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

<a id="bc_requirements"></a>
###### Bounded Context: Requirements Analysis

Id: bc_requirements
Name: Requirements Analysis
Domain Ref: [Job Matching](#dom_job_matching)
Description: Analyze and aggregate job requirements across postings
Team Ownership: Core Matching Team

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Requirements Analysis](#repo_requirements_analysis) | repo_requirements_analysis |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |
| [Aggregator](#svc_dom_aggregator) | svc_dom_aggregator |  |  |  |  |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Analyze Requirements](#svc_app_analyze_requirements) | svc_app_analyze_requirements |

###### Domain Events

| Domain Event | Id |
| ------------ | --- |
| [Analysis Completed](#evt_analysis_completed) | evt_analysis_completed |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Ubiquitous Language

###### Glossary

| Glossary | Term | Definition |
| -------- | ---- | ---------- |
| Requirement A skill, qualification, or experience needed for a job | Requirement | A skill, qualification, or experience needed for a job |
| Common Requirement Requirement that appears frequently in high-match jobs | Common Requirement | Requirement that appears frequently in high-match jobs |
| Requirements Gap Requirements candidate doesn't meet | Requirements Gap | Requirements candidate doesn't meet |

<a id="agg_requirements_analysis"></a>
###### Aggregate: Requirements Analysis

Id: agg_requirements_analysis
Name: Requirements Analysis
Bounded Context Ref: [Requirements Analysis](#bc_requirements)
Root Ref: ent_requirements_analysis
Lifecycle Hooks: 
Size Estimate: medium

###### Entities

| Entity | Id |
| ------ | --- |
| [Requirements Analysis](#ent_requirements_analysis) | ent_requirements_analysis |
| [Requirement Frequency](#ent_requirement_frequency) | ent_requirement_frequency |

###### Value Objects

| Value Object | Id |
| ------------ | --- |
| [Requirement](#vo_requirement) | vo_requirement |
| [Frequency](#vo_frequency) | vo_frequency |
| [Importance Score](#vo_importance_score) | vo_importance_score |

Consistency Rules: Analysis must be for specific candidate and time period Requirements sorted by frequency

Invariants: Analysis date <= Current date

On Create:

On Update:

On Delete:

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="evt_profile_updated"></a>
###### Domain Event: ProfileUpdated

Id: evt_profile_updated
Name: ProfileUpdated
Bounded Context Ref: [Profile Management](#bc_profile)
Aggregate Ref: [Candidate Profile](#agg_candidate_profile)
Description: Candidate profile was updated
Immutable: true
Timestamp Included: true

###### Data Carried

| Data Carried | Name | Type |
| ------------ | ---- | ---- |
| candidate_id | candidate_id | CandidateId |
| updated_fields | updated_fields | Set<String> |
| occurred_at | occurred_at | DateTime |

###### Handlers

| Handler | Bounded Context | Handler | Action |
| ------- | --------------- | ------- | ------ |
| bc_matching RecalculateMatchesHandler Recalculate all matches for this candidate | bc_matching | RecalculateMatchesHandler | Recalculate all matches for this candidate |
| bc_requirements UpdateRequirementsHandler Update requirements analysis | bc_requirements | UpdateRequirementsHandler | Update requirements analysis |

<a id="evt_job_posted"></a>
###### Domain Event: JobPosted

Id: evt_job_posted
Name: JobPosted
Bounded Context Ref: [Job Catalog](#bc_job_catalog)
Aggregate Ref: [Job Posting](#agg_job_posting)
Description: New job was posted to catalog
Immutable: true
Timestamp Included: true

###### Data Carried

| Data Carried | Name | Type |
| ------------ | ---- | ---- |
| job_id | job_id | JobId |
| title | title | JobTitle |
| location | location | Location |
| occurred_at | occurred_at | DateTime |

###### Handlers

| Handler | Bounded Context | Handler | Action |
| ------- | --------------- | ------- | ------ |
| bc_matching CalculateMatchesForNewJob Calculate matches for all eligible candidates | bc_matching | CalculateMatchesForNewJob | Calculate matches for all eligible candidates |

<a id="agg_job_posting"></a>
###### Aggregate: Job Posting

Id: agg_job_posting
Name: Job Posting
Bounded Context Ref: [Job Catalog](#bc_job_catalog)
Root Ref: [Job Posting](#ent_job_posting)
Lifecycle Hooks: 
Size Estimate: small

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Job Id](#vo_job_id) | vo_job_id |  |  |  |  |
| [Job Title](#vo_job_title) | vo_job_title |  |  |  |  |
| [Company](#vo_company) | vo_company |  |  |  |  |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |
| [Salary Range](#vo_salary_range) | vo_salary_range |  |  |  |  |
| [Requirements](#vo_requirements) | vo_requirements |  |  |  |  |
| [Description](#vo_description) | vo_description |  |  |  |  |
| [Source](#vo_source) | vo_source |  |  |  |  |

Consistency Rules: Job must have title, company, and source Job must not be duplicate (same title, company, location)

Invariants: Posted date <= Current date Expiry date > Posted date

On Create:

On Update:

On Delete:

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="vo_location"></a>
###### Value Object: Location

Id: vo_location
Name: Location
Bounded Context Ref: [Profile Management](#bc_profile)
Description: Canadian location (city, province)
Immutability: true

###### Attributes

| Attribute | Name | Type | Required | Validation |
| --------- | ---- | ---- | -------- | ---------- |
| city | city | string | true |  |
| province | province | CanadianProvince | true |  |
| country | country | string | true | Must be 'Canada' |

Validation Rules: Province must be valid Canadian province code (ON, BC, QC, etc.) Country must be 'Canada'

Equality Criteria: city province country

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="evt_high_match_found"></a>
###### Domain Event: HighMatchFound

Id: evt_high_match_found
Name: HighMatchFound
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Aggregate Ref: [Job Match](#agg_job_match)
Description: A high-quality match (score >= 80) was found
Immutable: true
Timestamp Included: true

###### Data Carried

| Data Carried | Name | Type |
| ------------ | ---- | ---- |
| match_id | match_id | MatchId |
| candidate_id | candidate_id | CandidateId |
| job_id | job_id | JobId |
| match_score | match_score | MatchScore |
| occurred_at | occurred_at | DateTime |

###### Handlers

| Handler | Bounded Context | Handler | Action |
| ------- | --------------- | ------- | ------ |
| bc_notifications NotifyHighMatch Send notification to candidate | bc_notifications | NotifyHighMatch | Send notification to candidate |

<a id="evt_application_submitted"></a>
###### Domain Event: ApplicationSubmitted

Id: evt_application_submitted
Name: ApplicationSubmitted
Bounded Context Ref: [Application Tracking](#bc_applications)
Aggregate Ref: [Job Application](#agg_job_application)
Description: Candidate submitted job application
Immutable: true
Timestamp Included: true

###### Data Carried

| Data Carried | Name | Type |
| ------------ | ---- | ---- |
| application_id | application_id | ApplicationId |
| candidate_id | candidate_id | CandidateId |
| job_id | job_id | JobId |
| submitted_at | submitted_at | DateTime |

###### Handlers

| Handler | Bounded Context | Handler | Action |
| ------- | --------------- | ------- | ------ |
| bc_notifications SendConfirmation Send confirmation email | bc_notifications | SendConfirmation | Send confirmation email |
| bc_matching UpdateMatchStatus Mark job as applied | bc_matching | UpdateMatchStatus | Mark job as applied |

<a id="bc_applications"></a>
###### Bounded Context: Application Tracking

Id: bc_applications
Name: Application Tracking
Domain Ref: [Application Tracking](#dom_application_tracking)
Description: Track job applications and their progress
Ubiquitous Language: 
Team Ownership: Application Tracking Team

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Application](#repo_application) | repo_application |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |
| [Update Status](#svc_app_update_status) | svc_app_update_status |  |  |  |  |  |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |
| [Application Status Changed](#evt_application_status_changed) | evt_application_status_changed |  |  |  |  |  |  |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="dom_application_tracking"></a>
###### Domain: Application Tracking

Id: dom_application_tracking
Name: Application Tracking
Type: supporting
Description: Track job applications and their status
Strategic Importance: standard
Investment Strategy: Simple implementation, standard patterns
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |

<a id="agg_job_application"></a>
###### Aggregate: Job Application

Id: agg_job_application
Name: Job Application
Bounded Context Ref: [Application Tracking](#bc_applications)
Root Ref: ent_job_application
Lifecycle Hooks: 
Size Estimate: small

###### Entities

| Entity | Id |
| ------ | --- |
| [Job Application](#ent_job_application) | ent_job_application |

###### Value Objects

| Value Object | Id |
| ------------ | --- |
| [Application Status](#vo_application_status) | vo_application_status |
| [Application Date](#vo_application_date) | vo_application_date |
| [Resume Version](#vo_resume_version) | vo_resume_version |
| [Cover Letter](#vo_cover_letter) | vo_cover_letter |

Consistency Rules: Cannot apply to same job twice Status transitions must be valid (applied → interviewing → offer/rejected)

Invariants: Application references valid candidate and job

On Create:

On Update:

On Delete:

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="repo_profile"></a>
###### Repository: ProfileRepository

Id: repo_profile
Name: ProfileRepository
Bounded Context Ref: [Profile Management](#bc_profile)
Aggregate Ref: [Candidate Profile](#agg_candidate_profile)
Persistence Strategy: PostgreSQL with JPA
Implementation Notes: Uses Data Mapper pattern to separate domain model from persistence

###### Interface Methods

| Interface Method | Name | Returns | Query Type |
| ---------------- | ---- | ------- | ---------- |
| save | save | void | custom |
| findById | findById | Optional<CandidateProfile> | by_id |
| findByEmail | findByEmail | Optional<CandidateProfile> | by_criteria |
| findIncompleteProfiles | findIncompleteProfiles | List<CandidateProfile> | custom |

<a id="repo_job_posting"></a>
###### Repository: JobPostingRepository

Id: repo_job_posting
Name: JobPostingRepository
Bounded Context Ref: [Job Catalog](#bc_job_catalog)
Aggregate Ref: [Job Posting](#agg_job_posting)
Persistence Strategy: PostgreSQL with pgvector for semantic search
Implementation Notes: Job embeddings stored for similarity matching

###### Interface Methods

| Interface Method | Name | Returns | Query Type |
| ---------------- | ---- | ------- | ---------- |
| save | save | void | custom |
| findById | findById | Optional<JobPosting> | by_id |
| findActive | findActive | List<JobPosting> | custom |
| findByLocation | findByLocation | List<JobPosting> | by_criteria |
| findPostedAfter | findPostedAfter | List<JobPosting> | by_criteria |

<a id="repo_job_match"></a>
###### Repository: JobMatchRepository

Id: repo_job_match
Name: JobMatchRepository
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Aggregate Ref: [Job Match](#agg_job_match)
Persistence Strategy: PostgreSQL
Implementation Notes: 

###### Interface Methods

| Interface Method | Name | Returns | Query Type |
| ---------------- | ---- | ------- | ---------- |
| save | save | void | custom |
| findByCandidate | findByCandidate | List<JobMatch> | by_criteria |
| findHighMatches | findHighMatches | List<JobMatch> | custom |
| findByJob | findByJob | List<JobMatch> | by_criteria |

<a id="svc_app_submit_application"></a>
###### Application Service: SubmitApplicationService

Id: svc_app_submit_application
Name: SubmitApplicationService
Bounded Context Ref: [Application Tracking](#bc_applications)
Use Case: Candidate submits application for a job
Transaction Boundary: true
Authorization: Candidate must own the profile

###### Orchestrates

| Orchestrate | Type | Ref | Operation |
| ----------- | ---- | --- | --------- |
| aggregate agg_job_application create | aggregate | agg_job_application | create |
| repository repo_application save | repository | repo_application | save |

###### Publishes Events

| Publishes Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --------------- | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

<a id="bc_applications"></a>
###### Specification: Application Tracking

Id: bc_applications
Name: Application Tracking
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="cm_profile_to_matching"></a>
###### Context Mapping: Profile To Matching

Id: cm_profile_to_matching
Upstream Context: [Profile Management](#bc_profile)
Downstream Context: [Job Matching Engine](#bc_matching)
Relationship Type: customer_supplier
Integration Pattern: Domain events + Direct repository access
Translation Map: 
Acl Details: 
Notes: Matching needs profile data. Profile team supports matching requirements.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="cm_job_catalog_to_matching"></a>
###### Context Mapping: Job Catalog To Matching

Id: cm_job_catalog_to_matching
Upstream Context: [Job Catalog](#bc_job_catalog)
Downstream Context: [Job Matching Engine](#bc_matching)
Relationship Type: customer_supplier
Integration Pattern: Read-only repository access
Translation Map: 
Acl Details: 
Notes: Matching reads jobs from catalog. Catalog team ensures data quality.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="cm_matching_to_requirements"></a>
###### Context Mapping: Matching To Requirements

Id: cm_matching_to_requirements
Upstream Context: [Job Matching Engine](#bc_matching)
Downstream Context: [Requirements Analysis](#bc_requirements)
Relationship Type: partnership
Integration Pattern: Shared analysis, coordinated development
Translation Map: 
Acl Details: 
Notes: Close collaboration needed. Both improve together.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="cm_requirements_to_skills"></a>
###### Context Mapping: Requirements To Skills

Id: cm_requirements_to_skills
Upstream Context: [Requirements Analysis](#bc_requirements)
Downstream Context: [Skills Gap Analysis](#bc_skills_analysis)
Relationship Type: customer_supplier
Integration Pattern: Domain events
Translation Map: 
Acl Details: 
Notes: Skills analysis reacts to requirement analysis completion.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="bc_skills_analysis"></a>
###### Bounded Context: Skills Gap Analysis

Id: bc_skills_analysis
Name: Skills Gap Analysis
Domain Ref: [Career Development](#dom_career_development)
Description: Identify skill gaps and prioritize learning
Ubiquitous Language: 
Team Ownership: Career Development Team

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Skills Gap](#repo_skills_gap) | repo_skills_gap |

###### Domain Services

| Domain Service | Id |
| -------------- | --- |
| [Gap Identifier](#svc_dom_gap_identifier) | svc_dom_gap_identifier |
| [Priority Ranker](#svc_dom_priority_ranker) | svc_dom_priority_ranker |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Generate Gap Report](#svc_app_generate_gap_report) | svc_app_generate_gap_report |

###### Domain Events

| Domain Event | Id |
| ------------ | --- |
| [Gap Identified](#evt_gap_identified) | evt_gap_identified |
| [Skill Acquired](#evt_skill_acquired) | evt_skill_acquired |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="dom_career_development"></a>
###### Domain: Career Development

Id: dom_career_development
Name: Career Development
Type: supporting
Description: Help candidates improve skills and close gaps
Strategic Importance: important
Investment Strategy: Adequate quality, focus on actionable insights
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |

<a id="bc_project_recommendations"></a>
###### Bounded Context: Project Recommendations

Id: bc_project_recommendations
Name: Project Recommendations
Domain Ref: [Career Development](#dom_career_development)
Description: Recommend portfolio projects to close skill gaps
Ubiquitous Language: 
Team Ownership: Career Development Team

###### Aggregates

| Aggregate | Id |
| --------- | --- |
| [Project Recommendation](#agg_project_recommendation) | agg_project_recommendation |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Project Recommendation](#repo_project_recommendation) | repo_project_recommendation |

###### Domain Services

| Domain Service | Id |
| -------------- | --- |
| [Project Recommender](#svc_dom_project_recommender) | svc_dom_project_recommender |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Get Project Ideas](#svc_app_get_project_ideas) | svc_app_get_project_ideas |

###### Domain Events

| Domain Event | Id |
| ------------ | --- |
| [Projects Recommended](#evt_projects_recommended) | evt_projects_recommended |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="bc_project_recommendations"></a>
###### Specification: Project Recommendations

Id: bc_project_recommendations
Name: Project Recommendations
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="cm_skills_to_projects"></a>
###### Context Mapping: Skills To Projects

Id: cm_skills_to_projects
Upstream Context: [Skills Gap Analysis](#bc_skills_analysis)
Downstream Context: [Project Recommendations](#bc_project_recommendations)
Relationship Type: customer_supplier
Integration Pattern: API calls
Translation Map: 
Acl Details: 
Notes: Project recommendations based on identified gaps.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="cm_scrapers_to_catalog"></a>
###### Context Mapping: Scrapers To Catalog

Id: cm_scrapers_to_catalog
Upstream Context: [Job Scrapers](#bc_scrapers)
Downstream Context: [Job Catalog](#bc_job_catalog)
Relationship Type: customer_supplier
Integration Pattern: Message queue (async)
Translation Map: 
Acl Details: 
Notes: Scrapers publish jobs, catalog ingests and normalizes.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="cm_matching_to_notifications"></a>
###### Context Mapping: Matching To Notifications

Id: cm_matching_to_notifications
Upstream Context: [Job Matching Engine](#bc_matching)
Downstream Context: [Notifications](#bc_notifications)
Relationship Type: conformist
Integration Pattern: Third-party service API
Translation Map: 
Acl Details: 
Notes: Notifications uses SendGrid. Matching conforms to their API.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="bc_notifications"></a>
###### Bounded Context: Notifications

Id: bc_notifications
Name: Notifications
Domain Ref: [Notifications](#dom_notifications)
Description: Send email, SMS, push notifications
Ubiquitous Language: 
Team Ownership: Infrastructure Team

###### Aggregates

| Aggregate | Id |
| --------- | --- |
| [Notification](#agg_notification) | agg_notification |

###### Repositories

| Repository | Id |
| ---------- | --- |
| [Notification](#repo_notification) | repo_notification |

###### Application Services

| Application Service | Id |
| ------------------- | --- |
| [Send Notification](#svc_app_send_notification) | svc_app_send_notification |

###### Domain Events

| Domain Event | Id |
| ------------ | --- |
| [Notification Sent](#evt_notification_sent) | evt_notification_sent |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="dom_notifications"></a>
###### Domain: Notifications

Id: dom_notifications
Name: Notifications
Type: generic
Description: Send notifications to users
Strategic Importance: low
Investment Strategy: Use third-party service (SendGrid, Twilio)
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

<a id="bc_notifications"></a>
###### Specification: Notifications

Id: bc_notifications
Name: Notifications
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="cm_applications_to_notifications"></a>
###### Context Mapping: Applications To Notifications

Id: cm_applications_to_notifications
Upstream Context: [Application Tracking](#bc_applications)
Downstream Context: [Notifications](#bc_notifications)
Relationship Type: conformist
Integration Pattern: Third-party service API
Translation Map: 
Acl Details: 
Notes: Application updates trigger notifications.

Shared Elements:

Facades:

Adapters:

Translators:

<a id="vo_skills"></a>
###### Value Object: Skills

Id: vo_skills
Name: Skills
Bounded Context Ref: [Profile Management](#bc_profile)
Description: Collection of candidate skills with proficiency levels
Immutability: true

###### Attributes

| Attribute | Name | Type | Required |
| --------- | ---- | ---- | -------- |
| technical_skills | technical_skills | Map<SkillName, ProficiencyLevel> | true |
| soft_skills | soft_skills | Set<SkillName> | false |

Validation Rules: Technical skills map must not be empty Proficiency levels must be: beginner, intermediate, advanced, expert

Equality Criteria: technical_skills soft_skills

###### Side Effect Free Methods

| Side Effect Free Method | Name | Description | Returns |
| ----------------------- | ---- | ----------- | ------- |
| hasSkill | hasSkill | Check if skill exists | boolean |
| proficiencyFor | proficiencyFor | Get proficiency for skill | ProficiencyLevel |
| addSkill | addSkill | Return new Skills with added skill | Skills |
| overlapWith | overlapWith | Calculate overlap with other Skills | Percentage |

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="vo_match_score"></a>
###### Value Object: MatchScore

Id: vo_match_score
Name: MatchScore
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Description: Calculated match score between 0 and 100
Immutability: true

###### Attributes

| Attribute | Name | Type | Required | Validation |
| --------- | ---- | ---- | -------- | ---------- |
| value | value | int | true | 0 <= value <= 100 |

Validation Rules: Score must be between 0 and 100 inclusive

Equality Criteria: value

###### Side Effect Free Methods

| Side Effect Free Method | Name | Description | Returns |
| ----------------------- | ---- | ----------- | ------- |
| isHighMatch | isHighMatch | Score >= 80 | boolean |
| isMediumMatch | isMediumMatch | 50 <= Score < 80 | boolean |
| isLowMatch | isLowMatch | Score < 50 | boolean |

Common Values: ZERO PERFECT (100) MINIMUM_ACCEPTABLE (50)

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

<a id="agg_skills_gap_report"></a>
###### Aggregate: Skills Gap Report

Id: agg_skills_gap_report
Name: Skills Gap Report
Bounded Context Ref: [Skills Gap Analysis](#bc_skills_analysis)
Root Ref: ent_skills_gap_report
Lifecycle Hooks: 
Size Estimate: small

###### Entities

| Entity | Id |
| ------ | --- |
| [Skills Gap Report](#ent_skills_gap_report) | ent_skills_gap_report |
| [Skill Gap](#ent_skill_gap) | ent_skill_gap |

###### Value Objects

| Value Object | Id |
| ------------ | --- |
| [Skill](#vo_skill) | vo_skill |
| [Gap Severity](#vo_gap_severity) | vo_gap_severity |
| [Learning Priority](#vo_learning_priority) | vo_learning_priority |

Consistency Rules: Gaps identified from requirements analysis Priority based on frequency and importance

Invariants: Report is for specific candidate

On Create:

On Update:

On Delete:

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

<a id="bc_skills_analysis"></a>
###### Specification: Skills Gap Analysis

Id: bc_skills_analysis
Name: Skills Gap Analysis
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="svc_dom_requirement_extractor"></a>
###### Domain Service: RequirementExtractor

Id: svc_dom_requirement_extractor
Name: RequirementExtractor
Bounded Context Ref: [Requirements Analysis](#bc_requirements)
Description: Extracts structured requirements from job descriptions using NLP
Stateless: true

###### Operations

| Operation | Name | Description | Returns | Business Logic |
| --------- | ---- | ----------- | ------- | -------------- |
| extract | extract | Extract requirements from job description | Requirements | NLP-based extraction of skills, years of experience, education level, certifications |

<a id="bc_requirements"></a>
###### Specification: Requirements Analysis

Id: bc_requirements
Name: Requirements Analysis
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="svc_dom_matching_engine"></a>
###### Domain Service: MatchingEngine

Id: svc_dom_matching_engine
Name: MatchingEngine
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Description: Core algorithm for calculating job-candidate match scores
Stateless: true

###### Operations

| Operation | Name | Description | Returns | Business Logic |
| --------- | ---- | ----------- | ------- | -------------- |
| calculateMatch | calculateMatch | Calculate match between candidate and job | JobMatch | Multi-criteria weighted scoring: skills (40%), experience (25%), education (20%), location (10%), domain (5%) |
| findBestMatches | findBestMatches | Find top N matches for candidate | List<JobMatch> | Returns matches sorted by score, filtered by minimum threshold |

###### Dependencies

| Dependency | Type | Ref |
| ---------- | ---- | --- |
| repository repo_profile | repository | repo_profile |
| repository repo_job_posting | repository | repo_job_posting |

<a id="svc_dom_deduplication"></a>
###### Domain Service: JobDeduplicationService

Id: svc_dom_deduplication
Name: JobDeduplicationService
Bounded Context Ref: [Job Catalog](#bc_job_catalog)
Description: Identifies and merges duplicate job postings from different sources
Stateless: true

###### Operations

| Operation | Name | Description | Returns | Business Logic |
| --------- | ---- | ----------- | ------- | -------------- |
| isDuplicate | isDuplicate | Check if two jobs are the same | boolean | Fuzzy matching on title + company + location; similarity threshold 85% |
| mergeDuplicates | mergeDuplicates | Merge multiple postings of same job | JobPosting | Keep most recent, aggregate sources, prefer higher quality data |

<a id="svc_app_update_profile"></a>
###### Application Service: UpdateProfileService

Id: svc_app_update_profile
Name: UpdateProfileService
Bounded Context Ref: [Profile Management](#bc_profile)
Use Case: Candidate updates their profile
Transaction Boundary: true
Authorization: Only the candidate can update their own profile

###### Orchestrates

| Orchestrate | Type | Ref | Operation |
| ----------- | ---- | --- | --------- |
| repository repo_profile findById, save | repository | repo_profile | findById, save |
| aggregate agg_candidate_profile updateSkills, calculateCompleteness | aggregate | agg_candidate_profile | updateSkills, calculateCompleteness |

###### Publishes Events

| Publishes Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --------------- | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |

<a id="svc_app_calculate_matches"></a>
###### Application Service: CalculateMatchesService

Id: svc_app_calculate_matches
Name: CalculateMatchesService
Bounded Context Ref: [Job Matching Engine](#bc_matching)
Use Case: Calculate matches for all new jobs or updated profile
Transaction Boundary: true
Authorization: 

###### Orchestrates

| Orchestrate | Type | Ref | Operation |
| ----------- | ---- | --- | --------- |
| repository repo_profile findById | repository | repo_profile | findById |
| repository repo_job_posting findActive | repository | repo_job_posting | findActive |
| domain_service svc_dom_matching_engine calculateMatch | domain_service | svc_dom_matching_engine | calculateMatch |
| repository repo_job_match save | repository | repo_job_match | save |

###### Publishes Events

| Publishes Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| --------------- | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [Match Calculated](#evt_match_calculated) | evt_match_calculated |  |  |  |  |  |  |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |

###### Specification: match_id

Id: 
Name: match_id
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: candidate_id

Id: 
Name: candidate_id
Bounded Context Ref: 
Description: Reference by ID only
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: candidate_id

Id: 
Name: candidate_id
Domain Ref: 
Description: Reference by ID only
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: candidate_id

Id: 
Name: candidate_id
Type: CandidateId
Description: Reference by ID only
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: candidate_id

Id: 
Name: candidate_id
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: job_id

Id: 
Name: job_id
Bounded Context Ref: 
Description: Reference by ID only
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: job_id

Id: 
Name: job_id
Domain Ref: 
Description: Reference by ID only
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: job_id

Id: 
Name: job_id
Type: JobId
Description: Reference by ID only
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: job_id

Id: 
Name: job_id
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: calculated_at

Id: 
Name: calculated_at
Bounded Context Ref: 
Description: 
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: calculated_at

Id: 
Name: calculated_at
Domain Ref: 
Description: 
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: calculated_at

Id: 
Name: calculated_at
Type: DateTime
Description: 
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: calculated_at

Id: 
Name: calculated_at
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_matching"></a>
###### Specification: Job Matching Engine

Id: bc_matching
Name: Job Matching Engine
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_scrapers"></a>
###### Specification: Job Scrapers

Id: bc_scrapers
Name: Job Scrapers
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_job_catalog"></a>
###### Specification: Job Catalog

Id: bc_job_catalog
Name: Job Catalog
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: posted_date

Id: 
Name: posted_date
Bounded Context Ref: 
Description: 
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: posted_date

Id: 
Name: posted_date
Domain Ref: 
Description: 
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: posted_date

Id: 
Name: posted_date
Type: Date
Description: 
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: posted_date

Id: 
Name: posted_date
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: expiry_date

Id: 
Name: expiry_date
Bounded Context Ref: 
Description: 
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: expiry_date

Id: 
Name: expiry_date
Domain Ref: 
Description: 
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: expiry_date

Id: 
Name: expiry_date
Type: Date
Description: 
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: expiry_date

Id: 
Name: expiry_date
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

###### Value Object: profile_completeness

Id: 
Name: profile_completeness
Bounded Context Ref: 
Description: Calculated score
Immutability: 

Validation Rules:

Equality Criteria:

Common Values:

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Bounded Context: profile_completeness

Id: 
Name: profile_completeness
Domain Ref: 
Description: Calculated score
Ubiquitous Language: 
Team Ownership: 

###### Aggregates

| Aggregate | Id | Name | Bounded Context Ref | Root Ref | Size Estimate |
| --------- | --- | ---- | ------------------- | -------- | ------------- |
| [Candidate Profile](#agg_candidate_profile) | agg_candidate_profile | Candidate Profile | bc_profile | ent_candidate | medium |
| [Job Posting](#agg_job_posting) | agg_job_posting | Job Posting | bc_job_catalog | ent_job_posting | small |
| [Job Match](#agg_job_match) | agg_job_match | Job Match | bc_matching | ent_job_match | small |
| [Requirements Analysis](#agg_requirements_analysis) | agg_requirements_analysis | Requirements Analysis | bc_requirements | ent_requirements_analysis | medium |
| [Skills Gap Report](#agg_skills_gap_report) | agg_skills_gap_report | Skills Gap Report | bc_skills_analysis | ent_skills_gap_report | small |
| [Job Application](#agg_job_application) | agg_job_application | Job Application | bc_applications | ent_job_application | small |

###### Repositories

| Repository | Id | Name | Bounded Context Ref | Aggregate Ref | Persistence Strategy | Implementation Notes |
| ---------- | --- | ---- | ------------------- | ------------- | -------------------- | -------------------- |
| [ProfileRepository](#repo_profile) | repo_profile | ProfileRepository | bc_profile | agg_candidate_profile | PostgreSQL with JPA | Uses Data Mapper pattern to separate domain model from persistence |
| [JobPostingRepository](#repo_job_posting) | repo_job_posting | JobPostingRepository | bc_job_catalog | agg_job_posting | PostgreSQL with pgvector for semantic search | Job embeddings stored for similarity matching |
| [JobMatchRepository](#repo_job_match) | repo_job_match | JobMatchRepository | bc_matching | agg_job_match | PostgreSQL |  |

###### Domain Services

| Domain Service | Id | Name | Bounded Context Ref | Description | Stateless |
| -------------- | --- | ---- | ------------------- | ----------- | --------- |
| [MatchingEngine](#svc_dom_matching_engine) | svc_dom_matching_engine | MatchingEngine | bc_matching | Core algorithm for calculating job-candidate match scores | true |
| [JobDeduplicationService](#svc_dom_deduplication) | svc_dom_deduplication | JobDeduplicationService | bc_job_catalog | Identifies and merges duplicate job postings from different sources | true |
| [RequirementExtractor](#svc_dom_requirement_extractor) | svc_dom_requirement_extractor | RequirementExtractor | bc_requirements | Extracts structured requirements from job descriptions using NLP | true |

###### Application Services

| Application Service | Id | Name | Bounded Context Ref | Use Case | Transaction Boundary | Authorization |
| ------------------- | --- | ---- | ------------------- | -------- | -------------------- | ------------- |
| [UpdateProfileService](#svc_app_update_profile) | svc_app_update_profile | UpdateProfileService | bc_profile | Candidate updates their profile | true | Only the candidate can update their own profile |
| [CalculateMatchesService](#svc_app_calculate_matches) | svc_app_calculate_matches | CalculateMatchesService | bc_matching | Calculate matches for all new jobs or updated profile | true |  |
| [SubmitApplicationService](#svc_app_submit_application) | svc_app_submit_application | SubmitApplicationService | bc_applications | Candidate submits application for a job | true | Candidate must own the profile |

###### Domain Events

| Domain Event | Id | Name | Bounded Context Ref | Aggregate Ref | Description | Immutable | Timestamp Included |
| ------------ | --- | ---- | ------------------- | ------------- | ----------- | --------- | ------------------ |
| [ProfileUpdated](#evt_profile_updated) | evt_profile_updated | ProfileUpdated | bc_profile | agg_candidate_profile | Candidate profile was updated | true | true |
| [JobPosted](#evt_job_posted) | evt_job_posted | JobPosted | bc_job_catalog | agg_job_posting | New job was posted to catalog | true | true |
| [HighMatchFound](#evt_high_match_found) | evt_high_match_found | HighMatchFound | bc_matching | agg_job_match | A high-quality match (score >= 80) was found | true | true |
| [ApplicationSubmitted](#evt_application_submitted) | evt_application_submitted | ApplicationSubmitted | bc_applications | agg_job_application | Candidate submitted job application | true | true |

###### Factories

| Factory | Id | Name | Bounded Context Ref | Creates Type | Creates Ref | Location | Reconstitution |
| ------- | --- | ---- | ------------------- | ------------ | ----------- | -------- | -------------- |
| [CandidateProfileFactory](#factory_candidate_profile) | factory_candidate_profile | CandidateProfileFactory | bc_profile | aggregate | agg_candidate_profile | domain_layer | true |
| [JobMatchFactory](#factory_job_match) | factory_job_match | JobMatchFactory | bc_matching | aggregate | agg_job_match | domain_layer | false |

###### Context Mappings

| Context Mapping | Id | Upstream Context | Downstream Context | Relationship Type | Integration Pattern | Notes |
| --------------- | --- | ---------------- | ------------------ | ----------------- | ------------------- | ----- |
| [Profile To Matching](#cm_profile_to_matching) | cm_profile_to_matching | bc_profile | bc_matching | customer_supplier | Domain events + Direct repository access | Matching needs profile data. Profile team supports matching requirements. |
| [Job Catalog To Matching](#cm_job_catalog_to_matching) | cm_job_catalog_to_matching | bc_job_catalog | bc_matching | customer_supplier | Read-only repository access | Matching reads jobs from catalog. Catalog team ensures data quality. |
| [Matching To Requirements](#cm_matching_to_requirements) | cm_matching_to_requirements | bc_matching | bc_requirements | partnership | Shared analysis, coordinated development | Close collaboration needed. Both improve together. |
| [Requirements To Skills](#cm_requirements_to_skills) | cm_requirements_to_skills | bc_requirements | bc_skills_analysis | customer_supplier | Domain events | Skills analysis reacts to requirement analysis completion. |
| [Skills To Projects](#cm_skills_to_projects) | cm_skills_to_projects | bc_skills_analysis | bc_project_recommendations | customer_supplier | API calls | Project recommendations based on identified gaps. |
| [Scrapers To Catalog](#cm_scrapers_to_catalog) | cm_scrapers_to_catalog | bc_scrapers | bc_job_catalog | customer_supplier | Message queue (async) | Scrapers publish jobs, catalog ingests and normalizes. |
| [Matching To Notifications](#cm_matching_to_notifications) | cm_matching_to_notifications | bc_matching | bc_notifications | conformist | Third-party service API | Notifications uses SendGrid. Matching conforms to their API. |
| [Applications To Notifications](#cm_applications_to_notifications) | cm_applications_to_notifications | bc_applications | bc_notifications | conformist | Third-party service API | Application updates trigger notifications. |

###### Value Objects

| Value Object | Id | Name | Bounded Context Ref | Description | Immutability |
| ------------ | --- | ---- | ------------------- | ----------- | ------------ |
| [Email](#vo_email) | vo_email | Email | bc_profile | Email address value object with validation | true |
| [Skills](#vo_skills) | vo_skills | Skills | bc_profile | Collection of candidate skills with proficiency levels | true |
| [MatchScore](#vo_match_score) | vo_match_score | MatchScore | bc_matching | Calculated match score between 0 and 100 | true |
| [Location](#vo_location) | vo_location | Location | bc_profile | Canadian location (city, province) | true |

###### Entities

| Entity | Id | Name | Bounded Context Ref | Aggregate Ref | Is Aggregate Root | Identity Field | Identity Generation |
| ------ | --- | ---- | ------------------- | ------------- | ----------------- | -------------- | ------------------- |
| [Candidate](#ent_candidate) | ent_candidate | Candidate | bc_profile | agg_candidate_profile | true | candidate_id | auto_generated |
| [Job Posting](#ent_job_posting) | ent_job_posting | Job Posting | bc_job_catalog | agg_job_posting | true | job_id | auto_generated |
| [Job Match](#ent_job_match) | ent_job_match | Job Match | bc_matching | agg_job_match | true | match_id | auto_generated |

###### Domain: profile_completeness

Id: 
Name: profile_completeness
Type: Percentage
Description: Calculated score
Strategic Importance: 
Investment Strategy: 
Notes: 

###### Bounded Contexts

| Bounded Context | Id | Name | Domain Ref | Description | Team Ownership |
| --------------- | --- | ---- | ---------- | ----------- | -------------- |
| [Profile Management](#bc_profile) | bc_profile | Profile Management | dom_job_matching | Manages candidate profile including skills, experience, preferences | Core Matching Team |
| [Job Catalog](#bc_job_catalog) | bc_job_catalog | Job Catalog | dom_job_aggregation | Centralized catalog of all jobs from various sources | Aggregation Team |
| [Job Matching Engine](#bc_matching) | bc_matching | Job Matching Engine | dom_job_matching | Intelligent matching of jobs to candidate profiles | Core Matching Team |
| [Requirements Analysis](#bc_requirements) | bc_requirements | Requirements Analysis | dom_job_matching | Analyze and aggregate job requirements across postings | Core Matching Team |
| [Skills Gap Analysis](#bc_skills_analysis) | bc_skills_analysis | Skills Gap Analysis | dom_career_development | Identify skill gaps and prioritize learning | Career Development Team |
| [Project Recommendations](#bc_project_recommendations) | bc_project_recommendations | Project Recommendations | dom_career_development | Recommend portfolio projects to close skill gaps | Career Development Team |
| [Application Tracking](#bc_applications) | bc_applications | Application Tracking | dom_application_tracking | Track job applications and their progress | Application Tracking Team |
| [Job Scrapers](#bc_scrapers) | bc_scrapers | Job Scrapers | dom_job_aggregation | Scrape jobs from external sources | Aggregation Team |
| [Notifications](#bc_notifications) | bc_notifications | Notifications | dom_notifications | Send email, SMS, push notifications | Infrastructure Team |

###### Specification: profile_completeness

Id: 
Name: profile_completeness
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases:

<a id="bc_profile"></a>
#### Specification: Profile Management

Id: bc_profile
Name: Profile Management
Bounded Context Ref: 
Applies To: 
Rule: 
Composable: 

Use Cases: