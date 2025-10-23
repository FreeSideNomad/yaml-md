# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ddd-part/tactical-example.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ddd-part/tactical-ddd.schema.yaml`
Objects Indexed: 20

<a id="agg_profile"></a>
# Aggregate: CandidateProfile

Id: agg_profile
Name: CandidateProfile
Bounded Context Ref: bc_profile
Root Ref: ent_candidate
Size Estimate: medium

Entities: ent_candidate

Value Objects: vo_email vo_phone vo_skill_level vo_location

Consistency Rules: Email must be unique across system Profile must have at least one contact method Skills cannot have proficiency level > 10

Invariants: Candidate must have valid email At least one skill must be specified

<a id="agg_match"></a>
# Aggregate: JobMatch

Id: agg_match
Name: JobMatch
Bounded Context Ref: bc_matching
Root Ref: ent_match
Size Estimate: small

Entities: ent_match

Value Objects: vo_match_score vo_match_criteria

Consistency Rules: Match score must be between 0 and 100 Match must reference valid candidate and job

Invariants: Match score reflects weighted criteria

<a id="agg_job_posting"></a>
# Aggregate: JobPosting

Id: agg_job_posting
Name: JobPosting
Bounded Context Ref: bc_job_catalog
Root Ref: ent_job
Size Estimate: medium

Entities: ent_job

Value Objects: vo_salary_range vo_job_requirements

Consistency Rules: Job must have title and company Salary range min <= max

Invariants: