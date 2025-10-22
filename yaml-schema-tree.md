# YAML Schema Tree Visualization Specification

## Overview
This specification defines how to create a Python script that analyzes a YAML schema file and generates an ASCII tree visualization showing the parent-child relationships between schema definitions.

## Input
A YAML schema file that defines object types and their relationships, typically using:
- A `$defs` section containing type definitions
- `properties` within each type definition
- `type: reference` and `ref_type` to indicate parent-child relationships
- Arrays that contain references to other types

## Output
An ASCII tree representation showing the hierarchical structure of schema types.

## Core Principles

### 1. Type Definition Discovery
- Parse the schema to identify all defined types (typically in `$defs` section)
- Each type definition represents a potential node in the tree

### 2. Relationship Identification
Look for parent-child relationships through:
- **Reference properties**: Properties with `type: reference` and `ref_type: <type_name>`
- **Array items**: Arrays where `items.type: reference` and `items.ref_type: <type_name>`
- **Direct containment**: Properties that reference other defined types

### 3. Tree Building Logic
1. Identify root types (types that are not referenced as children by others, or explicitly top-level)
2. For each type, find all types it references
3. Build hierarchical structure based on containment relationships

### 4. ASCII Tree Formatting
Use standard ASCII tree characters:
```
├── Child item
│   ├── Grandchild item
│   └── Last grandchild item
└── Last child item
```

Characters:
- `├──` : Branch with more siblings below
- `└──` : Last branch (no more siblings)
- `│   ` : Vertical line for continuation
- `    ` : Empty space (no continuation)

## Relationship Detection Rules

### Rule 1: Direct Reference
```yaml
bounded_context:
  properties:
    domain_ref:
      type: reference
      ref_type: domain
```
**Interpretation**: `bounded_context` is a child of `domain`

### Rule 2: Array of References
```yaml
domain:
  properties:
    bounded_contexts:
      type: array
      items:
        type: reference
        ref_type: bounded_context
```
**Interpretation**: `domain` contains multiple `bounded_context` children

### Rule 3: Bidirectional Relationships
When both parent→child and child→parent references exist:
- Use the "contains" relationship (array) as primary
- The type that contains an array of others is the parent

## Algorithm

### Step 1: Parse Schema
```python
def parse_schema(yaml_file):
    1. Load YAML file
    2. Extract all type definitions from $defs
    3. Return dictionary of {type_name: type_definition}
```

### Step 2: Build Relationship Map
```python
def build_relationships(type_definitions):
    for each type_def:
        for each property in type_def.properties:
            if property is reference:
                record relationship: type_def contains property.ref_type
            if property is array of references:
                record relationship: type_def contains property.items.ref_type
    return parent_to_children map
```

### Step 3: Identify Root Nodes
```python
def find_roots(type_definitions, relationships):
    1. Find all types that are never children
    2. Or use explicit root indicators (e.g., 'system' type)
    3. Return list of root type names
```

### Step 4: Generate ASCII Tree
```python
def generate_tree(root_type, relationships, prefix="", is_last=True):
    1. Print current node with appropriate prefix
    2. Get children of current node from relationships
    3. For each child:
        a. Determine if it's the last child
        b. Create new prefix based on is_last
        c. Recursively generate_tree for child
```

## Example Input (from ddd-schema.yaml)

```yaml
$defs:
  system:
    properties:
      domains:
        type: array
        items:
          type: reference
          ref_type: domain

  domain:
    properties:
      bounded_contexts:
        type: array
        items:
          type: reference
          ref_type: bounded_context

  bounded_context:
    properties:
      domain_ref:
        type: reference
        ref_type: domain
      aggregates:
        type: array
        items:
          type: reference
          ref_type: aggregate

  aggregate:
    properties:
      bounded_context_ref:
        type: reference
        ref_type: bounded_context
      entities:
        type: array
        items:
          type: reference
          ref_type: entity
      value_objects:
        type: array
        items:
          type: reference
          ref_type: value_object

  entity:
    properties:
      aggregate_ref:
        type: reference
        ref_type: aggregate

  value_object:
    properties:
      aggregate_ref:
        type: reference
        ref_type: aggregate
```

## Example Output

```
system
└── domain
    └── bounded_context
        ├── aggregate
        │   ├── entity
        │   └── value_object
        ├── repository
        ├── domain_service
        ├── application_service
        ├── domain_event
        └── factory
```

Or with more detail:

```
System Architecture
└── Domain
    └── Bounded Context
        ├── Strategic Patterns
        │   └── Context Mapping
        └── Tactical Patterns
            ├── Aggregate
            │   ├── Entity (Aggregate Root)
            │   ├── Entity (Internal)
            │   └── Value Object
            ├── Repository
            ├── Domain Service
            ├── Application Service
            ├── Domain Event
            ├── Factory
            └── Specification
```

