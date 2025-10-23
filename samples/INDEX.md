# Sample Schemas & Models

Curated catalog of the sample schemas and companion models included in `samples/`. Each entry links the schema definition to an illustrative YAML document so you can generate documentation immediately.

## Agile Delivery Patterns

| Schema | Model | Schema Description | Model Highlights |
| --- | --- | --- | --- |
| `agile/delivery-agile.schema.yaml` | `agile/delivery-example.yaml` | Product delivery patterns covering products, features, stories, tasks, and increments. | iOS app delivery scenario showing backlog hierarchy and work breakdown. |
| `agile/portfolio-agile.schema.yaml` | `agile/portfolio-example.yaml` | Portfolio-level patterns for value streams, epics, and roadmaps. | E-commerce platform portfolio illustrating portfolio, value streams, and roadmap data. |
| `agile/program-agile.schema.yaml` | `agile/program-example.yaml` | Program-level structures including programs, program increments, and release planning. | Mobile platform program with PI cadence, releases, and architectural runway details. |
| `agile/safe-agile.schema.yaml` | `agile/safe-example.yaml` | SAFe-specific extensions for ARTs and cadence patterns. | Mobile platform Agile Release Train with SAFe ceremonies and synchronization cadence. |
| `agile/team-agile.schema.yaml` | `agile/team-example.yaml` | Team-level execution patterns including sprints, ceremonies, and impediments. | iOS development team showcasing sprint ceremonies, velocity, and impediment tracking. |

## Data Engineering Systems

| Schema | Model | Schema Description | Model Highlights |
| --- | --- | --- | --- |
| `data-eng/model.schema.yaml` | `data-eng/iot.example.yaml` | Holistic data engineering model schema for domains, pipelines, storage, SLAs, and governance. | IoT sensor platform emphasizing streaming ingestion, windowing, anomaly detection, and late-arrival handling. |
| `data-eng/model.schema.yaml` | `data-eng/ml.example.yaml` | Holistic data engineering model schema for domains, pipelines, storage, SLAs, and governance. | ML feature store platform focusing on feature engineering, point-in-time joins, and drift monitoring. |
| `data-eng/model.schema.yaml` | `data-eng/payments.example.yaml` | Holistic data engineering model schema for domains, pipelines, storage, SLAs, and governance. | Payment processing system highlighting CDC outbox, exactly-once semantics, and fraud detection pipelines. |
| `data-eng/model.schema.yaml` | `data-eng/retail.example.yaml` | Holistic data engineering model schema for domains, pipelines, storage, SLAs, and governance. | Retail order processing medallion architecture with bronze/silver/gold layers and SCD Type 2 patterns. |

## Domain-Driven Design

| Schema | Model | Schema Description | Model Highlights |
| --- | --- | --- | --- |
| `ddd-full/ddd-schema.yaml` | `ddd-full/ddd-model.yaml` | Comprehensive DDD system architecture schema spanning strategic and tactical concepts. | Job Seeker Application blueprint covering domains, bounded contexts, aggregates, services, and events. |
| `ddd-part/strategic-ddd.schema.yaml` | `ddd-part/strategic-example.yaml` | Strategic DDD patterns for domains, bounded contexts, and context mappings. | Strategic view of the Job Seeker Application with context mappings across bounded contexts. |
| `ddd-part/strategic-ddd.schema.yaml` | `ddd-part/bff-example.yaml` | Strategic DDD patterns for domains, bounded contexts, and context mappings. | Web application BFF demonstrating aggregation across bounded contexts and upstream dependencies. |
| `ddd-part/tactical-ddd.schema.yaml` | `ddd-part/tactical-example.yaml` | Tactical DDD patterns covering aggregates, entities, value objects, services, and repositories. | Tactical view of Job Seeker domain with aggregates, entities, value objects, and service boundaries. |
| `ddd-part/tactical-ddd.schema.yaml` | `ddd-part/application-service-example.yaml` | Tactical DDD patterns covering aggregates, entities, value objects, services, and repositories. | Application service example illustrating CQRS workflow for user management. |

## Quality Engineering

| Schema | Model | Schema Description | Model Highlights |
| --- | --- | --- | --- |
| `qe/model-schema.yaml` | `qe/qe-schema-example.yaml` | Quality Engineering schema aligning test strategy, coverage, and DDD/UX integration points. | Job Seeker Application QE plan referencing DDD bounded contexts and UX journeys across release stages. |

## UX Architecture

| Schema | Model | Schema Description | Model Highlights |
| --- | --- | --- | --- |
| `ux/interaction-ux.schema.yaml` | `ux/interaction-example.yaml` | UX interaction schema for workflows, UI components, behaviors, and design system linkages. | E-commerce interaction design showing workflows, component library usage, and behavior rules. |
| `ux/navigation-ux.schema.yaml` | `ux/navigation-example.yaml` | UX navigation schema for global/local navigation, page structures, and wayfinding aids. | E-commerce navigation model with breadcrumbs, mega-menus, and contextual navigation patterns. |
| `ux/structure-ux.schema.yaml` | `ux/structure-example.yaml` | UX information architecture schema for content hierarchy, facets, and search structures. | E-commerce IA detailing product hierarchy, tagging facets, and search affordances. |

