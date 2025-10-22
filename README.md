# YAML Documentation Generator

A generic framework for generating documentation from YAML schemas and documents.

## Components

### 1. Schema Tree Generator (`yaml_schema_tree.py`)

Generates a navigable tree structure from a YAML schema definition.

**Usage:**
```bash
python yaml_schema_tree.py <schema_file> [--stats] [--no-humanize]
```

**Features:**
- Analyzes schema `$defs` to build type hierarchy
- Detects relationships through `type: reference` and `ref_type` fields
- Handles nested objects and arrays
- Adds reverse relationships automatically
- Outputs ASCII tree with type annotations
- **Completely generic** - works with any schema structure

**Output:**
- Non-humanized tree (for navigation): Use `--no-humanize` flag
- Humanized tree (for display): Default behavior
- Statistics: Use `--stats` flag

**Example:**
```bash
python yaml_schema_tree.py samples/ddd-schema.yaml --no-humanize > ddd-tree.md
```

### 2. Document Visitor (`yaml_visitor_final.py`)

Visits every node in a YAML document using the schema tree structure and extracts values.

**Usage:**
```bash
python yaml_visitor_final.py <schema_file> <document_file> <output_file>
```

**Features:**
- Uses schema tree for navigation
- Resolves references by ID
- Handles both inline objects and reference arrays
- Detects and prevents infinite cycles
- Extracts actual values from document
- **Completely generic** - no hardcoded schema types

**Output:**
- Markdown file with all node paths and their values
- Statistics on nodes found vs not found

**Example:**
```bash
python yaml_visitor_final.py samples/ddd-schema.yaml samples/ddd-model.yaml ddd-tree-values.md
```

## Schema Requirements

For the tools to work, your YAML schema must follow these conventions:

### 1. Schema Structure
```yaml
$defs:
  type_name:
    type: object
    properties:
      field_name:
        type: string
```

### 2. References
Single reference:
```yaml
domain_ref:
  type: reference
  ref_type: domain
```

Array of references:
```yaml
domains:
  type: array
  items:
    type: reference
    ref_type: domain
```

### 3. Inline Objects
```yaml
attributes:
  type: array
  items:
    type: object
    properties:
      name: {type: string}
      type: {type: string}
```

## Document Requirements

For the visitor to extract values, your YAML document should:

1. **Use IDs for references:** Objects should have an `id` field
2. **Reference by ID:** Use ID strings or full objects in arrays
3. **Match schema structure:** Field names should match schema definitions

## Output Files

- **`ddd-tree.md`** - Non-humanized schema tree for navigation
- **`ddd-tree-values.md`** - Document values extracted using the tree
- **`yaml-schema-tree.md`** - Specification for tree generation
- **`yaml-to-md-spec.md`** - Specification for YAML to Markdown conversion

## Examples

### Generate Schema Tree
```bash
# With humanized names (for display)
python yaml_schema_tree.py samples/ddd-schema.yaml --stats

# Without humanized names (for navigation)
python yaml_schema_tree.py samples/ddd-schema.yaml --no-humanize > ddd-tree.md
```

### Visit Document
```bash
python yaml_visitor_final.py samples/ddd-schema.yaml samples/ddd-model.yaml output.md
```

## Generic Design

Both tools are **completely generic** and work with any YAML schema/document:

- **No hardcoded type names** - All types discovered from schema `$defs`
- **No hardcoded field names** - All fields discovered from schema properties
- **No hardcoded relationships** - All relationships discovered through `type: reference`
- **Flexible document structure** - Handles both ID references and inline objects

## Architecture

```
┌─────────────────┐
│  YAML Schema    │
│  ($defs)        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  yaml_schema_tree.py    │
│  - Parses $defs         │
│  - Builds relationships │
│  - Generates tree       │
└────────┬────────────────┘
         │
         ├──► ddd-tree.md (navigation tree)
         │
         ▼
┌─────────────────────────┐      ┌──────────────┐
│  yaml_visitor_final.py  │◄─────┤ YAML Document│
│  - Loads tree structure │      └──────────────┘
│  - Visits all nodes     │
│  - Extracts values      │
│  - Resolves references  │
└────────┬────────────────┘
         │
         ▼
  ddd-tree-values.md (extracted values)
```

## Type Annotations

The tree includes type annotations for each node:

- `attribute[string]` - Simple string field
- `attribute[boolean]` - Boolean field
- `attribute[enum: ...]` - Enumeration with possible values
- `array[string]` - Array of strings
- `array[object]` - Array of inline objects
- `array[reference→type]` - Array of references to a type
- `reference→type` - Single reference to a type
- `object` - Nested object
- `[type]` - Schema type (no prefix)

## Configuration

The visitor can be customized by modifying:

1. **ID field name** - Change `'id'` in `get_object_id()` and `build_id_index()`
2. **Root type detection** - Modify root finding logic in `main()`
3. **Cycle detection** - Adjust `visit_key` generation in `visit_tree()`

## Virtual Environment

Always use the virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml
```

See `.claude.md` for project-specific instructions.
