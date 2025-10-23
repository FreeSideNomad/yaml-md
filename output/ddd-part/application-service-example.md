# YAML Document Overview
Document: `/Users/igor/code/yaml-md/samples/ddd-part/application-service-example.yaml`
Schema: `/Users/igor/code/yaml-md/samples/ddd-part/tactical-ddd.schema.yaml`
Objects Indexed: 13

<a id="vo_user_id"></a>
# Value Object: UserId

Id: vo_user_id
Name: UserId
Bounded Context Ref: bc_user_management
Description: Unique identifier for a user (UUID-based)
Immutability: true

## Attributes

| Attribute | Type | Required | Validation |
| --------- | ---- | -------- | ---------- |
| id | String | true | UUID format |

Validation Rules: Cannot be null or blank Must be valid UUID string

Equality Criteria: id

<a id="vo_client_id"></a>
# Value Object: ClientId

Id: vo_client_id
Name: ClientId
Bounded Context Ref: bc_user_management
Description: URN-based identifier for clients (srf, gid, ind)
Immutability: true

## Attributes

| Attribute | Type | Required | Validation |
| --------- | ---- | -------- | ---------- |
| urn | String | true | ^(srf|gid|ind):[A-Za-z0-9_-]+$ |

Validation Rules: Must match pattern {system}:{clientNumber} System must be srf, gid, or ind

Equality Criteria: urn