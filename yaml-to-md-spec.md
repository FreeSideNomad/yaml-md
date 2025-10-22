# YAML to Markdown Conversion Specification

## Overview
Guidelines for translating YAML documents into structured Markdown using the schema-driven visitor. The rules below are exhaustive for every node shape encountered in the generated tree so that multiple renderers can produce identical output.

## Global Rendering Rules
- **Heading content**: Every schema type (root or nested) renders as a heading using the humanized node name. If the humanized name is missing or empty, fall back to `description`, then `id`, then a space-separated concatenation of up to three available simple attribute values (in document order).
- **Heading depth**: Depth increases with hierarchy. Root types use `#`, their children `##`, and so on.
- **Property order inside a section**: 
  1. Simple attributes (scalar values and enums).
  2. Arrays (objects first, then references, then primitives, then arrays without type).
  3. Nested single objects.
- **Humanization**: Convert `snake_case`/`camelCase` identifiers to Title Case everywhere they appear (headings, column headers, link text).
- **Missing values**: When a simple attribute lacks a value, render an empty value after the colon (i.e., `Field Name:` with nothing following).
- **Anchors**: Whenever a row or list item points to an object with an `id`, link using `[#id]` so navigation works across the document.
- **Table headings**: Every table must be preceded by a heading derived from the array or relationship name it represents. Humanize that name using the same fallback logic as section headings.
- **Name derivation fallback**: When both `name` and `description` are absent or empty, derive a humanized label from the `id` by dropping common type prefixes (e.g., `vo_`, `ent_`, `agg_`, `repo_`, `evt_`, `factory_`, `svc_dom_`, `svc_app_`) and then applying Title Case to the remainder (e.g., `vo_match_score` → “Match Score”).

## Node Type Rules

### Schema Type Nodes (`[type]`)
- Render a heading at the appropriate depth using the global heading content rule.
- Immediately below the heading, list that node’s simple attributes as `Field Name: value`, one per line.
- After simple attributes, render arrays and nested single objects following the rules in this section.
- **Leaf shortcut**: When a schema type (or inline object) has no child arrays or nested objects in its schema definition—i.e., it consists entirely of simple attributes and references—render those fields as a single-row table instead of individual `Field: value` lines. Use humanized attribute names as the header row (preserve YAML order) and place the corresponding values in the row. Do not repeat the attributes in list form when this shortcut is applied.

### Simple Attributes (`attribute[string|number|integer|boolean]`)
- Output as `Humanized Name: value`.
- If the value is missing, leave it blank after the colon.
- Boolean and numeric values use their literal text representation.

### Enum Attributes (`attribute[enum: ...]`)
- Treat as a simple attribute and display only the selected enum value (no enumeration of allowed options).

### Single Reference Fields (`reference→Type`)
- Render as `Humanized Name: [Humanized Target](#target_id)` when the referenced object has an `id`. The link text uses the reference’s humanized display name fallback chain (name → description → id → concatenated values).
- If the target cannot be resolved to an `id`, display the raw value while still humanizing the label (e.g., `Parent Ref: value123`).

### Arrays of References (`array[reference→Type]`)
- Treat identically to arrays of objects: render as a table.
- First column: humanized description of each referenced object, linked to `#id`.
- Subsequent columns: all available simple attributes of the referenced object, in document order.
- If a referenced object cannot be resolved, show a fallback row with the raw reference value in the first column and leave other cells blank.

### Arrays of Objects (`array[object]`)
- Render a Markdown table.
- Precede the table with a heading based on the array name (humanized).
- First column header: humanized node name.
- First column cells: link text derived from the object’s display name (name → description → id → concatenated simple values) linking to `#id`. If no `id`, omit the link.
- Remaining columns: every simple attribute for that object, in YAML order, humanized as column headers. Cells contain the attribute values (blank if missing).
- Nested arrays/objects inside each row are not expanded in the table; handle them in separate nested sections below the table if needed.

### Arrays of Primitive Values (`array[string|number|integer|boolean]`)
- Render as `Humanized Name: value1 value2 value3`.
- Values appear space-separated on the same line.
- If the array is empty, omit the line.

### Arrays Without Declared Item Type (`array`)
- Render as a bullet list under a humanized label:
  ```
  Humanized Name:
  - key1: valueA valueB
  - key2: …
  ```
- Each bullet may contain a concise summary of the item’s simple attributes as space-separated `key: value` pairs. For scalar items, list the value directly.

### Nested Single Objects (`object`)
- Create a subheading using the global heading rule.
- List simple attributes immediately below the heading.
- Process any arrays or deeper nested objects using the same rules recursively so the structure mirrors the schema hierarchy.
- Leaf objects (no child arrays/objects) may reuse the table shortcut described above instead of key-value lines.

### Synthetic Reverse Relationship Nodes (`array[reference→Type]` generated automatically)
- Treat exactly like forward arrays of references: render as tables with the first column linking to each related object’s `#id` and subsequent columns for simple attributes. Precede the table with a heading such as “Referenced by …” derived from the synthetic property name.
- Use a humanized heading or label that clarifies it represents “Referenced by …” if the schema name alone is ambiguous.

## Examples

### Array of Objects
```markdown
## Permissions

| Permission | Level | Description |
|------------|-------|-------------|
| [Read Data](#perm_read_data) | full | Full access |
| [Write Data](#perm_write_data) | restricted | Limited write |
```

### Array of References
```markdown
## Domains

| Domain | Type | Description |
|--------|------|-------------|
| [Job Matching](#dom_job_matching) | core | Core domain for matching |
| [Profile Intelligence](#dom_profile_intelligence) | supporting | Profile enrichment |
```

### Array of Simple Values
```markdown
Tags: engineering senior remote
```

### Nested Object
```markdown
## Metadata

Established: 2015
Budget: 1000000
```

### Single Reference
```markdown
Aggregate Ref: [Candidate Profile](#agg_candidate_profile)
```

These rules ensure consistent, navigable Markdown output regardless of renderer implementation.