## Python Script Structure

### Required Libraries
```python
import yaml
from collections import defaultdict
```

### Main Functions

#### 1. Load Schema
```python
def load_schema(schema_file: str) -> dict:
    """Load and parse YAML schema file."""
    with open(schema_file, 'r') as f:
        return yaml.safe_load(f)
```

#### 2. Extract Type Definitions
```python
def extract_types(schema: dict) -> dict:
    """Extract all type definitions from schema."""
    return schema.get('$defs', {})
```

#### 3. Build Parent-Child Relationships
```python
def build_relationships(type_defs: dict) -> dict:
    """
    Build parent->children relationship map.
    Returns: {parent_type: [child_type1, child_type2, ...]}
    """
    relationships = defaultdict(list)

    for type_name, type_def in type_defs.items():
        properties = type_def.get('properties', {})

        for prop_name, prop_def in properties.items():
            # Check for array of references
            if prop_def.get('type') == 'array':
                items = prop_def.get('items', {})
                if items.get('type') == 'reference':
                    child_type = items.get('ref_type')
                    if child_type:
                        relationships[type_name].append(child_type)

            # Check for direct reference
            elif prop_def.get('type') == 'reference':
                # This indicates parent relationship (inverse)
                # Skip or handle based on needs
                pass

    return relationships
```

#### 4. Find Root Types
```python
def find_root_types(type_defs: dict, relationships: dict) -> list:
    """Find types that are not children of any other type."""
    all_types = set(type_defs.keys())
    child_types = set()

    for children in relationships.values():
        child_types.update(children)

    roots = all_types - child_types

    # Prefer 'system' if it exists
    if 'system' in roots:
        return ['system']

    return list(roots)
```

#### 5. Generate ASCII Tree
```python
def print_tree(type_name: str, relationships: dict, prefix: str = "", is_last: bool = True):
    """Recursively print ASCII tree."""
    # Determine connector
    connector = "└── " if is_last else "├── "

    # Print current node
    print(f"{prefix}{connector}{type_name}")

    # Get children
    children = relationships.get(type_name, [])

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Print children
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        print_tree(child, relationships, child_prefix, is_last_child)
```

#### 6. Main Function
```python
def main(schema_file: str):
    """Main function to generate tree from schema."""
    # Load schema
    schema = load_schema(schema_file)

    # Extract type definitions
    type_defs = extract_types(schema)

    # Build relationships
    relationships = build_relationships(type_defs)

    # Find root types
    roots = find_root_types(type_defs, relationships)

    # Generate tree for each root
    for i, root in enumerate(roots):
        print_tree(root, relationships, "", True)
        if i < len(roots) - 1:
            print()  # Blank line between multiple trees
```

## Usage

```bash
python yaml_schema_tree.py samples/ddd-schema.yaml
```

## Advanced Features (Optional)

### 1. Humanize Type Names
Convert `snake_case` type names to `Title Case` for display:
```python
def humanize(name: str) -> str:
    """Convert snake_case to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('_'))
```

### 2. Show Cardinality
Indicate one-to-many relationships:
```
domain
└── bounded_contexts [*]
    └── aggregates [*]
        └── entities [*]
```

### 3. Group by Category
Use schema metadata to group types:
```
system
└── domain
    └── bounded_context
        ├── [Strategic Patterns]
        │   └── context_mapping
        └── [Tactical Patterns]
            ├── aggregate
            ├── entity
            └── value_object
```

### 4. Cycle Detection
Detect and handle circular references:
```python
def print_tree_with_cycle_detection(type_name, relationships, visited=None, ...):
    if visited is None:
        visited = set()

    if type_name in visited:
        print(f"{prefix}{connector}{type_name} [CYCLE]")
        return

    visited.add(type_name)
    # ... rest of tree printing
    visited.remove(type_name)
```

## Edge Cases

1. **Orphan types**: Types not referenced by anyone and don't reference anyone
   - Display in separate section or at root level

2. **Circular references**: Type A references Type B which references Type A
   - Detect and mark with `[CYCLE]` or `[→]` indicator

3. **Multiple parents**: A child type referenced by multiple parents
   - Show under each parent or show once with `[→]` reference marker

4. **Empty relationships**: Types with no children
   - Display as leaf nodes (no branches below)

## Output Variations

### Compact Mode
```
system→domain→bounded_context→aggregate→entity
                             →value_object
```

### Detailed Mode with Descriptions
```
system (The entire software system)
└── domain (Sphere of knowledge and activity)
    └── bounded_context (Explicit boundary for domain model)
        └── aggregate (Consistency boundary)
```

### Statistics Mode
```
Schema Statistics:
- Total types: 15
- Root types: 1
- Max depth: 4
- Leaf types: 5

Tree:
system
└── domain (3 children)
    └── bounded_context (8 children)
        └── aggregate (2 children)
```
