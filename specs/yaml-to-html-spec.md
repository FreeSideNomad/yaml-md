# YAML to HTML Conversion Specification

## Overview
Authoritative rules for rendering YAML documents (driven by the schema tree visitor) into a **single-page HTML application**. These instructions extend `yaml-to-md-spec.md` and override Markdown-specific behavior where necessary.

## Implementation Requirements
- Implement an `HtmlVisitor` (parallel to the Markdown visitor) that consumes schema metadata and document data without any schema- or model-specific hardcoding. All behavior must derive from the schema tree structure and the document content.
- The visitor must respect naming fallbacks, relationship discovery, and all traversal conventions defined in `yaml_schema_tree.py` so it remains completely generic across schemas.

## Global Layout & Assets
- Output exactly one self-contained HTML document.
- Include Primer CSS and JavaScript from the official CDN. Load Primer utilities before any custom styles/scripts.
- Embed any custom CSS and JavaScript inline in `<style>`/`<script>` blocks after the Primer assets.
- Wrap the entire experience in a `<div id="app">` that contains a navigation region and a content region.
- Use semantic HTML (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<table>`, etc.) where applicable.
- All schema concepts from `yaml-to-md-spec.md` still apply (humanization, naming fallbacks, property ordering, anchor generation) unless explicitly overridden.
- Provide a persistent breadcrumb bar (`<nav aria-label="Breadcrumb">`) directly above the active type content. The breadcrumb must always start with “Home” linking to the default view (hash `#` or equivalent). Intermediate crumbs represent each level in the schema hierarchy leading to the current item, with each crumb linking to its corresponding section anchor.

## Navigation & View Management
- Render a **single navigation menu** (`<nav>`), listing every schema type in schema order. Use humanized display names (heading fallback chain) as link text.
- Links should point to `#type_id` anchors so deep linking works on refresh. When the user selects a link, update `window.location.hash` and scroll the corresponding type into view.
- Default view:
  - If the schema exposes exactly **one top-level type**, show it immediately.
- Otherwise render an index view of top-level types (humanized, hyperlinked). Hide type detail sections until the user selects a type.
- Only one type detail panel may be visible at a time. Hide inactive sections using a utility class (e.g., `display: none`) toggled via JavaScript.
- Persist the active type across reloads by reading `window.location.hash` on load. If no hash exists, fall back to the default view rule above.
- Breadcrumb navigation must update whenever the active type changes and should reflect nested context (e.g., `Home / Bounded Context / Aggregates / Candidate Profile`). Selecting any crumb navigates to that anchor and updates the hash so browser back/forward buttons mirror user navigation.
- Ensure `hashchange` and history updates keep browser back/forward buttons in sync with the active view. When navigating back to the home hash, show the index view again.

## Type Detail Sections
- Each type renders inside its own `<section class="type-view" id="type_id" data-type="type_name">`.
- Insert a `<header>` containing the type name (apply the standard display-name fallback sequence).
- Render the type content in the following order:
  1. Simple attributes and enums.
  2. Arrays (objects → references → primitives → untyped).
  3. Nested single objects.
- Maintain the value formatting rules from the Markdown spec (humanized labels, blank values when missing, fallback naming for linked targets).
- When inline objects or schema types have no child arrays/objects (leaf shortcut), render them as single-row tables (see **Leaf Tables**).
- Include anchor targets for any object with an `id`. Use `<a id="object_id"></a>` immediately before the element that introduces the object.

### Simple Attributes & Enums
- Render as a responsive key/value grid using Primer `ActionList` components or a simple definition list (`<dl class="type-attributes">`).
- For each attribute:
  - `<dt>` = humanized attribute name.
  - `<dd>` = literal value (blank if missing).
- Boolean and numeric values remain literal text; enums show only the selected value.

### Single References
- Display within the attribute grid as `<dd><a href="#target_id">Display Name</a></dd>`.
- If the target lacks an `id`, show the raw value without a link.

## Array Rendering
All arrays render as tables displayed inside a **horizontal tab set** per type. Use Primer `TabNav` for the tab bar and Primer table styles for content.

### Tab Framework
- Place a single `<div class="tabbed-tables">` inside each type section.
- Create a `<nav class="TabNav">` with one `<button>` per table-producing array. Buttons should reference the corresponding panel via `aria-controls`.
- Render each table inside `<div role="tabpanel" class="TabPanel" id="panel-type-arrayname">`.
- Only one tab panel should be visible at a time (toggle `hidden` attribute or a CSS utility class).
- If a type has no tables, omit the tab framework entirely.

### Arrays of Objects & References
- Precede each table by setting the tab label to the array’s humanized name (e.g., “Aggregates”, “Repositories”).
- Tables follow Primer `.Table` styles. First column header = humanized node name.
- First column cells show the object’s display name and link to `#id` when available.
- Remaining columns enumerate simple attributes in YAML order, using humanized headers. Empty values render as empty cells.
- Nested arrays/objects belonging to a row render in their own type sections and should not be expanded inside the table.
- Reverse relationships share the same treatment. Suggest tab labels such as “Referenced by Repositories” for clarity.

### Arrays of Primitives
- Display as a tab, with the table containing a single column labeled by the humanized array name.
- Each element occupies its own row. For key/value primitives, show `key: value` pairs inline.
- Empty arrays should omit the tab entirely.

### Arrays Without Declared Item Type
- Render as a tab containing a bullet list. Use `<ul class="ActionList">` with one `<li>` per item.
- Scalar entries display their value directly. Complex entries render concise `key: value` summaries using the item’s simple attributes.

## Nested Single Objects
- Render nested objects as their own type sections reusing all rules above. If an object should stay embedded within its parent panel, render it in a collapsible `<details>` component titled with the object’s display name.
- Maintain the leaf table shortcut: if the nested object has only simple attributes/references, render them as a single-row table (in the parent’s tab set or directly within the panel if tabs are absent).

## Leaf Tables
- When a type or inline object is composed entirely of simple attributes and references, render a single-row Primer table with the schema attributes as headers and document values in the lone body row.
- Do not duplicate the same fields in the attribute grid when this shortcut is used.

## JavaScript Behavior
- Provide a lightweight controller that:
  - Initializes navigation, tab switching, and view toggling.
  - Adds/removes `is-active` classes on navigation items and tabs.
  - Manages `hidden` or `display` states to keep only the active type panel visible.
  - Listens for `hashchange` events to update the active panel.
  - Rebuilds breadcrumb markup on each view change and keeps the location hash synchronized so browser history navigation works naturally (back/forward).
  - Persists the last active tab per type (optional but recommended) using `data-*` attributes or in-memory state.

## Accessibility
- Tabs must implement `aria-selected`, `role="tab"`, and `role="tabpanel"` semantics.
- Provide `aria-controls`/`aria-labelledby` relationships for navigation and tab interactions.
- Ensure color contrast meets WCAG by relying on Primer variables.
- Use focus states on navigation links and tab buttons to aid keyboard users.

## Styling Notes
- Prefer Primer layout utilities (`Flex`, `Grid`, `Box`, spacing utilities) over custom CSS.
- Keep custom CSS minimal: view toggling, tab panel visibility, and responsive adjustments.
- Add a `.hidden` utility class (e.g., `display: none`) for sections and tab panels.
- For mobile, stack navigation above the content and convert the tab bar into a horizontal scrollable list.

## Example Structure (Simplified)
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="https://unpkg.com/@primer/css/dist/primer.css">
    <script src="https://unpkg.com/@primer/react"></script>
    <style>
      .hidden { display: none !important; }
    </style>
  </head>
  <body>
    <div id="app" class="Layout Layout--flowRow-until-lg">
      <nav class="Layout-sidebar">
        <ul class="ActionList">
          <li><a href="#agg_candidate_profile" class="ActionList-content">Candidate Profile</a></li>
          <!-- more links -->
        </ul>
      </nav>
      <main class="Layout-main">
        <section id="agg_candidate_profile" class="type-view">
          <header><h1>Candidate Profile</h1></header>
          <nav aria-label="Breadcrumb" class="Breadcrumbs">
            <ol>
              <li><a href="#">Home</a></li>
              <li><a href="#bounded_context_core">Bounded Context</a></li>
              <li><a href="#agg_candidate_profile">Candidate Profile</a></li>
            </ol>
          </nav>
          <dl class="type-attributes">
            <dt>Description</dt><dd>Core aggregate</dd>
            <dt>Status</dt><dd>active</dd>
            <dt>Domain</dt><dd><a href="#dom_job_matching">Job Matching</a></dd>
          </dl>
          <div class="tabbed-tables">
            <nav class="TabNav" role="tablist">
              <button role="tab" aria-selected="true" aria-controls="panel-agg_candidate_profile-aggregates">Aggregates</button>
              <button role="tab" aria-selected="false" aria-controls="panel-agg_candidate_profile-repositories">Repositories</button>
            </nav>
            <div id="panel-agg_candidate_profile-aggregates" role="tabpanel">
              <table class="Table">
                <thead>
                  <tr><th>Aggregate</th><th>Summary</th></tr>
                </thead>
                <tbody>
                  <tr>
                    <td><a href="#agg_candidate_profile">Candidate Profile</a></td>
                    <td>Matches candidates to jobs</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div id="panel-agg_candidate_profile-repositories" role="tabpanel" class="hidden">
              <!-- table content -->
            </div>
          </div>
        </section>
        <!-- additional sections -->
      </main>
    </div>
    <script>
      // minimal controller to handle nav and tab interactions
    </script>
  </body>
</html>
```

These rules guarantee that every renderer produces consistent, Primer-styled HTML that mirrors the schema semantics while meeting the project’s single-view and tabbed-table requirements.
