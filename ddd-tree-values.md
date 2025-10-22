# YAML Document Values
# Document: samples/ddd-model.yaml
# Schema: samples/ddd-schema.yaml
# Total objects indexed: 51

system [type] (id: sys_job_seeker)
  system.id [attribute[string]]: sys_job_seeker
  system.name [attribute[string]]: Job Seeker Application
  system.description [attribute[string]]: AI-powered job application assistant for data scientists
  system.version [attribute[string]]: 1.0.0
  system.domains [array[reference→domain]]: [5 items]
    domain [type] (id: dom_job_matching)
      domain.id [attribute[string]]: dom_job_matching
      domain.name [attribute[string]]: Job Matching
      domain.type [attribute[enum: core, supporting, generic]]: core
      domain.description [attribute[string]]: Core domain for intelligently matching jobs to candidate profiles
      domain.strategic_importance [attribute[enum: critical, important, standard...]]: critical
      domain.bounded_contexts [array[reference→bounded_context]]: [3 items: bc_profile, bc_matching, bc_requirements]
        bounded_context [type] (id: bc_profile)
          bounded_context.id [attribute[string]]: bc_profile
          bounded_context.name [attribute[string]]: Profile Management
          bounded_context.domain_ref [reference→domain]: dom_job_matching
          bounded_context.description [attribute[string]]: Manages candidate profile including skills, experience, preferences
          bounded_context.ubiquitous_language [object]: {glossary}
            bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
              bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
              bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
              bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
          bounded_context.team_ownership [attribute[string]]: Core Matching Team
          bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_candidate_profile]
            aggregate [type] (id: agg_candidate_profile)
              aggregate.id [attribute[string]]: agg_candidate_profile
              aggregate.name [attribute[string]]: Candidate Profile
              aggregate.bounded_context_ref [reference→bounded_context]: bc_profile
              aggregate.root_ref [reference→entity]: ent_candidate
                entity [type] (id: ent_candidate)
                  entity.id [attribute[string]]: ent_candidate
                  entity.name [attribute[string]]: Candidate
                  entity.bounded_context_ref [reference→bounded_context]: bc_profile
                  entity.aggregate_ref [reference→aggregate]: agg_candidate_profile
                  entity.is_aggregate_root [attribute[boolean]]: True
                  entity.identity_field [attribute[string]]: candidate_id
                  entity.identity_generation [attribute[enum: user_provided, auto_generated, derived...]]: auto_generated
                  entity.attributes [array[object]]: [9 items]
                    entity.attributes.name [attribute[string]]: candidate_id
                    entity.attributes.type [attribute[string]]: CandidateId
                    entity.attributes.value_object_ref [reference→value_object]: vo_candidate_id
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: email
                    entity.attributes.type [attribute[string]]: Email
                    entity.attributes.value_object_ref [reference→value_object]: vo_email
                      value_object [type] (id: vo_email)
                        value_object.id [attribute[string]]: vo_email
                        value_object.name [attribute[string]]: Email
                        value_object.bounded_context_ref [reference→bounded_context]: bc_profile
                        value_object.description [attribute[string]]: Email address value object with validation
                        value_object.attributes [array[object]]: [1 items]
                          value_object.attributes.name [attribute[string]]: address
                          value_object.attributes.type [attribute[string]]: string
                          value_object.attributes.required [attribute[boolean]]: True
                          value_object.attributes.validation [attribute[string]]: RFC 5322 email format
                        value_object.validation_rules [array[string]]: [3 items: Must match email regex pattern, Must have @ symbol and domain, Normalized to lowercase]
                        value_object.equality_criteria [array[string]]: [1 items: address]
                        value_object.immutability [attribute[boolean]]: True
                        value_object.side_effect_free_methods [array[object]]: [2 items]
                          value_object.side_effect_free_methods.name [attribute[string]]: domain
                          value_object.side_effect_free_methods.description [attribute[string]]: Extract domain part
                          value_object.side_effect_free_methods.returns [attribute[string]]: string
                          value_object.side_effect_free_methods.name [attribute[string]]: localPart
                          value_object.side_effect_free_methods.description [attribute[string]]: Extract local part
                          value_object.side_effect_free_methods.returns [attribute[string]]: string
                        value_object.common_values [array[string]]: <not found>
                        value_object.entities [array[reference→entity]]: [3 items]
                          entity [type] (id: ent_job_posting)
                            entity.id [attribute[string]]: ent_job_posting
                            entity.name [attribute[string]]: Job Posting
                            entity.bounded_context_ref [reference→bounded_context]: bc_job_catalog
                              bounded_context [type] (id: bc_job_catalog)
                                bounded_context.id [attribute[string]]: bc_job_catalog
                                bounded_context.name [attribute[string]]: Job Catalog
                                bounded_context.domain_ref [reference→domain]: dom_job_aggregation
                                  domain [type] (id: dom_job_aggregation)
                                    domain.id [attribute[string]]: dom_job_aggregation
                                    domain.name [attribute[string]]: Job Aggregation
                                    domain.type [attribute[enum: core, supporting, generic]]: supporting
                                    domain.description [attribute[string]]: Aggregate jobs from various sources and normalize data
                                    domain.strategic_importance [attribute[enum: critical, important, standard...]]: important
                                    domain.bounded_contexts [array[reference→bounded_context]]: [2 items: bc_scrapers, bc_job_catalog]
                                      bounded_context [type] (id: bc_scrapers)
                                        bounded_context.id [attribute[string]]: bc_scrapers
                                        bounded_context.name [attribute[string]]: Job Scrapers
                                        bounded_context.domain_ref [reference→domain]: dom_job_aggregation
                                        bounded_context.description [attribute[string]]: Scrape jobs from external sources
                                        bounded_context.ubiquitous_language [object]: <not found>
                                          bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                            bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                            bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                            bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                        bounded_context.team_ownership [attribute[string]]: Aggregation Team
                                        bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_scraping_job]
                                        bounded_context.repositories [array[reference→repository]]: [1 items: repo_scraping_job]
                                        bounded_context.domain_services [array[reference→domain_service]]: [0 items]
                                        bounded_context.application_services [array[reference→application_service]]: [2 items: svc_app_schedule_scraping, svc_app_run_scraper]
                                        bounded_context.domain_events [array[reference→domain_event]]: [1 items: evt_scraping_completed]
                                        bounded_context.factories [array[reference→factory]]: [2 items]
                                          factory [type] (id: factory_candidate_profile)
                                            factory.id [attribute[string]]: factory_candidate_profile
                                            factory.name [attribute[string]]: CandidateProfileFactory
                                            factory.bounded_context_ref [reference→bounded_context]: bc_profile
                                            factory.creates_type [attribute[enum: entity, aggregate, value_object]]: aggregate
                                            factory.creates_ref [reference→None]: agg_candidate_profile
                                            factory.creation_methods [array[object]]: [2 items]
                                              factory.creation_methods.name [attribute[string]]: createFromResume
                                              factory.creation_methods.parameters [array]: [1 items: ResumeFile resume]
                                              factory.creation_methods.returns [attribute[string]]: CandidateProfile
                                              factory.creation_methods.description [attribute[string]]: Parse resume and create initial profile
                                              factory.creation_methods.name [attribute[string]]: createManual
                                              factory.creation_methods.parameters [array]: [2 items: Email email, PersonName name]
                                              factory.creation_methods.returns [attribute[string]]: CandidateProfile
                                              factory.creation_methods.description [attribute[string]]: Create empty profile for manual completion
                                            factory.location [attribute[enum: domain_layer, infrastructure_layer, on_aggregate]]: domain_layer
                                            factory.reconstitution [attribute[boolean]]: True
                                          factory [type] (id: factory_job_match)
                                            factory.id [attribute[string]]: factory_job_match
                                            factory.name [attribute[string]]: JobMatchFactory
                                            factory.bounded_context_ref [reference→bounded_context]: bc_matching
                                              bounded_context [type] (id: bc_matching)
                                                bounded_context.id [attribute[string]]: bc_matching
                                                bounded_context.name [attribute[string]]: Job Matching Engine
                                                bounded_context.domain_ref [reference→domain]: dom_job_matching
                                                bounded_context.description [attribute[string]]: Intelligent matching of jobs to candidate profiles
                                                bounded_context.ubiquitous_language [object]: {glossary}
                                                  bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                    bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                    bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                    bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                bounded_context.team_ownership [attribute[string]]: Core Matching Team
                                                bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_job_match]
                                                  aggregate [type] (id: agg_job_match)
                                                    aggregate.id [attribute[string]]: agg_job_match
                                                    aggregate.name [attribute[string]]: Job Match
                                                    aggregate.bounded_context_ref [reference→bounded_context]: bc_matching
                                                    aggregate.root_ref [reference→entity]: ent_job_match
                                                      entity [type] (id: ent_job_match)
                                                        entity.id [attribute[string]]: ent_job_match
                                                        entity.name [attribute[string]]: Job Match
                                                        entity.bounded_context_ref [reference→bounded_context]: bc_matching
                                                        entity.aggregate_ref [reference→aggregate]: agg_job_match
                                                        entity.is_aggregate_root [attribute[boolean]]: True
                                                        entity.identity_field [attribute[string]]: match_id
                                                        entity.identity_generation [attribute[enum: user_provided, auto_generated, derived...]]: auto_generated
                                                        entity.attributes [array[object]]: [7 items]
                                                          entity.attributes.name [attribute[string]]: match_id
                                                          entity.attributes.type [attribute[string]]: MatchId
                                                          entity.attributes.value_object_ref [reference→value_object]: <not found>
                                                            value_object [type] (id: ?)
                                                              value_object.id [attribute[string]]: <not found>
                                                              value_object.name [attribute[string]]: match_id
                                                              value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                                                bounded_context [type] (id: ?)
                                                                  bounded_context.id [attribute[string]]: <not found>
                                                                  bounded_context.name [attribute[string]]: match_id
                                                                  bounded_context.domain_ref [reference→domain]: <not found>
                                                                    domain [type] (id: ?)
                                                                      domain.id [attribute[string]]: <not found>
                                                                      domain.name [attribute[string]]: match_id
                                                                      domain.type [attribute[enum: core, supporting, generic]]: MatchId
                                                                      domain.description [attribute[string]]: <not found>
                                                                      domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                                                      domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                                                        bounded_context [type] (id: bc_requirements)
                                                                          bounded_context.id [attribute[string]]: bc_requirements
                                                                          bounded_context.name [attribute[string]]: Requirements Analysis
                                                                          bounded_context.domain_ref [reference→domain]: dom_job_matching
                                                                          bounded_context.description [attribute[string]]: Analyze and aggregate job requirements across postings
                                                                          bounded_context.ubiquitous_language [object]: {glossary}
                                                                            bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                              bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                              bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                              bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                          bounded_context.team_ownership [attribute[string]]: Core Matching Team
                                                                          bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_requirements_analysis]
                                                                            aggregate [type] (id: agg_requirements_analysis)
                                                                              aggregate.id [attribute[string]]: agg_requirements_analysis
                                                                              aggregate.name [attribute[string]]: Requirements Analysis
                                                                              aggregate.bounded_context_ref [reference→bounded_context]: bc_requirements
                                                                              aggregate.root_ref [reference→entity]: ent_requirements_analysis
                                                                              aggregate.entities [array[reference→entity]]: [2 items: ent_requirements_analysis, ent_requirement_frequency]
                                                                              aggregate.value_objects [array[reference→value_object]]: [3 items: vo_requirement, vo_frequency, vo_importance_score]
                                                                              aggregate.consistency_rules [array[string]]: [2 items: Analysis must be for specific candidate and time period, Requirements sorted by frequency]
                                                                              aggregate.invariants [array[string]]: [1 items: Analysis date <= Current date]
                                                                              aggregate.lifecycle_hooks [object]: <not found>
                                                                                aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                                                                                aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                                                                                aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
                                                                              aggregate.size_estimate [attribute[enum: small, medium, large]]: medium
                                                                              aggregate.repositories [array[reference→repository]]: [3 items]
                                                                                repository [type] (id: repo_profile)
                                                                                  repository.id [attribute[string]]: repo_profile
                                                                                  repository.name [attribute[string]]: ProfileRepository
                                                                                  repository.bounded_context_ref [reference→bounded_context]: bc_profile
                                                                                  repository.aggregate_ref [reference→aggregate]: agg_candidate_profile
                                                                                  repository.interface_methods [array[object]]: [4 items]
                                                                                    repository.interface_methods.name [attribute[string]]: save
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: CandidateProfile profile]
                                                                                    repository.interface_methods.returns [attribute[string]]: void
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                    repository.interface_methods.name [attribute[string]]: findById
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: CandidateId id]
                                                                                    repository.interface_methods.returns [attribute[string]]: Optional<CandidateProfile>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_id
                                                                                    repository.interface_methods.name [attribute[string]]: findByEmail
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: Email email]
                                                                                    repository.interface_methods.returns [attribute[string]]: Optional<CandidateProfile>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_criteria
                                                                                    repository.interface_methods.name [attribute[string]]: findIncompleteProfiles
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [0 items]
                                                                                    repository.interface_methods.returns [attribute[string]]: List<CandidateProfile>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                  repository.persistence_strategy [attribute[string]]: PostgreSQL with JPA
                                                                                  repository.implementation_notes [attribute[string]]: Uses Data Mapper pattern to separate domain model from persistence
                                                                                repository [type] (id: repo_job_posting)
                                                                                  repository.id [attribute[string]]: repo_job_posting
                                                                                  repository.name [attribute[string]]: JobPostingRepository
                                                                                  repository.bounded_context_ref [reference→bounded_context]: bc_job_catalog
                                                                                  repository.aggregate_ref [reference→aggregate]: agg_job_posting
                                                                                    aggregate [type] (id: agg_job_posting)
                                                                                      aggregate.id [attribute[string]]: agg_job_posting
                                                                                      aggregate.name [attribute[string]]: Job Posting
                                                                                      aggregate.bounded_context_ref [reference→bounded_context]: bc_job_catalog
                                                                                      aggregate.root_ref [reference→entity]: ent_job_posting
                                                                                      aggregate.entities [array[reference→entity]]: [1 items: ent_job_posting]
                                                                                      aggregate.value_objects [array[reference→value_object]]: [8 items: vo_job_id, vo_job_title, vo_company...]
                                                                                        value_object [type] (id: vo_location)
                                                                                          value_object.id [attribute[string]]: vo_location
                                                                                          value_object.name [attribute[string]]: Location
                                                                                          value_object.bounded_context_ref [reference→bounded_context]: bc_profile
                                                                                          value_object.description [attribute[string]]: Canadian location (city, province)
                                                                                          value_object.attributes [array[object]]: [3 items]
                                                                                            value_object.attributes.name [attribute[string]]: city
                                                                                            value_object.attributes.type [attribute[string]]: string
                                                                                            value_object.attributes.required [attribute[boolean]]: True
                                                                                            value_object.attributes.validation [attribute[string]]: <not found>
                                                                                            value_object.attributes.name [attribute[string]]: province
                                                                                            value_object.attributes.type [attribute[string]]: CanadianProvince
                                                                                            value_object.attributes.required [attribute[boolean]]: True
                                                                                            value_object.attributes.validation [attribute[string]]: <not found>
                                                                                            value_object.attributes.name [attribute[string]]: country
                                                                                            value_object.attributes.type [attribute[string]]: string
                                                                                            value_object.attributes.required [attribute[boolean]]: True
                                                                                            value_object.attributes.validation [attribute[string]]: Must be 'Canada'
                                                                                          value_object.validation_rules [array[string]]: [2 items: Province must be valid Canadian province code (ON, BC, QC, etc.), Country must be 'Canada']
                                                                                          value_object.equality_criteria [array[string]]: [3 items: city, province, country]
                                                                                          value_object.immutability [attribute[boolean]]: True
                                                                                          value_object.side_effect_free_methods [array[object]]: <not found>
                                                                                            value_object.side_effect_free_methods.name [attribute[string]]: Location
                                                                                            value_object.side_effect_free_methods.description [attribute[string]]: Canadian location (city, province)
                                                                                            value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                                                                          value_object.common_values [array[string]]: <not found>
                                                                                          value_object.entities [array[reference→entity]]: [3 items]
                                                                                      aggregate.consistency_rules [array[string]]: [2 items: Job must have title, company, and source, Job must not be duplicate (same title, company, location)]
                                                                                      aggregate.invariants [array[string]]: [2 items: Posted date <= Current date, Expiry date > Posted date]
                                                                                      aggregate.lifecycle_hooks [object]: <not found>
                                                                                        aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                                                                                        aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                                                                                        aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
                                                                                      aggregate.size_estimate [attribute[enum: small, medium, large]]: small
                                                                                      aggregate.repositories [array[reference→repository]]: [3 items]
                                                                                        repository [type] (id: repo_job_match)
                                                                                          repository.id [attribute[string]]: repo_job_match
                                                                                          repository.name [attribute[string]]: JobMatchRepository
                                                                                          repository.bounded_context_ref [reference→bounded_context]: bc_matching
                                                                                          repository.aggregate_ref [reference→aggregate]: agg_job_match
                                                                                          repository.interface_methods [array[object]]: [4 items]
                                                                                            repository.interface_methods.name [attribute[string]]: save
                                                                                            repository.interface_methods.description [attribute[string]]: <not found>
                                                                                            repository.interface_methods.parameters [array]: [1 items: JobMatch match]
                                                                                            repository.interface_methods.returns [attribute[string]]: void
                                                                                            repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                            repository.interface_methods.name [attribute[string]]: findByCandidate
                                                                                            repository.interface_methods.description [attribute[string]]: <not found>
                                                                                            repository.interface_methods.parameters [array]: [1 items: CandidateId candidateId]
                                                                                            repository.interface_methods.returns [attribute[string]]: List<JobMatch>
                                                                                            repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_criteria
                                                                                            repository.interface_methods.name [attribute[string]]: findHighMatches
                                                                                            repository.interface_methods.description [attribute[string]]: <not found>
                                                                                            repository.interface_methods.parameters [array]: [1 items: CandidateId candidateId]
                                                                                            repository.interface_methods.returns [attribute[string]]: List<JobMatch>
                                                                                            repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                            repository.interface_methods.name [attribute[string]]: findByJob
                                                                                            repository.interface_methods.description [attribute[string]]: <not found>
                                                                                            repository.interface_methods.parameters [array]: [1 items: JobId jobId]
                                                                                            repository.interface_methods.returns [attribute[string]]: List<JobMatch>
                                                                                            repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_criteria
                                                                                          repository.persistence_strategy [attribute[string]]: PostgreSQL
                                                                                          repository.implementation_notes [attribute[string]]: <not found>
                                                                                      aggregate.domain_events [array[reference→domain_event]]: [4 items]
                                                                                        domain_event [type] (id: evt_profile_updated)
                                                                                          domain_event.id [attribute[string]]: evt_profile_updated
                                                                                          domain_event.name [attribute[string]]: ProfileUpdated
                                                                                          domain_event.bounded_context_ref [reference→bounded_context]: bc_profile
                                                                                          domain_event.aggregate_ref [reference→aggregate]: agg_candidate_profile
                                                                                          domain_event.description [attribute[string]]: Candidate profile was updated
                                                                                          domain_event.data_carried [array[object]]: [3 items]
                                                                                            domain_event.data_carried.name [attribute[string]]: candidate_id
                                                                                            domain_event.data_carried.type [attribute[string]]: CandidateId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: updated_fields
                                                                                            domain_event.data_carried.type [attribute[string]]: Set<String>
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: occurred_at
                                                                                            domain_event.data_carried.type [attribute[string]]: DateTime
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                          domain_event.handlers [array[object]]: [2 items]
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_matching
                                                                                            domain_event.handlers.handler [attribute[string]]: RecalculateMatchesHandler
                                                                                            domain_event.handlers.action [attribute[string]]: Recalculate all matches for this candidate
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_requirements
                                                                                            domain_event.handlers.handler [attribute[string]]: UpdateRequirementsHandler
                                                                                            domain_event.handlers.action [attribute[string]]: Update requirements analysis
                                                                                          domain_event.immutable [attribute[boolean]]: True
                                                                                          domain_event.timestamp_included [attribute[boolean]]: True
                                                                                        domain_event [type] (id: evt_job_posted)
                                                                                          domain_event.id [attribute[string]]: evt_job_posted
                                                                                          domain_event.name [attribute[string]]: JobPosted
                                                                                          domain_event.bounded_context_ref [reference→bounded_context]: bc_job_catalog
                                                                                          domain_event.aggregate_ref [reference→aggregate]: agg_job_posting
                                                                                          domain_event.description [attribute[string]]: New job was posted to catalog
                                                                                          domain_event.data_carried [array[object]]: [4 items]
                                                                                            domain_event.data_carried.name [attribute[string]]: job_id
                                                                                            domain_event.data_carried.type [attribute[string]]: JobId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: title
                                                                                            domain_event.data_carried.type [attribute[string]]: JobTitle
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: location
                                                                                            domain_event.data_carried.type [attribute[string]]: Location
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: occurred_at
                                                                                            domain_event.data_carried.type [attribute[string]]: DateTime
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                          domain_event.handlers [array[object]]: [1 items]
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_matching
                                                                                            domain_event.handlers.handler [attribute[string]]: CalculateMatchesForNewJob
                                                                                            domain_event.handlers.action [attribute[string]]: Calculate matches for all eligible candidates
                                                                                          domain_event.immutable [attribute[boolean]]: True
                                                                                          domain_event.timestamp_included [attribute[boolean]]: True
                                                                                        domain_event [type] (id: evt_high_match_found)
                                                                                          domain_event.id [attribute[string]]: evt_high_match_found
                                                                                          domain_event.name [attribute[string]]: HighMatchFound
                                                                                          domain_event.bounded_context_ref [reference→bounded_context]: bc_matching
                                                                                          domain_event.aggregate_ref [reference→aggregate]: agg_job_match
                                                                                          domain_event.description [attribute[string]]: A high-quality match (score >= 80) was found
                                                                                          domain_event.data_carried [array[object]]: [5 items]
                                                                                            domain_event.data_carried.name [attribute[string]]: match_id
                                                                                            domain_event.data_carried.type [attribute[string]]: MatchId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: candidate_id
                                                                                            domain_event.data_carried.type [attribute[string]]: CandidateId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: job_id
                                                                                            domain_event.data_carried.type [attribute[string]]: JobId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: match_score
                                                                                            domain_event.data_carried.type [attribute[string]]: MatchScore
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: occurred_at
                                                                                            domain_event.data_carried.type [attribute[string]]: DateTime
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                          domain_event.handlers [array[object]]: [1 items]
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_notifications
                                                                                            domain_event.handlers.handler [attribute[string]]: NotifyHighMatch
                                                                                            domain_event.handlers.action [attribute[string]]: Send notification to candidate
                                                                                          domain_event.immutable [attribute[boolean]]: True
                                                                                          domain_event.timestamp_included [attribute[boolean]]: True
                                                                                        domain_event [type] (id: evt_application_submitted)
                                                                                          domain_event.id [attribute[string]]: evt_application_submitted
                                                                                          domain_event.name [attribute[string]]: ApplicationSubmitted
                                                                                          domain_event.bounded_context_ref [reference→bounded_context]: bc_applications
                                                                                            bounded_context [type] (id: bc_applications)
                                                                                              bounded_context.id [attribute[string]]: bc_applications
                                                                                              bounded_context.name [attribute[string]]: Application Tracking
                                                                                              bounded_context.domain_ref [reference→domain]: dom_application_tracking
                                                                                                domain [type] (id: dom_application_tracking)
                                                                                                  domain.id [attribute[string]]: dom_application_tracking
                                                                                                  domain.name [attribute[string]]: Application Tracking
                                                                                                  domain.type [attribute[enum: core, supporting, generic]]: supporting
                                                                                                  domain.description [attribute[string]]: Track job applications and their status
                                                                                                  domain.strategic_importance [attribute[enum: critical, important, standard...]]: standard
                                                                                                  domain.bounded_contexts [array[reference→bounded_context]]: [1 items: bc_applications]
                                                                                                  domain.investment_strategy [attribute[string]]: Simple implementation, standard patterns
                                                                                                  domain.notes [attribute[string]]: <not found>
                                                                                              bounded_context.description [attribute[string]]: Track job applications and their progress
                                                                                              bounded_context.ubiquitous_language [object]: <not found>
                                                                                                bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                                                  bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                                                  bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                                                  bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                                              bounded_context.team_ownership [attribute[string]]: Application Tracking Team
                                                                                              bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_job_application]
                                                                                                aggregate [type] (id: agg_job_application)
                                                                                                  aggregate.id [attribute[string]]: agg_job_application
                                                                                                  aggregate.name [attribute[string]]: Job Application
                                                                                                  aggregate.bounded_context_ref [reference→bounded_context]: bc_applications
                                                                                                  aggregate.root_ref [reference→entity]: ent_job_application
                                                                                                  aggregate.entities [array[reference→entity]]: [1 items: ent_job_application]
                                                                                                  aggregate.value_objects [array[reference→value_object]]: [4 items: vo_application_status, vo_application_date, vo_resume_version...]
                                                                                                  aggregate.consistency_rules [array[string]]: [2 items: Cannot apply to same job twice, Status transitions must be valid (applied → interviewing → offer/rejected)]
                                                                                                  aggregate.invariants [array[string]]: [1 items: Application references valid candidate and job]
                                                                                                  aggregate.lifecycle_hooks [object]: <not found>
                                                                                                    aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                                                                                                    aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                                                                                                    aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
                                                                                                  aggregate.size_estimate [attribute[enum: small, medium, large]]: small
                                                                                                  aggregate.repositories [array[reference→repository]]: [3 items]
                                                                                                  aggregate.domain_events [array[reference→domain_event]]: [4 items]
                                                                                              bounded_context.repositories [array[reference→repository]]: [1 items: repo_application]
                                                                                              bounded_context.domain_services [array[reference→domain_service]]: [0 items]
                                                                                              bounded_context.application_services [array[reference→application_service]]: [2 items: svc_app_submit_application, svc_app_update_status]
                                                                                                application_service [type] (id: svc_app_submit_application)
                                                                                                  application_service.id [attribute[string]]: svc_app_submit_application
                                                                                                  application_service.name [attribute[string]]: SubmitApplicationService
                                                                                                  application_service.bounded_context_ref [reference→bounded_context]: bc_applications
                                                                                                  application_service.use_case [attribute[string]]: Candidate submits application for a job
                                                                                                  application_service.orchestrates [array[object]]: [2 items]
                                                                                                    application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: aggregate
                                                                                                    application_service.orchestrates.ref [attribute[string]]: agg_job_application
                                                                                                    application_service.orchestrates.operation [attribute[string]]: create
                                                                                                    application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: repository
                                                                                                    application_service.orchestrates.ref [attribute[string]]: repo_application
                                                                                                    application_service.orchestrates.operation [attribute[string]]: save
                                                                                                  application_service.transaction_boundary [attribute[boolean]]: True
                                                                                                  application_service.publishes_events [array[reference→domain_event]]: [1 items: evt_application_submitted]
                                                                                                  application_service.authorization [attribute[string]]: Candidate must own the profile
                                                                                              bounded_context.domain_events [array[reference→domain_event]]: [2 items: evt_application_submitted, evt_application_status_changed]
                                                                                              bounded_context.factories [array[reference→factory]]: [2 items]
                                                                                              bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                                                value_object [type] (id: vo_skills)
                                                                                                  value_object.id [attribute[string]]: vo_skills
                                                                                                  value_object.name [attribute[string]]: Skills
                                                                                                  value_object.bounded_context_ref [reference→bounded_context]: bc_profile
                                                                                                  value_object.description [attribute[string]]: Collection of candidate skills with proficiency levels
                                                                                                  value_object.attributes [array[object]]: [2 items]
                                                                                                    value_object.attributes.name [attribute[string]]: technical_skills
                                                                                                    value_object.attributes.type [attribute[string]]: Map<SkillName, ProficiencyLevel>
                                                                                                    value_object.attributes.required [attribute[boolean]]: True
                                                                                                    value_object.attributes.validation [attribute[string]]: <not found>
                                                                                                    value_object.attributes.name [attribute[string]]: soft_skills
                                                                                                    value_object.attributes.type [attribute[string]]: Set<SkillName>
                                                                                                    value_object.attributes.required [attribute[boolean]]: False
                                                                                                    value_object.attributes.validation [attribute[string]]: <not found>
                                                                                                  value_object.validation_rules [array[string]]: [2 items: Technical skills map must not be empty, Proficiency levels must be: beginner, intermediate, advanced, expert]
                                                                                                  value_object.equality_criteria [array[string]]: [2 items: technical_skills, soft_skills]
                                                                                                  value_object.immutability [attribute[boolean]]: True
                                                                                                  value_object.side_effect_free_methods [array[object]]: [4 items]
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: hasSkill
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Check if skill exists
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: boolean
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: proficiencyFor
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Get proficiency for skill
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: ProficiencyLevel
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: addSkill
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Return new Skills with added skill
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: Skills
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: overlapWith
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Calculate overlap with other Skills
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: Percentage
                                                                                                  value_object.common_values [array[string]]: <not found>
                                                                                                  value_object.entities [array[reference→entity]]: [3 items]
                                                                                                value_object [type] (id: vo_match_score)
                                                                                                  value_object.id [attribute[string]]: vo_match_score
                                                                                                  value_object.name [attribute[string]]: MatchScore
                                                                                                  value_object.bounded_context_ref [reference→bounded_context]: bc_matching
                                                                                                  value_object.description [attribute[string]]: Calculated match score between 0 and 100
                                                                                                  value_object.attributes [array[object]]: [1 items]
                                                                                                    value_object.attributes.name [attribute[string]]: value
                                                                                                    value_object.attributes.type [attribute[string]]: int
                                                                                                    value_object.attributes.required [attribute[boolean]]: True
                                                                                                    value_object.attributes.validation [attribute[string]]: 0 <= value <= 100
                                                                                                  value_object.validation_rules [array[string]]: [1 items: Score must be between 0 and 100 inclusive]
                                                                                                  value_object.equality_criteria [array[string]]: [1 items: value]
                                                                                                  value_object.immutability [attribute[boolean]]: True
                                                                                                  value_object.side_effect_free_methods [array[object]]: [3 items]
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: isHighMatch
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Score >= 80
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: boolean
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: isMediumMatch
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: 50 <= Score < 80
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: boolean
                                                                                                    value_object.side_effect_free_methods.name [attribute[string]]: isLowMatch
                                                                                                    value_object.side_effect_free_methods.description [attribute[string]]: Score < 50
                                                                                                    value_object.side_effect_free_methods.returns [attribute[string]]: boolean
                                                                                                  value_object.common_values [array[string]]: [3 items: ZERO, PERFECT (100), MINIMUM_ACCEPTABLE (50)]
                                                                                                  value_object.entities [array[reference→entity]]: [3 items]
                                                                                              bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                                                context_mapping [type] (id: cm_profile_to_matching)
                                                                                                  context_mapping.id [attribute[string]]: cm_profile_to_matching
                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_profile
                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_matching
                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: customer_supplier
                                                                                                  context_mapping.integration_pattern [attribute[string]]: Domain events + Direct repository access
                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                  context_mapping.notes [attribute[string]]: Matching needs profile data. Profile team supports matching requirements.
                                                                                                context_mapping [type] (id: cm_job_catalog_to_matching)
                                                                                                  context_mapping.id [attribute[string]]: cm_job_catalog_to_matching
                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_job_catalog
                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_matching
                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: customer_supplier
                                                                                                  context_mapping.integration_pattern [attribute[string]]: Read-only repository access
                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                  context_mapping.notes [attribute[string]]: Matching reads jobs from catalog. Catalog team ensures data quality.
                                                                                                context_mapping [type] (id: cm_matching_to_requirements)
                                                                                                  context_mapping.id [attribute[string]]: cm_matching_to_requirements
                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_matching
                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_requirements
                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: partnership
                                                                                                  context_mapping.integration_pattern [attribute[string]]: Shared analysis, coordinated development
                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                  context_mapping.notes [attribute[string]]: Close collaboration needed. Both improve together.
                                                                                                context_mapping [type] (id: cm_requirements_to_skills)
                                                                                                  context_mapping.id [attribute[string]]: cm_requirements_to_skills
                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_requirements
                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_skills_analysis
                                                                                                    bounded_context [type] (id: bc_skills_analysis)
                                                                                                      bounded_context.id [attribute[string]]: bc_skills_analysis
                                                                                                      bounded_context.name [attribute[string]]: Skills Gap Analysis
                                                                                                      bounded_context.domain_ref [reference→domain]: dom_career_development
                                                                                                        domain [type] (id: dom_career_development)
                                                                                                          domain.id [attribute[string]]: dom_career_development
                                                                                                          domain.name [attribute[string]]: Career Development
                                                                                                          domain.type [attribute[enum: core, supporting, generic]]: supporting
                                                                                                          domain.description [attribute[string]]: Help candidates improve skills and close gaps
                                                                                                          domain.strategic_importance [attribute[enum: critical, important, standard...]]: important
                                                                                                          domain.bounded_contexts [array[reference→bounded_context]]: [2 items: bc_skills_analysis, bc_project_recommendations]
                                                                                                            bounded_context [type] (id: bc_project_recommendations)
                                                                                                              bounded_context.id [attribute[string]]: bc_project_recommendations
                                                                                                              bounded_context.name [attribute[string]]: Project Recommendations
                                                                                                              bounded_context.domain_ref [reference→domain]: dom_career_development
                                                                                                              bounded_context.description [attribute[string]]: Recommend portfolio projects to close skill gaps
                                                                                                              bounded_context.ubiquitous_language [object]: <not found>
                                                                                                                bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                                                                  bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                                                                  bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                                                                  bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                                                              bounded_context.team_ownership [attribute[string]]: Career Development Team
                                                                                                              bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_project_recommendation]
                                                                                                              bounded_context.repositories [array[reference→repository]]: [1 items: repo_project_recommendation]
                                                                                                              bounded_context.domain_services [array[reference→domain_service]]: [1 items: svc_dom_project_recommender]
                                                                                                              bounded_context.application_services [array[reference→application_service]]: [1 items: svc_app_get_project_ideas]
                                                                                                              bounded_context.domain_events [array[reference→domain_event]]: [1 items: evt_projects_recommended]
                                                                                                              bounded_context.factories [array[reference→factory]]: [2 items]
                                                                                                              bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                                                              bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                                                                context_mapping [type] (id: cm_skills_to_projects)
                                                                                                                  context_mapping.id [attribute[string]]: cm_skills_to_projects
                                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_skills_analysis
                                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_project_recommendations
                                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: customer_supplier
                                                                                                                  context_mapping.integration_pattern [attribute[string]]: API calls
                                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                                  context_mapping.notes [attribute[string]]: Project recommendations based on identified gaps.
                                                                                                                context_mapping [type] (id: cm_scrapers_to_catalog)
                                                                                                                  context_mapping.id [attribute[string]]: cm_scrapers_to_catalog
                                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_scrapers
                                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_job_catalog
                                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: customer_supplier
                                                                                                                  context_mapping.integration_pattern [attribute[string]]: Message queue (async)
                                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                                  context_mapping.notes [attribute[string]]: Scrapers publish jobs, catalog ingests and normalizes.
                                                                                                                context_mapping [type] (id: cm_matching_to_notifications)
                                                                                                                  context_mapping.id [attribute[string]]: cm_matching_to_notifications
                                                                                                                  context_mapping.upstream_context [reference→bounded_context]: bc_matching
                                                                                                                  context_mapping.downstream_context [reference→bounded_context]: bc_notifications
                                                                                                                    bounded_context [type] (id: bc_notifications)
                                                                                                                      bounded_context.id [attribute[string]]: bc_notifications
                                                                                                                      bounded_context.name [attribute[string]]: Notifications
                                                                                                                      bounded_context.domain_ref [reference→domain]: dom_notifications
                                                                                                                        domain [type] (id: dom_notifications)
                                                                                                                          domain.id [attribute[string]]: dom_notifications
                                                                                                                          domain.name [attribute[string]]: Notifications
                                                                                                                          domain.type [attribute[enum: core, supporting, generic]]: generic
                                                                                                                          domain.description [attribute[string]]: Send notifications to users
                                                                                                                          domain.strategic_importance [attribute[enum: critical, important, standard...]]: low
                                                                                                                          domain.bounded_contexts [array[reference→bounded_context]]: [1 items: bc_notifications]
                                                                                                                          domain.investment_strategy [attribute[string]]: Use third-party service (SendGrid, Twilio)
                                                                                                                          domain.notes [attribute[string]]: <not found>
                                                                                                                      bounded_context.description [attribute[string]]: Send email, SMS, push notifications
                                                                                                                      bounded_context.ubiquitous_language [object]: <not found>
                                                                                                                        bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                                                                          bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                                                                          bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                                                                          bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                                                                      bounded_context.team_ownership [attribute[string]]: Infrastructure Team
                                                                                                                      bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_notification]
                                                                                                                      bounded_context.repositories [array[reference→repository]]: [1 items: repo_notification]
                                                                                                                      bounded_context.domain_services [array[reference→domain_service]]: [0 items]
                                                                                                                      bounded_context.application_services [array[reference→application_service]]: [1 items: svc_app_send_notification]
                                                                                                                      bounded_context.domain_events [array[reference→domain_event]]: [1 items: evt_notification_sent]
                                                                                                                      bounded_context.factories [array[reference→factory]]: [2 items]
                                                                                                                      bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                                                                      bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                                                                        context_mapping [type] (id: cm_applications_to_notifications)
                                                                                                                          context_mapping.id [attribute[string]]: cm_applications_to_notifications
                                                                                                                          context_mapping.upstream_context [reference→bounded_context]: bc_applications
                                                                                                                          context_mapping.downstream_context [reference→bounded_context]: bc_notifications
                                                                                                                          context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: conformist
                                                                                                                          context_mapping.integration_pattern [attribute[string]]: Third-party service API
                                                                                                                          context_mapping.translation_map [object]: <not found>
                                                                                                                          context_mapping.shared_elements [array[string]]: <not found>
                                                                                                                          context_mapping.acl_details [object]: <not found>
                                                                                                                            context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                                            context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                                            context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                                          context_mapping.notes [attribute[string]]: Application updates trigger notifications.
                                                                                                                      bounded_context.entities [array[reference→entity]]: [3 items]
                                                                                                                      bounded_context.specifications [array[reference→specification]]: <not found>
                                                                                                                        specification [type] (id: bc_notifications)
                                                                                                                          specification.id [attribute[string]]: bc_notifications
                                                                                                                          specification.name [attribute[string]]: Notifications
                                                                                                                          specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                                                                          specification.applies_to [reference→None]: <not found>
                                                                                                                          specification.rule [attribute[string]]: <not found>
                                                                                                                          specification.composable [attribute[boolean]]: <not found>
                                                                                                                          specification.use_cases [array[string]]: <not found>
                                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: conformist
                                                                                                                  context_mapping.integration_pattern [attribute[string]]: Third-party service API
                                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                                  context_mapping.notes [attribute[string]]: Notifications uses SendGrid. Matching conforms to their API.
                                                                                                              bounded_context.entities [array[reference→entity]]: [3 items]
                                                                                                              bounded_context.specifications [array[reference→specification]]: <not found>
                                                                                                                specification [type] (id: bc_project_recommendations)
                                                                                                                  specification.id [attribute[string]]: bc_project_recommendations
                                                                                                                  specification.name [attribute[string]]: Project Recommendations
                                                                                                                  specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                                                                  specification.applies_to [reference→None]: <not found>
                                                                                                                  specification.rule [attribute[string]]: <not found>
                                                                                                                  specification.composable [attribute[boolean]]: <not found>
                                                                                                                  specification.use_cases [array[string]]: <not found>
                                                                                                          domain.investment_strategy [attribute[string]]: Adequate quality, focus on actionable insights
                                                                                                          domain.notes [attribute[string]]: <not found>
                                                                                                      bounded_context.description [attribute[string]]: Identify skill gaps and prioritize learning
                                                                                                      bounded_context.ubiquitous_language [object]: <not found>
                                                                                                        bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                                                          bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                                                          bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                                                          bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                                                      bounded_context.team_ownership [attribute[string]]: Career Development Team
                                                                                                      bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_skills_gap_report]
                                                                                                        aggregate [type] (id: agg_skills_gap_report)
                                                                                                          aggregate.id [attribute[string]]: agg_skills_gap_report
                                                                                                          aggregate.name [attribute[string]]: Skills Gap Report
                                                                                                          aggregate.bounded_context_ref [reference→bounded_context]: bc_skills_analysis
                                                                                                          aggregate.root_ref [reference→entity]: ent_skills_gap_report
                                                                                                          aggregate.entities [array[reference→entity]]: [2 items: ent_skills_gap_report, ent_skill_gap]
                                                                                                          aggregate.value_objects [array[reference→value_object]]: [3 items: vo_skill, vo_gap_severity, vo_learning_priority]
                                                                                                          aggregate.consistency_rules [array[string]]: [2 items: Gaps identified from requirements analysis, Priority based on frequency and importance]
                                                                                                          aggregate.invariants [array[string]]: [1 items: Report is for specific candidate]
                                                                                                          aggregate.lifecycle_hooks [object]: <not found>
                                                                                                            aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                                                                                                            aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                                                                                                            aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
                                                                                                          aggregate.size_estimate [attribute[enum: small, medium, large]]: small
                                                                                                          aggregate.repositories [array[reference→repository]]: [3 items]
                                                                                                          aggregate.domain_events [array[reference→domain_event]]: [4 items]
                                                                                                      bounded_context.repositories [array[reference→repository]]: [1 items: repo_skills_gap]
                                                                                                      bounded_context.domain_services [array[reference→domain_service]]: [2 items: svc_dom_gap_identifier, svc_dom_priority_ranker]
                                                                                                      bounded_context.application_services [array[reference→application_service]]: [1 items: svc_app_generate_gap_report]
                                                                                                      bounded_context.domain_events [array[reference→domain_event]]: [2 items: evt_gap_identified, evt_skill_acquired]
                                                                                                      bounded_context.factories [array[reference→factory]]: [2 items]
                                                                                                      bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                                                      bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                                                      bounded_context.entities [array[reference→entity]]: [3 items]
                                                                                                      bounded_context.specifications [array[reference→specification]]: <not found>
                                                                                                        specification [type] (id: bc_skills_analysis)
                                                                                                          specification.id [attribute[string]]: bc_skills_analysis
                                                                                                          specification.name [attribute[string]]: Skills Gap Analysis
                                                                                                          specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                                                          specification.applies_to [reference→None]: <not found>
                                                                                                          specification.rule [attribute[string]]: <not found>
                                                                                                          specification.composable [attribute[boolean]]: <not found>
                                                                                                          specification.use_cases [array[string]]: <not found>
                                                                                                  context_mapping.relationship_type [attribute[enum: partnership, shared_kernel, customer_supplier...]]: customer_supplier
                                                                                                  context_mapping.integration_pattern [attribute[string]]: Domain events
                                                                                                  context_mapping.translation_map [object]: <not found>
                                                                                                  context_mapping.shared_elements [array[string]]: <not found>
                                                                                                  context_mapping.acl_details [object]: <not found>
                                                                                                    context_mapping.acl_details.facades [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.adapters [array[string]]: <not found>
                                                                                                    context_mapping.acl_details.translators [array[string]]: <not found>
                                                                                                  context_mapping.notes [attribute[string]]: Skills analysis reacts to requirement analysis completion.
                                                                                              bounded_context.entities [array[reference→entity]]: [3 items]
                                                                                              bounded_context.specifications [array[reference→specification]]: <not found>
                                                                                                specification [type] (id: bc_applications)
                                                                                                  specification.id [attribute[string]]: bc_applications
                                                                                                  specification.name [attribute[string]]: Application Tracking
                                                                                                  specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                                                  specification.applies_to [reference→None]: <not found>
                                                                                                  specification.rule [attribute[string]]: <not found>
                                                                                                  specification.composable [attribute[boolean]]: <not found>
                                                                                                  specification.use_cases [array[string]]: <not found>
                                                                                          domain_event.aggregate_ref [reference→aggregate]: agg_job_application
                                                                                          domain_event.description [attribute[string]]: Candidate submitted job application
                                                                                          domain_event.data_carried [array[object]]: [4 items]
                                                                                            domain_event.data_carried.name [attribute[string]]: application_id
                                                                                            domain_event.data_carried.type [attribute[string]]: ApplicationId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: candidate_id
                                                                                            domain_event.data_carried.type [attribute[string]]: CandidateId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: job_id
                                                                                            domain_event.data_carried.type [attribute[string]]: JobId
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                            domain_event.data_carried.name [attribute[string]]: submitted_at
                                                                                            domain_event.data_carried.type [attribute[string]]: DateTime
                                                                                            domain_event.data_carried.description [attribute[string]]: <not found>
                                                                                          domain_event.handlers [array[object]]: [2 items]
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_notifications
                                                                                            domain_event.handlers.handler [attribute[string]]: SendConfirmation
                                                                                            domain_event.handlers.action [attribute[string]]: Send confirmation email
                                                                                            domain_event.handlers.bounded_context [attribute[string]]: bc_matching
                                                                                            domain_event.handlers.handler [attribute[string]]: UpdateMatchStatus
                                                                                            domain_event.handlers.action [attribute[string]]: Mark job as applied
                                                                                          domain_event.immutable [attribute[boolean]]: True
                                                                                          domain_event.timestamp_included [attribute[boolean]]: True
                                                                                  repository.interface_methods [array[object]]: [5 items]
                                                                                    repository.interface_methods.name [attribute[string]]: save
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: JobPosting job]
                                                                                    repository.interface_methods.returns [attribute[string]]: void
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                    repository.interface_methods.name [attribute[string]]: findById
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: JobId id]
                                                                                    repository.interface_methods.returns [attribute[string]]: Optional<JobPosting>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_id
                                                                                    repository.interface_methods.name [attribute[string]]: findActive
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [0 items]
                                                                                    repository.interface_methods.returns [attribute[string]]: List<JobPosting>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: custom
                                                                                    repository.interface_methods.name [attribute[string]]: findByLocation
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: Location location]
                                                                                    repository.interface_methods.returns [attribute[string]]: List<JobPosting>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_criteria
                                                                                    repository.interface_methods.name [attribute[string]]: findPostedAfter
                                                                                    repository.interface_methods.description [attribute[string]]: <not found>
                                                                                    repository.interface_methods.parameters [array]: [1 items: Date date]
                                                                                    repository.interface_methods.returns [attribute[string]]: List<JobPosting>
                                                                                    repository.interface_methods.query_type [attribute[enum: by_id, by_criteria, all...]]: by_criteria
                                                                                  repository.persistence_strategy [attribute[string]]: PostgreSQL with pgvector for semantic search
                                                                                  repository.implementation_notes [attribute[string]]: Job embeddings stored for similarity matching
                                                                              aggregate.domain_events [array[reference→domain_event]]: [4 items]
                                                                          bounded_context.repositories [array[reference→repository]]: [1 items: repo_requirements_analysis]
                                                                          bounded_context.domain_services [array[reference→domain_service]]: [2 items: svc_dom_requirement_extractor, svc_dom_aggregator]
                                                                            domain_service [type] (id: svc_dom_requirement_extractor)
                                                                              domain_service.id [attribute[string]]: svc_dom_requirement_extractor
                                                                              domain_service.name [attribute[string]]: RequirementExtractor
                                                                              domain_service.bounded_context_ref [reference→bounded_context]: bc_requirements
                                                                              domain_service.description [attribute[string]]: Extracts structured requirements from job descriptions using NLP
                                                                              domain_service.operations [array[object]]: [1 items]
                                                                                domain_service.operations.name [attribute[string]]: extract
                                                                                domain_service.operations.description [attribute[string]]: Extract requirements from job description
                                                                                domain_service.operations.parameters [array]: [1 items: JobDescription description]
                                                                                domain_service.operations.returns [attribute[string]]: Requirements
                                                                                domain_service.operations.involves_aggregates [array]: <not found>
                                                                                domain_service.operations.business_logic [attribute[string]]: NLP-based extraction of skills, years of experience, education level, certifications
                                                                              domain_service.dependencies [array[object]]: <not found>
                                                                                domain_service.dependencies.type [attribute[enum: repository, domain_service, specification]]: <not found>
                                                                                domain_service.dependencies.ref [attribute[string]]: <not found>
                                                                              domain_service.stateless [attribute[boolean]]: True
                                                                          bounded_context.application_services [array[reference→application_service]]: [1 items: svc_app_analyze_requirements]
                                                                          bounded_context.domain_events [array[reference→domain_event]]: [1 items: evt_analysis_completed]
                                                                          bounded_context.factories [array[reference→factory]]: [2 items]
                                                                          bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                          bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                          bounded_context.entities [array[reference→entity]]: [3 items]
                                                                          bounded_context.specifications [array[reference→specification]]: <not found>
                                                                            specification [type] (id: bc_requirements)
                                                                              specification.id [attribute[string]]: bc_requirements
                                                                              specification.name [attribute[string]]: Requirements Analysis
                                                                              specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                              specification.applies_to [reference→None]: <not found>
                                                                              specification.rule [attribute[string]]: <not found>
                                                                              specification.composable [attribute[boolean]]: <not found>
                                                                              specification.use_cases [array[string]]: <not found>
                                                                      domain.investment_strategy [attribute[string]]: <not found>
                                                                      domain.notes [attribute[string]]: <not found>
                                                                  bounded_context.description [attribute[string]]: <not found>
                                                                  bounded_context.ubiquitous_language [object]: <not found>
                                                                    bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                  bounded_context.team_ownership [attribute[string]]: <not found>
                                                                  bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                                                  bounded_context.repositories [array[reference→repository]]: [3 items]
                                                                  bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                                                    domain_service [type] (id: svc_dom_matching_engine)
                                                                      domain_service.id [attribute[string]]: svc_dom_matching_engine
                                                                      domain_service.name [attribute[string]]: MatchingEngine
                                                                      domain_service.bounded_context_ref [reference→bounded_context]: bc_matching
                                                                      domain_service.description [attribute[string]]: Core algorithm for calculating job-candidate match scores
                                                                      domain_service.operations [array[object]]: [2 items]
                                                                        domain_service.operations.name [attribute[string]]: calculateMatch
                                                                        domain_service.operations.description [attribute[string]]: Calculate match between candidate and job
                                                                        domain_service.operations.parameters [array]: [2 items: Candidate candidate, JobPosting job]
                                                                        domain_service.operations.returns [attribute[string]]: JobMatch
                                                                        domain_service.operations.involves_aggregates [array]: [2 items: agg_candidate_profile, agg_job_posting]
                                                                        domain_service.operations.business_logic [attribute[string]]: Multi-criteria weighted scoring: skills (40%), experience (25%), education (20%), location (10%), do...
                                                                        domain_service.operations.name [attribute[string]]: findBestMatches
                                                                        domain_service.operations.description [attribute[string]]: Find top N matches for candidate
                                                                        domain_service.operations.parameters [array]: [2 items: CandidateId candidateId, int limit]
                                                                        domain_service.operations.returns [attribute[string]]: List<JobMatch>
                                                                        domain_service.operations.involves_aggregates [array]: [1 items: agg_job_match]
                                                                        domain_service.operations.business_logic [attribute[string]]: Returns matches sorted by score, filtered by minimum threshold
                                                                      domain_service.dependencies [array[object]]: [2 items]
                                                                        domain_service.dependencies.type [attribute[enum: repository, domain_service, specification]]: repository
                                                                        domain_service.dependencies.ref [attribute[string]]: repo_profile
                                                                        domain_service.dependencies.type [attribute[enum: repository, domain_service, specification]]: repository
                                                                        domain_service.dependencies.ref [attribute[string]]: repo_job_posting
                                                                      domain_service.stateless [attribute[boolean]]: True
                                                                    domain_service [type] (id: svc_dom_deduplication)
                                                                      domain_service.id [attribute[string]]: svc_dom_deduplication
                                                                      domain_service.name [attribute[string]]: JobDeduplicationService
                                                                      domain_service.bounded_context_ref [reference→bounded_context]: bc_job_catalog
                                                                      domain_service.description [attribute[string]]: Identifies and merges duplicate job postings from different sources
                                                                      domain_service.operations [array[object]]: [2 items]
                                                                        domain_service.operations.name [attribute[string]]: isDuplicate
                                                                        domain_service.operations.description [attribute[string]]: Check if two jobs are the same
                                                                        domain_service.operations.parameters [array]: [2 items: JobPosting job1, JobPosting job2]
                                                                        domain_service.operations.returns [attribute[string]]: boolean
                                                                        domain_service.operations.involves_aggregates [array]: <not found>
                                                                        domain_service.operations.business_logic [attribute[string]]: Fuzzy matching on title + company + location; similarity threshold 85%
                                                                        domain_service.operations.name [attribute[string]]: mergeDuplicates
                                                                        domain_service.operations.description [attribute[string]]: Merge multiple postings of same job
                                                                        domain_service.operations.parameters [array]: [1 items: List<JobPosting> duplicates]
                                                                        domain_service.operations.returns [attribute[string]]: JobPosting
                                                                        domain_service.operations.involves_aggregates [array]: <not found>
                                                                        domain_service.operations.business_logic [attribute[string]]: Keep most recent, aggregate sources, prefer higher quality data
                                                                      domain_service.dependencies [array[object]]: <not found>
                                                                        domain_service.dependencies.type [attribute[enum: repository, domain_service, specification]]: <not found>
                                                                        domain_service.dependencies.ref [attribute[string]]: <not found>
                                                                      domain_service.stateless [attribute[boolean]]: True
                                                                  bounded_context.application_services [array[reference→application_service]]: [3 items]
                                                                    application_service [type] (id: svc_app_update_profile)
                                                                      application_service.id [attribute[string]]: svc_app_update_profile
                                                                      application_service.name [attribute[string]]: UpdateProfileService
                                                                      application_service.bounded_context_ref [reference→bounded_context]: bc_profile
                                                                      application_service.use_case [attribute[string]]: Candidate updates their profile
                                                                      application_service.orchestrates [array[object]]: [2 items]
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: repository
                                                                        application_service.orchestrates.ref [attribute[string]]: repo_profile
                                                                        application_service.orchestrates.operation [attribute[string]]: findById, save
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: aggregate
                                                                        application_service.orchestrates.ref [attribute[string]]: agg_candidate_profile
                                                                        application_service.orchestrates.operation [attribute[string]]: updateSkills, calculateCompleteness
                                                                      application_service.transaction_boundary [attribute[boolean]]: True
                                                                      application_service.publishes_events [array[reference→domain_event]]: [1 items: evt_profile_updated]
                                                                      application_service.authorization [attribute[string]]: Only the candidate can update their own profile
                                                                    application_service [type] (id: svc_app_calculate_matches)
                                                                      application_service.id [attribute[string]]: svc_app_calculate_matches
                                                                      application_service.name [attribute[string]]: CalculateMatchesService
                                                                      application_service.bounded_context_ref [reference→bounded_context]: bc_matching
                                                                      application_service.use_case [attribute[string]]: Calculate matches for all new jobs or updated profile
                                                                      application_service.orchestrates [array[object]]: [4 items]
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: repository
                                                                        application_service.orchestrates.ref [attribute[string]]: repo_profile
                                                                        application_service.orchestrates.operation [attribute[string]]: findById
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: repository
                                                                        application_service.orchestrates.ref [attribute[string]]: repo_job_posting
                                                                        application_service.orchestrates.operation [attribute[string]]: findActive
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: domain_service
                                                                        application_service.orchestrates.ref [attribute[string]]: svc_dom_matching_engine
                                                                        application_service.orchestrates.operation [attribute[string]]: calculateMatch
                                                                        application_service.orchestrates.type [attribute[enum: aggregate, domain_service, repository]]: repository
                                                                        application_service.orchestrates.ref [attribute[string]]: repo_job_match
                                                                        application_service.orchestrates.operation [attribute[string]]: save
                                                                      application_service.transaction_boundary [attribute[boolean]]: True
                                                                      application_service.publishes_events [array[reference→domain_event]]: [2 items: evt_match_calculated, evt_high_match_found]
                                                                      application_service.authorization [attribute[string]]: <not found>
                                                                  bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                                                  bounded_context.factories [array[reference→factory]]: [2 items]
                                                                  bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                  bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                  bounded_context.entities [array[reference→entity]]: [3 items]
                                                                  bounded_context.specifications [array[reference→specification]]: <not found>
                                                                    specification [type] (id: ?)
                                                                      specification.id [attribute[string]]: <not found>
                                                                      specification.name [attribute[string]]: match_id
                                                                      specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                      specification.applies_to [reference→None]: <not found>
                                                                      specification.rule [attribute[string]]: <not found>
                                                                      specification.composable [attribute[boolean]]: <not found>
                                                                      specification.use_cases [array[string]]: <not found>
                                                              value_object.description [attribute[string]]: <not found>
                                                              value_object.attributes [array[object]]: <not found>
                                                                value_object.attributes.name [attribute[string]]: match_id
                                                                value_object.attributes.type [attribute[string]]: MatchId
                                                                value_object.attributes.required [attribute[boolean]]: True
                                                                value_object.attributes.validation [attribute[string]]: <not found>
                                                              value_object.validation_rules [array[string]]: <not found>
                                                              value_object.equality_criteria [array[string]]: <not found>
                                                              value_object.immutability [attribute[boolean]]: <not found>
                                                              value_object.side_effect_free_methods [array[object]]: <not found>
                                                                value_object.side_effect_free_methods.name [attribute[string]]: match_id
                                                                value_object.side_effect_free_methods.description [attribute[string]]: <not found>
                                                                value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                                              value_object.common_values [array[string]]: <not found>
                                                              value_object.entities [array[reference→entity]]: [3 items]
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: <not found>
                                                          entity.attributes.name [attribute[string]]: candidate_id
                                                          entity.attributes.type [attribute[string]]: CandidateId
                                                          entity.attributes.value_object_ref [reference→value_object]: <not found>
                                                            value_object [type] (id: ?)
                                                              value_object.id [attribute[string]]: <not found>
                                                              value_object.name [attribute[string]]: candidate_id
                                                              value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                                                bounded_context [type] (id: ?)
                                                                  bounded_context.id [attribute[string]]: <not found>
                                                                  bounded_context.name [attribute[string]]: candidate_id
                                                                  bounded_context.domain_ref [reference→domain]: <not found>
                                                                    domain [type] (id: ?)
                                                                      domain.id [attribute[string]]: <not found>
                                                                      domain.name [attribute[string]]: candidate_id
                                                                      domain.type [attribute[enum: core, supporting, generic]]: CandidateId
                                                                      domain.description [attribute[string]]: Reference by ID only
                                                                      domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                                                      domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                                                      domain.investment_strategy [attribute[string]]: <not found>
                                                                      domain.notes [attribute[string]]: <not found>
                                                                  bounded_context.description [attribute[string]]: Reference by ID only
                                                                  bounded_context.ubiquitous_language [object]: <not found>
                                                                    bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                  bounded_context.team_ownership [attribute[string]]: <not found>
                                                                  bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                                                  bounded_context.repositories [array[reference→repository]]: [3 items]
                                                                  bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                                                  bounded_context.application_services [array[reference→application_service]]: [3 items]
                                                                  bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                                                  bounded_context.factories [array[reference→factory]]: [2 items]
                                                                  bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                  bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                  bounded_context.entities [array[reference→entity]]: [3 items]
                                                                  bounded_context.specifications [array[reference→specification]]: <not found>
                                                                    specification [type] (id: ?)
                                                                      specification.id [attribute[string]]: <not found>
                                                                      specification.name [attribute[string]]: candidate_id
                                                                      specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                      specification.applies_to [reference→None]: <not found>
                                                                      specification.rule [attribute[string]]: <not found>
                                                                      specification.composable [attribute[boolean]]: <not found>
                                                                      specification.use_cases [array[string]]: <not found>
                                                              value_object.description [attribute[string]]: Reference by ID only
                                                              value_object.attributes [array[object]]: <not found>
                                                                value_object.attributes.name [attribute[string]]: candidate_id
                                                                value_object.attributes.type [attribute[string]]: CandidateId
                                                                value_object.attributes.required [attribute[boolean]]: True
                                                                value_object.attributes.validation [attribute[string]]: <not found>
                                                              value_object.validation_rules [array[string]]: <not found>
                                                              value_object.equality_criteria [array[string]]: <not found>
                                                              value_object.immutability [attribute[boolean]]: <not found>
                                                              value_object.side_effect_free_methods [array[object]]: <not found>
                                                                value_object.side_effect_free_methods.name [attribute[string]]: candidate_id
                                                                value_object.side_effect_free_methods.description [attribute[string]]: Reference by ID only
                                                                value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                                              value_object.common_values [array[string]]: <not found>
                                                              value_object.entities [array[reference→entity]]: [3 items]
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: Reference by ID only
                                                          entity.attributes.name [attribute[string]]: job_id
                                                          entity.attributes.type [attribute[string]]: JobId
                                                          entity.attributes.value_object_ref [reference→value_object]: <not found>
                                                            value_object [type] (id: ?)
                                                              value_object.id [attribute[string]]: <not found>
                                                              value_object.name [attribute[string]]: job_id
                                                              value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                                                bounded_context [type] (id: ?)
                                                                  bounded_context.id [attribute[string]]: <not found>
                                                                  bounded_context.name [attribute[string]]: job_id
                                                                  bounded_context.domain_ref [reference→domain]: <not found>
                                                                    domain [type] (id: ?)
                                                                      domain.id [attribute[string]]: <not found>
                                                                      domain.name [attribute[string]]: job_id
                                                                      domain.type [attribute[enum: core, supporting, generic]]: JobId
                                                                      domain.description [attribute[string]]: Reference by ID only
                                                                      domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                                                      domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                                                      domain.investment_strategy [attribute[string]]: <not found>
                                                                      domain.notes [attribute[string]]: <not found>
                                                                  bounded_context.description [attribute[string]]: Reference by ID only
                                                                  bounded_context.ubiquitous_language [object]: <not found>
                                                                    bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                  bounded_context.team_ownership [attribute[string]]: <not found>
                                                                  bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                                                  bounded_context.repositories [array[reference→repository]]: [3 items]
                                                                  bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                                                  bounded_context.application_services [array[reference→application_service]]: [3 items]
                                                                  bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                                                  bounded_context.factories [array[reference→factory]]: [2 items]
                                                                  bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                  bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                  bounded_context.entities [array[reference→entity]]: [3 items]
                                                                  bounded_context.specifications [array[reference→specification]]: <not found>
                                                                    specification [type] (id: ?)
                                                                      specification.id [attribute[string]]: <not found>
                                                                      specification.name [attribute[string]]: job_id
                                                                      specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                      specification.applies_to [reference→None]: <not found>
                                                                      specification.rule [attribute[string]]: <not found>
                                                                      specification.composable [attribute[boolean]]: <not found>
                                                                      specification.use_cases [array[string]]: <not found>
                                                              value_object.description [attribute[string]]: Reference by ID only
                                                              value_object.attributes [array[object]]: <not found>
                                                                value_object.attributes.name [attribute[string]]: job_id
                                                                value_object.attributes.type [attribute[string]]: JobId
                                                                value_object.attributes.required [attribute[boolean]]: True
                                                                value_object.attributes.validation [attribute[string]]: <not found>
                                                              value_object.validation_rules [array[string]]: <not found>
                                                              value_object.equality_criteria [array[string]]: <not found>
                                                              value_object.immutability [attribute[boolean]]: <not found>
                                                              value_object.side_effect_free_methods [array[object]]: <not found>
                                                                value_object.side_effect_free_methods.name [attribute[string]]: job_id
                                                                value_object.side_effect_free_methods.description [attribute[string]]: Reference by ID only
                                                                value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                                              value_object.common_values [array[string]]: <not found>
                                                              value_object.entities [array[reference→entity]]: [3 items]
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: Reference by ID only
                                                          entity.attributes.name [attribute[string]]: match_score
                                                          entity.attributes.type [attribute[string]]: MatchScore
                                                          entity.attributes.value_object_ref [reference→value_object]: vo_match_score
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: <not found>
                                                          entity.attributes.name [attribute[string]]: match_tier
                                                          entity.attributes.type [attribute[string]]: MatchTier
                                                          entity.attributes.value_object_ref [reference→value_object]: vo_match_tier
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: <not found>
                                                          entity.attributes.name [attribute[string]]: criteria_scores
                                                          entity.attributes.type [attribute[string]]: CriteriaScores
                                                          entity.attributes.value_object_ref [reference→value_object]: vo_match_criteria_scores
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: <not found>
                                                          entity.attributes.name [attribute[string]]: calculated_at
                                                          entity.attributes.type [attribute[string]]: DateTime
                                                          entity.attributes.value_object_ref [reference→value_object]: <not found>
                                                            value_object [type] (id: ?)
                                                              value_object.id [attribute[string]]: <not found>
                                                              value_object.name [attribute[string]]: calculated_at
                                                              value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                                                bounded_context [type] (id: ?)
                                                                  bounded_context.id [attribute[string]]: <not found>
                                                                  bounded_context.name [attribute[string]]: calculated_at
                                                                  bounded_context.domain_ref [reference→domain]: <not found>
                                                                    domain [type] (id: ?)
                                                                      domain.id [attribute[string]]: <not found>
                                                                      domain.name [attribute[string]]: calculated_at
                                                                      domain.type [attribute[enum: core, supporting, generic]]: DateTime
                                                                      domain.description [attribute[string]]: <not found>
                                                                      domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                                                      domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                                                      domain.investment_strategy [attribute[string]]: <not found>
                                                                      domain.notes [attribute[string]]: <not found>
                                                                  bounded_context.description [attribute[string]]: <not found>
                                                                  bounded_context.ubiquitous_language [object]: <not found>
                                                                    bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                                                      bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                                                  bounded_context.team_ownership [attribute[string]]: <not found>
                                                                  bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                                                  bounded_context.repositories [array[reference→repository]]: [3 items]
                                                                  bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                                                  bounded_context.application_services [array[reference→application_service]]: [3 items]
                                                                  bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                                                  bounded_context.factories [array[reference→factory]]: [2 items]
                                                                  bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                                  bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                                  bounded_context.entities [array[reference→entity]]: [3 items]
                                                                  bounded_context.specifications [array[reference→specification]]: <not found>
                                                                    specification [type] (id: ?)
                                                                      specification.id [attribute[string]]: <not found>
                                                                      specification.name [attribute[string]]: calculated_at
                                                                      specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                                      specification.applies_to [reference→None]: <not found>
                                                                      specification.rule [attribute[string]]: <not found>
                                                                      specification.composable [attribute[boolean]]: <not found>
                                                                      specification.use_cases [array[string]]: <not found>
                                                              value_object.description [attribute[string]]: <not found>
                                                              value_object.attributes [array[object]]: <not found>
                                                                value_object.attributes.name [attribute[string]]: calculated_at
                                                                value_object.attributes.type [attribute[string]]: DateTime
                                                                value_object.attributes.required [attribute[boolean]]: True
                                                                value_object.attributes.validation [attribute[string]]: <not found>
                                                              value_object.validation_rules [array[string]]: <not found>
                                                              value_object.equality_criteria [array[string]]: <not found>
                                                              value_object.immutability [attribute[boolean]]: <not found>
                                                              value_object.side_effect_free_methods [array[object]]: <not found>
                                                                value_object.side_effect_free_methods.name [attribute[string]]: calculated_at
                                                                value_object.side_effect_free_methods.description [attribute[string]]: <not found>
                                                                value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                                              value_object.common_values [array[string]]: <not found>
                                                              value_object.entities [array[reference→entity]]: [3 items]
                                                          entity.attributes.required [attribute[boolean]]: True
                                                          entity.attributes.description [attribute[string]]: <not found>
                                                        entity.business_methods [array[object]]: [1 items]
                                                          entity.business_methods.name [attribute[string]]: recalculate
                                                          entity.business_methods.description [attribute[string]]: Recalculate match score (if profile or job changed)
                                                          entity.business_methods.parameters [array]: [2 items: Candidate candidate, JobPosting job]
                                                          entity.business_methods.returns [attribute[string]]: void
                                                          entity.business_methods.publishes_events [array]: [1 items: evt_match_calculated]
                                                        entity.invariants [array[string]]: [2 items: Score matches tier (80+ = High, 50-79 = Medium, <50 = Low), Criteria scores sum to total score]
                                                        entity.lifecycle_states [array[string]]: <not found>
                                                        entity.aggregates [array[reference→aggregate]]: [6 items]
                                                    aggregate.entities [array[reference→entity]]: [1 items: ent_job_match]
                                                    aggregate.value_objects [array[reference→value_object]]: [3 items: vo_match_score, vo_match_tier, vo_match_criteria_scores]
                                                    aggregate.consistency_rules [array[string]]: [2 items: Match score must be 0-100, Match tier must correspond to score (High: 80+, Medium: 50-79, Low: <50)]
                                                    aggregate.invariants [array[string]]: [2 items: Match score calculated from weighted criteria, Match references valid candidate and job]
                                                    aggregate.lifecycle_hooks [object]: <not found>
                                                      aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                                                      aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                                                      aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
                                                    aggregate.size_estimate [attribute[enum: small, medium, large]]: small
                                                    aggregate.repositories [array[reference→repository]]: [3 items]
                                                    aggregate.domain_events [array[reference→domain_event]]: [4 items]
                                                bounded_context.repositories [array[reference→repository]]: [1 items: repo_job_match]
                                                bounded_context.domain_services [array[reference→domain_service]]: [2 items: svc_dom_matching_engine, svc_dom_scoring_algorithm]
                                                bounded_context.application_services [array[reference→application_service]]: [2 items: svc_app_calculate_matches, svc_app_get_recommendations]
                                                bounded_context.domain_events [array[reference→domain_event]]: [2 items: evt_match_calculated, evt_high_match_found]
                                                bounded_context.factories [array[reference→factory]]: [2 items]
                                                bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                                bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                                bounded_context.entities [array[reference→entity]]: [3 items]
                                                bounded_context.specifications [array[reference→specification]]: <not found>
                                                  specification [type] (id: bc_matching)
                                                    specification.id [attribute[string]]: bc_matching
                                                    specification.name [attribute[string]]: Job Matching Engine
                                                    specification.bounded_context_ref [reference→bounded_context]: <not found>
                                                    specification.applies_to [reference→None]: <not found>
                                                    specification.rule [attribute[string]]: <not found>
                                                    specification.composable [attribute[boolean]]: <not found>
                                                    specification.use_cases [array[string]]: <not found>
                                            factory.creates_type [attribute[enum: entity, aggregate, value_object]]: aggregate
                                            factory.creates_ref [reference→None]: agg_job_match
                                            factory.creation_methods [array[object]]: [1 items]
                                              factory.creation_methods.name [attribute[string]]: createMatch
                                              factory.creation_methods.parameters [array]: [4 items: CandidateId candidateId, JobId jobId, MatchScore score...]
                                              factory.creation_methods.returns [attribute[string]]: JobMatch
                                              factory.creation_methods.description [attribute[string]]: Create new match result
                                            factory.location [attribute[enum: domain_layer, infrastructure_layer, on_aggregate]]: domain_layer
                                            factory.reconstitution [attribute[boolean]]: False
                                        bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                        bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                        bounded_context.entities [array[reference→entity]]: [3 items]
                                        bounded_context.specifications [array[reference→specification]]: <not found>
                                          specification [type] (id: bc_scrapers)
                                            specification.id [attribute[string]]: bc_scrapers
                                            specification.name [attribute[string]]: Job Scrapers
                                            specification.bounded_context_ref [reference→bounded_context]: <not found>
                                            specification.applies_to [reference→None]: <not found>
                                            specification.rule [attribute[string]]: <not found>
                                            specification.composable [attribute[boolean]]: <not found>
                                            specification.use_cases [array[string]]: <not found>
                                    domain.investment_strategy [attribute[string]]: Adequate quality, consider third-party scraping services
                                    domain.notes [attribute[string]]: Necessary but not differentiating
                                bounded_context.description [attribute[string]]: Centralized catalog of all jobs from various sources
                                bounded_context.ubiquitous_language [object]: {glossary}
                                  bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                    bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                    bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                    bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                bounded_context.team_ownership [attribute[string]]: Aggregation Team
                                bounded_context.aggregates [array[reference→aggregate]]: [1 items: agg_job_posting]
                                bounded_context.repositories [array[reference→repository]]: [1 items: repo_job_posting]
                                bounded_context.domain_services [array[reference→domain_service]]: [1 items: svc_dom_deduplication]
                                bounded_context.application_services [array[reference→application_service]]: [1 items: svc_app_ingest_jobs]
                                bounded_context.domain_events [array[reference→domain_event]]: [2 items: evt_job_posted, evt_job_expired]
                                bounded_context.factories [array[reference→factory]]: [2 items]
                                bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                bounded_context.entities [array[reference→entity]]: [3 items]
                                bounded_context.specifications [array[reference→specification]]: <not found>
                                  specification [type] (id: bc_job_catalog)
                                    specification.id [attribute[string]]: bc_job_catalog
                                    specification.name [attribute[string]]: Job Catalog
                                    specification.bounded_context_ref [reference→bounded_context]: <not found>
                                    specification.applies_to [reference→None]: <not found>
                                    specification.rule [attribute[string]]: <not found>
                                    specification.composable [attribute[boolean]]: <not found>
                                    specification.use_cases [array[string]]: <not found>
                            entity.aggregate_ref [reference→aggregate]: agg_job_posting
                            entity.is_aggregate_root [attribute[boolean]]: True
                            entity.identity_field [attribute[string]]: job_id
                            entity.identity_generation [attribute[enum: user_provided, auto_generated, derived...]]: auto_generated
                            entity.attributes [array[object]]: [10 items]
                              entity.attributes.name [attribute[string]]: job_id
                              entity.attributes.type [attribute[string]]: JobId
                              entity.attributes.value_object_ref [reference→value_object]: vo_job_id
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: title
                              entity.attributes.type [attribute[string]]: JobTitle
                              entity.attributes.value_object_ref [reference→value_object]: vo_job_title
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: company
                              entity.attributes.type [attribute[string]]: Company
                              entity.attributes.value_object_ref [reference→value_object]: vo_company
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: location
                              entity.attributes.type [attribute[string]]: Location
                              entity.attributes.value_object_ref [reference→value_object]: vo_location
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: salary_range
                              entity.attributes.type [attribute[string]]: SalaryRange
                              entity.attributes.value_object_ref [reference→value_object]: vo_salary_range
                              entity.attributes.required [attribute[boolean]]: False
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: requirements
                              entity.attributes.type [attribute[string]]: Requirements
                              entity.attributes.value_object_ref [reference→value_object]: vo_requirements
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: description
                              entity.attributes.type [attribute[string]]: Description
                              entity.attributes.value_object_ref [reference→value_object]: vo_description
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: source
                              entity.attributes.type [attribute[string]]: Source
                              entity.attributes.value_object_ref [reference→value_object]: vo_source
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: posted_date
                              entity.attributes.type [attribute[string]]: Date
                              entity.attributes.value_object_ref [reference→value_object]: <not found>
                                value_object [type] (id: ?)
                                  value_object.id [attribute[string]]: <not found>
                                  value_object.name [attribute[string]]: posted_date
                                  value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                    bounded_context [type] (id: ?)
                                      bounded_context.id [attribute[string]]: <not found>
                                      bounded_context.name [attribute[string]]: posted_date
                                      bounded_context.domain_ref [reference→domain]: <not found>
                                        domain [type] (id: ?)
                                          domain.id [attribute[string]]: <not found>
                                          domain.name [attribute[string]]: posted_date
                                          domain.type [attribute[enum: core, supporting, generic]]: Date
                                          domain.description [attribute[string]]: <not found>
                                          domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                          domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                          domain.investment_strategy [attribute[string]]: <not found>
                                          domain.notes [attribute[string]]: <not found>
                                      bounded_context.description [attribute[string]]: <not found>
                                      bounded_context.ubiquitous_language [object]: <not found>
                                        bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                      bounded_context.team_ownership [attribute[string]]: <not found>
                                      bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                      bounded_context.repositories [array[reference→repository]]: [3 items]
                                      bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                      bounded_context.application_services [array[reference→application_service]]: [3 items]
                                      bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                      bounded_context.factories [array[reference→factory]]: [2 items]
                                      bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                      bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                      bounded_context.entities [array[reference→entity]]: [3 items]
                                      bounded_context.specifications [array[reference→specification]]: <not found>
                                        specification [type] (id: ?)
                                          specification.id [attribute[string]]: <not found>
                                          specification.name [attribute[string]]: posted_date
                                          specification.bounded_context_ref [reference→bounded_context]: <not found>
                                          specification.applies_to [reference→None]: <not found>
                                          specification.rule [attribute[string]]: <not found>
                                          specification.composable [attribute[boolean]]: <not found>
                                          specification.use_cases [array[string]]: <not found>
                                  value_object.description [attribute[string]]: <not found>
                                  value_object.attributes [array[object]]: <not found>
                                    value_object.attributes.name [attribute[string]]: posted_date
                                    value_object.attributes.type [attribute[string]]: Date
                                    value_object.attributes.required [attribute[boolean]]: True
                                    value_object.attributes.validation [attribute[string]]: <not found>
                                  value_object.validation_rules [array[string]]: <not found>
                                  value_object.equality_criteria [array[string]]: <not found>
                                  value_object.immutability [attribute[boolean]]: <not found>
                                  value_object.side_effect_free_methods [array[object]]: <not found>
                                    value_object.side_effect_free_methods.name [attribute[string]]: posted_date
                                    value_object.side_effect_free_methods.description [attribute[string]]: <not found>
                                    value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                  value_object.common_values [array[string]]: <not found>
                                  value_object.entities [array[reference→entity]]: [3 items]
                              entity.attributes.required [attribute[boolean]]: True
                              entity.attributes.description [attribute[string]]: <not found>
                              entity.attributes.name [attribute[string]]: expiry_date
                              entity.attributes.type [attribute[string]]: Date
                              entity.attributes.value_object_ref [reference→value_object]: <not found>
                                value_object [type] (id: ?)
                                  value_object.id [attribute[string]]: <not found>
                                  value_object.name [attribute[string]]: expiry_date
                                  value_object.bounded_context_ref [reference→bounded_context]: <not found>
                                    bounded_context [type] (id: ?)
                                      bounded_context.id [attribute[string]]: <not found>
                                      bounded_context.name [attribute[string]]: expiry_date
                                      bounded_context.domain_ref [reference→domain]: <not found>
                                        domain [type] (id: ?)
                                          domain.id [attribute[string]]: <not found>
                                          domain.name [attribute[string]]: expiry_date
                                          domain.type [attribute[enum: core, supporting, generic]]: Date
                                          domain.description [attribute[string]]: <not found>
                                          domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                          domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                          domain.investment_strategy [attribute[string]]: <not found>
                                          domain.notes [attribute[string]]: <not found>
                                      bounded_context.description [attribute[string]]: <not found>
                                      bounded_context.ubiquitous_language [object]: <not found>
                                        bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                          bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                                      bounded_context.team_ownership [attribute[string]]: <not found>
                                      bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                                      bounded_context.repositories [array[reference→repository]]: [3 items]
                                      bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                                      bounded_context.application_services [array[reference→application_service]]: [3 items]
                                      bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                                      bounded_context.factories [array[reference→factory]]: [2 items]
                                      bounded_context.value_objects [array[reference→value_object]]: [4 items]
                                      bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                                      bounded_context.entities [array[reference→entity]]: [3 items]
                                      bounded_context.specifications [array[reference→specification]]: <not found>
                                        specification [type] (id: ?)
                                          specification.id [attribute[string]]: <not found>
                                          specification.name [attribute[string]]: expiry_date
                                          specification.bounded_context_ref [reference→bounded_context]: <not found>
                                          specification.applies_to [reference→None]: <not found>
                                          specification.rule [attribute[string]]: <not found>
                                          specification.composable [attribute[boolean]]: <not found>
                                          specification.use_cases [array[string]]: <not found>
                                  value_object.description [attribute[string]]: <not found>
                                  value_object.attributes [array[object]]: <not found>
                                    value_object.attributes.name [attribute[string]]: expiry_date
                                    value_object.attributes.type [attribute[string]]: Date
                                    value_object.attributes.required [attribute[boolean]]: False
                                    value_object.attributes.validation [attribute[string]]: <not found>
                                  value_object.validation_rules [array[string]]: <not found>
                                  value_object.equality_criteria [array[string]]: <not found>
                                  value_object.immutability [attribute[boolean]]: <not found>
                                  value_object.side_effect_free_methods [array[object]]: <not found>
                                    value_object.side_effect_free_methods.name [attribute[string]]: expiry_date
                                    value_object.side_effect_free_methods.description [attribute[string]]: <not found>
                                    value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                                  value_object.common_values [array[string]]: <not found>
                                  value_object.entities [array[reference→entity]]: [3 items]
                              entity.attributes.required [attribute[boolean]]: False
                              entity.attributes.description [attribute[string]]: <not found>
                            entity.business_methods [array[object]]: [2 items]
                              entity.business_methods.name [attribute[string]]: isExpired
                              entity.business_methods.description [attribute[string]]: Check if job posting has expired
                              entity.business_methods.parameters [array]: [0 items]
                              entity.business_methods.returns [attribute[string]]: boolean
                              entity.business_methods.publishes_events [array]: [0 items]
                              entity.business_methods.name [attribute[string]]: markExpired
                              entity.business_methods.description [attribute[string]]: Mark job as expired
                              entity.business_methods.parameters [array]: [0 items]
                              entity.business_methods.returns [attribute[string]]: void
                              entity.business_methods.publishes_events [array]: [1 items: evt_job_expired]
                            entity.invariants [array[string]]: <not found>
                            entity.lifecycle_states [array[string]]: [3 items: active, expired, filled]
                            entity.aggregates [array[reference→aggregate]]: [6 items]
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: name
                    entity.attributes.type [attribute[string]]: PersonName
                    entity.attributes.value_object_ref [reference→value_object]: vo_person_name
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: skills
                    entity.attributes.type [attribute[string]]: Skills
                    entity.attributes.value_object_ref [reference→value_object]: vo_skills
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: education
                    entity.attributes.type [attribute[string]]: Education
                    entity.attributes.value_object_ref [reference→value_object]: vo_education
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: experience
                    entity.attributes.type [attribute[string]]: Experience
                    entity.attributes.value_object_ref [reference→value_object]: vo_experience
                    entity.attributes.required [attribute[boolean]]: False
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: location
                    entity.attributes.type [attribute[string]]: Location
                    entity.attributes.value_object_ref [reference→value_object]: vo_location
                    entity.attributes.required [attribute[boolean]]: True
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: preferences
                    entity.attributes.type [attribute[string]]: JobPreferences
                    entity.attributes.value_object_ref [reference→value_object]: vo_preferences
                    entity.attributes.required [attribute[boolean]]: False
                    entity.attributes.description [attribute[string]]: <not found>
                    entity.attributes.name [attribute[string]]: profile_completeness
                    entity.attributes.type [attribute[string]]: Percentage
                    entity.attributes.value_object_ref [reference→value_object]: <not found>
                      value_object [type] (id: ?)
                        value_object.id [attribute[string]]: <not found>
                        value_object.name [attribute[string]]: profile_completeness
                        value_object.bounded_context_ref [reference→bounded_context]: <not found>
                          bounded_context [type] (id: ?)
                            bounded_context.id [attribute[string]]: <not found>
                            bounded_context.name [attribute[string]]: profile_completeness
                            bounded_context.domain_ref [reference→domain]: <not found>
                              domain [type] (id: ?)
                                domain.id [attribute[string]]: <not found>
                                domain.name [attribute[string]]: profile_completeness
                                domain.type [attribute[enum: core, supporting, generic]]: Percentage
                                domain.description [attribute[string]]: Calculated score
                                domain.strategic_importance [attribute[enum: critical, important, standard...]]: <not found>
                                domain.bounded_contexts [array[reference→bounded_context]]: [9 items]
                                domain.investment_strategy [attribute[string]]: <not found>
                                domain.notes [attribute[string]]: <not found>
                            bounded_context.description [attribute[string]]: Calculated score
                            bounded_context.ubiquitous_language [object]: <not found>
                              bounded_context.ubiquitous_language.glossary [array[object]]: <not found>
                                bounded_context.ubiquitous_language.glossary.term [attribute[string]]: <not found>
                                bounded_context.ubiquitous_language.glossary.definition [attribute[string]]: <not found>
                                bounded_context.ubiquitous_language.glossary.examples [array[string]]: <not found>
                            bounded_context.team_ownership [attribute[string]]: <not found>
                            bounded_context.aggregates [array[reference→aggregate]]: [6 items]
                            bounded_context.repositories [array[reference→repository]]: [3 items]
                            bounded_context.domain_services [array[reference→domain_service]]: [3 items]
                            bounded_context.application_services [array[reference→application_service]]: [3 items]
                            bounded_context.domain_events [array[reference→domain_event]]: [4 items]
                            bounded_context.factories [array[reference→factory]]: [2 items]
                            bounded_context.value_objects [array[reference→value_object]]: [4 items]
                            bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
                            bounded_context.entities [array[reference→entity]]: [3 items]
                            bounded_context.specifications [array[reference→specification]]: <not found>
                              specification [type] (id: ?)
                                specification.id [attribute[string]]: <not found>
                                specification.name [attribute[string]]: profile_completeness
                                specification.bounded_context_ref [reference→bounded_context]: <not found>
                                specification.applies_to [reference→None]: <not found>
                                specification.rule [attribute[string]]: <not found>
                                specification.composable [attribute[boolean]]: <not found>
                                specification.use_cases [array[string]]: <not found>
                        value_object.description [attribute[string]]: Calculated score
                        value_object.attributes [array[object]]: <not found>
                          value_object.attributes.name [attribute[string]]: profile_completeness
                          value_object.attributes.type [attribute[string]]: Percentage
                          value_object.attributes.required [attribute[boolean]]: False
                          value_object.attributes.validation [attribute[string]]: <not found>
                        value_object.validation_rules [array[string]]: <not found>
                        value_object.equality_criteria [array[string]]: <not found>
                        value_object.immutability [attribute[boolean]]: <not found>
                        value_object.side_effect_free_methods [array[object]]: <not found>
                          value_object.side_effect_free_methods.name [attribute[string]]: profile_completeness
                          value_object.side_effect_free_methods.description [attribute[string]]: Calculated score
                          value_object.side_effect_free_methods.returns [attribute[string]]: <not found>
                        value_object.common_values [array[string]]: <not found>
                        value_object.entities [array[reference→entity]]: [3 items]
                    entity.attributes.required [attribute[boolean]]: False
                    entity.attributes.description [attribute[string]]: Calculated score
                  entity.business_methods [array[object]]: [3 items]
                    entity.business_methods.name [attribute[string]]: updateSkills
                    entity.business_methods.description [attribute[string]]: Update candidate's skills
                    entity.business_methods.parameters [array]: [1 items: Skills newSkills]
                    entity.business_methods.returns [attribute[string]]: void
                    entity.business_methods.publishes_events [array]: [1 items: evt_skills_changed]
                    entity.business_methods.name [attribute[string]]: calculateCompleteness
                    entity.business_methods.description [attribute[string]]: Calculate profile completeness percentage
                    entity.business_methods.parameters [array]: [0 items]
                    entity.business_methods.returns [attribute[string]]: Percentage
                    entity.business_methods.publishes_events [array]: [0 items]
                    entity.business_methods.name [attribute[string]]: isEligibleForMatching
                    entity.business_methods.description [attribute[string]]: Check if profile is complete enough for matching
                    entity.business_methods.parameters [array]: [0 items]
                    entity.business_methods.returns [attribute[string]]: boolean
                    entity.business_methods.publishes_events [array]: [0 items]
                  entity.invariants [array[string]]: [3 items: Email must be unique, Skills list must not be empty, Completeness score must be accurate]
                  entity.lifecycle_states [array[string]]: [3 items: draft, active, suspended]
                  entity.aggregates [array[reference→aggregate]]: [6 items]
              aggregate.entities [array[reference→entity]]: [1 items: ent_candidate]
              aggregate.value_objects [array[reference→value_object]]: [8 items: vo_candidate_id, vo_email, vo_person_name...]
              aggregate.consistency_rules [array[string]]: [3 items: Candidate must have valid email, Skills list must not be empty for matching to work, Location must be valid Canadian location]
              aggregate.invariants [array[string]]: [2 items: Email uniqueness across all candidates, Profile completeness score >= 60% for matching]
              aggregate.lifecycle_hooks [object]: <not found>
                aggregate.lifecycle_hooks.on_create [array[string]]: <not found>
                aggregate.lifecycle_hooks.on_update [array[string]]: <not found>
                aggregate.lifecycle_hooks.on_delete [array[string]]: <not found>
              aggregate.size_estimate [attribute[enum: small, medium, large]]: medium
              aggregate.repositories [array[reference→repository]]: [3 items]
              aggregate.domain_events [array[reference→domain_event]]: [4 items]
          bounded_context.repositories [array[reference→repository]]: [1 items: repo_profile]
          bounded_context.domain_services [array[reference→domain_service]]: [1 items: svc_dom_profile_scorer]
          bounded_context.application_services [array[reference→application_service]]: [2 items: svc_app_update_profile, svc_app_import_resume]
          bounded_context.domain_events [array[reference→domain_event]]: [3 items: evt_profile_created, evt_profile_updated, evt_skills_changed]
          bounded_context.factories [array[reference→factory]]: [2 items]
          bounded_context.value_objects [array[reference→value_object]]: [4 items]
          bounded_context.context_mappings [array[reference→context_mapping]]: [8 items]
          bounded_context.entities [array[reference→entity]]: [3 items]
          bounded_context.specifications [array[reference→specification]]: <not found>
            specification [type] (id: bc_profile)
              specification.id [attribute[string]]: bc_profile
              specification.name [attribute[string]]: Profile Management
              specification.bounded_context_ref [reference→bounded_context]: <not found>
              specification.applies_to [reference→None]: <not found>
              specification.rule [attribute[string]]: <not found>
              specification.composable [attribute[boolean]]: <not found>
              specification.use_cases [array[string]]: <not found>
      domain.investment_strategy [attribute[string]]: Best team, rigorous DDD, continuous refinement
      domain.notes [attribute[string]]: This is where we provide competitive advantage
  system.bounded_contexts [array[reference→bounded_context]]: [9 items]
  system.context_mappings [array[reference→context_mapping]]: [8 items]