└── system
    ├── attribute[string]: system.id
    ├── attribute[string]: system.name
    ├── attribute[string]: system.description
    ├── attribute[string]: system.version
    ├── array[reference→domain]: system.domains
    │   └── domain
    │       ├── attribute[string]: domain.id
    │       ├── attribute[string]: domain.name
    │       ├── attribute[enum: core, supporting, generic]: domain.type
    │       ├── attribute[string]: domain.description
    │       ├── attribute[enum: critical, important, standard...]: domain.strategic_importance
    │       ├── array[reference→bounded_context]: domain.bounded_contexts
    │       │   └── bounded_context
    │       │       ├── attribute[string]: bounded_context.id
    │       │       ├── attribute[string]: bounded_context.name
    │       │       ├── reference→domain: bounded_context.domain_ref
    │       │       ├── attribute[string]: bounded_context.description
    │       │       ├── object: bounded_context.ubiquitous_language
    │       │       │   └── array[object]: bounded_context.ubiquitous_language.glossary
    │       │       │       ├── attribute[string]: bounded_context.ubiquitous_language.glossary.term
    │       │       │       ├── attribute[string]: bounded_context.ubiquitous_language.glossary.definition
    │       │       │       └── array[string]: bounded_context.ubiquitous_language.glossary.examples
    │       │       ├── attribute[string]: bounded_context.team_ownership
    │       │       ├── array[reference→aggregate]: bounded_context.aggregates
    │       │       │   └── aggregate
    │       │       │       ├── attribute[string]: aggregate.id
    │       │       │       ├── attribute[string]: aggregate.name
    │       │       │       ├── reference→bounded_context: aggregate.bounded_context_ref
    │       │       │       ├── reference→entity: aggregate.root_ref
    │       │       │       │   └── entity
    │       │       │       │       ├── attribute[string]: entity.id
    │       │       │       │       ├── attribute[string]: entity.name
    │       │       │       │       ├── reference→bounded_context: entity.bounded_context_ref
    │       │       │       │       ├── reference→aggregate: entity.aggregate_ref
    │       │       │       │       ├── attribute[boolean]: entity.is_aggregate_root
    │       │       │       │       ├── attribute[string]: entity.identity_field
    │       │       │       │       ├── attribute[enum: user_provided, auto_generated, derived...]: entity.identity_generation
    │       │       │       │       ├── array[object]: entity.attributes
    │       │       │       │       │   ├── attribute[string]: entity.attributes.name
    │       │       │       │       │   ├── attribute[string]: entity.attributes.type
    │       │       │       │       │   ├── reference→value_object: entity.attributes.value_object_ref
    │       │       │       │       │   │   └── value_object
    │       │       │       │       │   │       ├── attribute[string]: value_object.id
    │       │       │       │       │   │       ├── attribute[string]: value_object.name
    │       │       │       │       │   │       ├── reference→bounded_context: value_object.bounded_context_ref
    │       │       │       │       │   │       ├── attribute[string]: value_object.description
    │       │       │       │       │   │       ├── array[object]: value_object.attributes
    │       │       │       │       │   │       │   ├── attribute[string]: value_object.attributes.name
    │       │       │       │       │   │       │   ├── attribute[string]: value_object.attributes.type
    │       │       │       │       │   │       │   ├── attribute[boolean]: value_object.attributes.required
    │       │       │       │       │   │       │   └── attribute[string]: value_object.attributes.validation
    │       │       │       │       │   │       ├── array[string]: value_object.validation_rules
    │       │       │       │       │   │       ├── array[string]: value_object.equality_criteria
    │       │       │       │       │   │       ├── attribute[boolean]: value_object.immutability
    │       │       │       │       │   │       ├── array[object]: value_object.side_effect_free_methods
    │       │       │       │       │   │       │   ├── attribute[string]: value_object.side_effect_free_methods.name
    │       │       │       │       │   │       │   ├── attribute[string]: value_object.side_effect_free_methods.description
    │       │       │       │       │   │       │   └── attribute[string]: value_object.side_effect_free_methods.returns
    │       │       │       │       │   │       ├── array[string]: value_object.common_values
    │       │       │       │       │   │       └── array[reference→entity]: value_object.entities
    │       │       │       │       │   ├── attribute[boolean]: entity.attributes.required
    │       │       │       │       │   └── attribute[string]: entity.attributes.description
    │       │       │       │       ├── array[object]: entity.business_methods
    │       │       │       │       │   ├── attribute[string]: entity.business_methods.name
    │       │       │       │       │   ├── attribute[string]: entity.business_methods.description
    │       │       │       │       │   ├── array: entity.business_methods.parameters
    │       │       │       │       │   ├── attribute[string]: entity.business_methods.returns
    │       │       │       │       │   └── array: entity.business_methods.publishes_events
    │       │       │       │       ├── array[string]: entity.invariants
    │       │       │       │       ├── array[string]: entity.lifecycle_states
    │       │       │       │       └── array[reference→aggregate]: entity.aggregates
    │       │       │       ├── array[reference→entity]: aggregate.entities
    │       │       │       ├── array[reference→value_object]: aggregate.value_objects
    │       │       │       ├── array[string]: aggregate.consistency_rules
    │       │       │       ├── array[string]: aggregate.invariants
    │       │       │       ├── object: aggregate.lifecycle_hooks
    │       │       │       │   ├── array[string]: aggregate.lifecycle_hooks.on_create
    │       │       │       │   ├── array[string]: aggregate.lifecycle_hooks.on_update
    │       │       │       │   └── array[string]: aggregate.lifecycle_hooks.on_delete
    │       │       │       ├── attribute[enum: small, medium, large]: aggregate.size_estimate
    │       │       │       ├── array[reference→repository]: aggregate.repositories
    │       │       │       │   └── repository
    │       │       │       │       ├── attribute[string]: repository.id
    │       │       │       │       ├── attribute[string]: repository.name
    │       │       │       │       ├── reference→bounded_context: repository.bounded_context_ref
    │       │       │       │       ├── reference→aggregate: repository.aggregate_ref
    │       │       │       │       ├── array[object]: repository.interface_methods
    │       │       │       │       │   ├── attribute[string]: repository.interface_methods.name
    │       │       │       │       │   ├── attribute[string]: repository.interface_methods.description
    │       │       │       │       │   ├── array: repository.interface_methods.parameters
    │       │       │       │       │   ├── attribute[string]: repository.interface_methods.returns
    │       │       │       │       │   └── attribute[enum: by_id, by_criteria, all...]: repository.interface_methods.query_type
    │       │       │       │       ├── attribute[string]: repository.persistence_strategy
    │       │       │       │       └── attribute[string]: repository.implementation_notes
    │       │       │       └── array[reference→domain_event]: aggregate.domain_events
    │       │       │           └── domain_event
    │       │       │               ├── attribute[string]: domain_event.id
    │       │       │               ├── attribute[string]: domain_event.name
    │       │       │               ├── reference→bounded_context: domain_event.bounded_context_ref
    │       │       │               ├── reference→aggregate: domain_event.aggregate_ref
    │       │       │               ├── attribute[string]: domain_event.description
    │       │       │               ├── array[object]: domain_event.data_carried
    │       │       │               │   ├── attribute[string]: domain_event.data_carried.name
    │       │       │               │   ├── attribute[string]: domain_event.data_carried.type
    │       │       │               │   └── attribute[string]: domain_event.data_carried.description
    │       │       │               ├── array[object]: domain_event.handlers
    │       │       │               │   ├── attribute[string]: domain_event.handlers.bounded_context
    │       │       │               │   ├── attribute[string]: domain_event.handlers.handler
    │       │       │               │   └── attribute[string]: domain_event.handlers.action
    │       │       │               ├── attribute[boolean]: domain_event.immutable
    │       │       │               └── attribute[boolean]: domain_event.timestamp_included
    │       │       ├── array[reference→repository]: bounded_context.repositories
    │       │       ├── array[reference→domain_service]: bounded_context.domain_services
    │       │       │   └── domain_service
    │       │       │       ├── attribute[string]: domain_service.id
    │       │       │       ├── attribute[string]: domain_service.name
    │       │       │       ├── reference→bounded_context: domain_service.bounded_context_ref
    │       │       │       ├── attribute[string]: domain_service.description
    │       │       │       ├── array[object]: domain_service.operations
    │       │       │       │   ├── attribute[string]: domain_service.operations.name
    │       │       │       │   ├── attribute[string]: domain_service.operations.description
    │       │       │       │   ├── array: domain_service.operations.parameters
    │       │       │       │   ├── attribute[string]: domain_service.operations.returns
    │       │       │       │   ├── array: domain_service.operations.involves_aggregates
    │       │       │       │   └── attribute[string]: domain_service.operations.business_logic
    │       │       │       ├── array[object]: domain_service.dependencies
    │       │       │       │   ├── attribute[enum: repository, domain_service, specification]: domain_service.dependencies.type
    │       │       │       │   └── attribute[string]: domain_service.dependencies.ref
    │       │       │       └── attribute[boolean]: domain_service.stateless
    │       │       ├── array[reference→application_service]: bounded_context.application_services
    │       │       │   └── application_service
    │       │       │       ├── attribute[string]: application_service.id
    │       │       │       ├── attribute[string]: application_service.name
    │       │       │       ├── reference→bounded_context: application_service.bounded_context_ref
    │       │       │       ├── attribute[string]: application_service.use_case
    │       │       │       ├── array[object]: application_service.orchestrates
    │       │       │       │   ├── attribute[enum: aggregate, domain_service, repository]: application_service.orchestrates.type
    │       │       │       │   ├── attribute[string]: application_service.orchestrates.ref
    │       │       │       │   └── attribute[string]: application_service.orchestrates.operation
    │       │       │       ├── attribute[boolean]: application_service.transaction_boundary
    │       │       │       ├── array[reference→domain_event]: application_service.publishes_events
    │       │       │       └── attribute[string]: application_service.authorization
    │       │       ├── array[reference→domain_event]: bounded_context.domain_events
    │       │       ├── array[reference→factory]: bounded_context.factories
    │       │       │   └── factory
    │       │       │       ├── attribute[string]: factory.id
    │       │       │       ├── attribute[string]: factory.name
    │       │       │       ├── reference→bounded_context: factory.bounded_context_ref
    │       │       │       ├── attribute[enum: entity, aggregate, value_object]: factory.creates_type
    │       │       │       ├── reference→None: factory.creates_ref
    │       │       │       ├── array[object]: factory.creation_methods
    │       │       │       │   ├── attribute[string]: factory.creation_methods.name
    │       │       │       │   ├── array: factory.creation_methods.parameters
    │       │       │       │   ├── attribute[string]: factory.creation_methods.returns
    │       │       │       │   └── attribute[string]: factory.creation_methods.description
    │       │       │       ├── attribute[enum: domain_layer, infrastructure_layer, on_aggregate]: factory.location
    │       │       │       └── attribute[boolean]: factory.reconstitution
    │       │       ├── array[reference→context_mapping]: bounded_context.context_mappings
    │       │       │   └── context_mapping
    │       │       │       ├── attribute[string]: context_mapping.id
    │       │       │       ├── reference→bounded_context: context_mapping.upstream_context
    │       │       │       ├── reference→bounded_context: context_mapping.downstream_context
    │       │       │       ├── attribute[enum: partnership, shared_kernel, customer_supplier...]: context_mapping.relationship_type
    │       │       │       ├── attribute[string]: context_mapping.integration_pattern
    │       │       │       ├── object: context_mapping.translation_map
    │       │       │       ├── array[string]: context_mapping.shared_elements
    │       │       │       ├── object: context_mapping.acl_details
    │       │       │       │   ├── array[string]: context_mapping.acl_details.facades
    │       │       │       │   ├── array[string]: context_mapping.acl_details.adapters
    │       │       │       │   └── array[string]: context_mapping.acl_details.translators
    │       │       │       └── attribute[string]: context_mapping.notes
    │       │       ├── array[reference→entity]: bounded_context.entities
    │       │       ├── array[reference→specification]: bounded_context.specifications
    │       │       │   └── specification
    │       │       │       ├── attribute[string]: specification.id
    │       │       │       ├── attribute[string]: specification.name
    │       │       │       ├── reference→bounded_context: specification.bounded_context_ref
    │       │       │       ├── reference→None: specification.applies_to
    │       │       │       ├── attribute[string]: specification.rule
    │       │       │       ├── attribute[boolean]: specification.composable
    │       │       │       └── array[string]: specification.use_cases
    │       │       └── array[reference→value_object]: bounded_context.value_objects
    │       ├── attribute[string]: domain.investment_strategy
    │       └── attribute[string]: domain.notes
    ├── array[reference→bounded_context]: system.bounded_contexts
    └── array[reference→context_mapping]: system.context_mappings
