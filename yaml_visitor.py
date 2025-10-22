#!/usr/bin/env python3
"""
YAML Document Visitor
Visits every node in a YAML document using the schema tree with proper cycle detection
"""

import yaml
import sys
from abc import ABC, abstractmethod
from yaml_schema_tree import load_schema, extract_types, build_relationships, humanize


class NodeVisitor(ABC):
    """Abstract visitor interface for handling traversal events."""

    def start(self, schema_file: str, document_file: str, total_objects: int):
        """Called before traversal begins."""

    def finish(self):
        """Called after traversal completes."""

    @abstractmethod
    def enter_schema_node(self, node_name: str, data_context: dict, indent: int):
        """Called when a schema type node is entered."""

    @abstractmethod
    def exit_schema_node(self, node_name: str, data_context: dict, indent: int):
        """Called after a schema type node and its descendants are processed."""

    def enter_inline_object(self, node_path: str, value: dict, indent: int):
        """Called when an inline object property is entered."""

    def exit_inline_object(self, node_path: str, value: dict, indent: int):
        """Called after an inline object property is processed."""

    @abstractmethod
    def handle_property(self, node_path: str, value, node_type: str, indent: int):
        """Handle a property node with resolved value."""

    def get_output_lines(self) -> list:
        """Return collected output lines if applicable."""
        return []


class TraceVisitor(NodeVisitor):
    """Collect traversal trace with values for debugging purposes."""

    def __init__(self):
        self.lines = []

    def start(self, schema_file: str, document_file: str, total_objects: int):
        self.lines.append("# YAML Document Trace")
        self.lines.append(f"# Document: {document_file}")
        self.lines.append(f"# Schema: {schema_file}")
        self.lines.append(f"# Total objects indexed: {total_objects}")
        self.lines.append("")

    def enter_schema_node(self, node_name: str, data_context: dict, indent: int):
        obj_display_id = data_context.get('id', '?') if isinstance(data_context, dict) else '?'
        self.lines.append(f"{'  ' * indent}{node_name} [type] (id: {obj_display_id})")

    def exit_schema_node(self, node_name: str, data_context: dict, indent: int):
        pass

    def enter_inline_object(self, node_path: str, value: dict, indent: int):
        self.lines.append(f"{'  ' * indent}{node_path} [object] → entering")

    def exit_inline_object(self, node_path: str, value: dict, indent: int):
        self.lines.append(f"{'  ' * indent}{node_path} [object] ← exiting")

    def handle_property(self, node_path: str, value, node_type: str, indent: int):
        prefix = "  " * indent
        node_type_display = node_type or "type"
        if value is None:
            display = "<not found>"
        elif isinstance(value, list):
            if value and all(isinstance(v, str) for v in value):
                preview = ', '.join(value[:3])
                if len(value) > 3:
                    preview += '...'
                display = f"[{len(value)} items: {preview}]"
            else:
                display = f"[{len(value)} items]"
        elif isinstance(value, dict):
            keys = ', '.join(list(value.keys())[:10])
            display = f"{{{keys}}}"
        else:
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + "..."
            display = value_str
        self.lines.append(f"{prefix}{node_path} [{node_type_display}]: {display}")

    def get_output_lines(self) -> list:
        return self.lines


def extract_id_prefixes(schema: dict) -> set:
    """Extract ID prefixes from schema naming conventions if available."""
    prefixes = set()
    naming = schema.get("naming_conventions", {})
    for pattern in naming.values():
        if not isinstance(pattern, str):
            continue
        if "<" in pattern:
            prefix = pattern.split("<", 1)[0]
            if prefix:
                prefixes.add(prefix)
    return prefixes


class MarkdownVisitor(NodeVisitor):
    """Render Markdown output following yaml-to-md-spec.md rules."""

    def __init__(self, relationships: dict, type_info: dict, id_index: dict, id_prefixes: set = None):
        self.relationships = relationships
        self.type_info = type_info
        self.id_index = id_index
        self.id_prefixes = tuple(sorted(id_prefixes or [], key=len, reverse=True))
        self.lines = []
        self.context_stack = []
        self.suppressed_prefixes = set()

    def start(self, schema_file: str, document_file: str, total_objects: int):
        self.lines = [
            "# YAML Document Overview",
            f"Document: `{document_file}`",
            f"Schema: `{schema_file}`",
            f"Objects Indexed: {total_objects}",
            ""
        ]

    def enter_schema_node(self, node_name: str, data_context: dict, indent: int):
        base_label = humanize(node_name)
        self._push_context(
            display_name=base_label,
            heading_level=min(6, len(self.context_stack) + 1),
            anchor=data_context.get('id') if isinstance(data_context, dict) else None,
            descriptor=self._describe_object(data_context)
        )

    def exit_schema_node(self, node_name: str, data_context: dict, indent: int):
        context = self.context_stack.pop()
        block = self._render_section(context)
        self._append_to_parent(block)

    def enter_inline_object(self, node_path: str, value: dict, indent: int):
        base_label = humanize(node_path.split('.')[-1])
        self._push_context(
            display_name=base_label,
            heading_level=min(6, len(self.context_stack) + 1),
            anchor=value.get('id') if isinstance(value, dict) else None,
            descriptor=self._describe_object(value)
        )

    def exit_inline_object(self, node_path: str, value: dict, indent: int):
        context = self.context_stack.pop()
        block = self._render_section(context)
        if self.context_stack:
            self.context_stack[-1]["inline_sections"].append(block)
        else:
            self._extend_with_block(self.lines, block)

    def handle_property(self, node_path: str, value, node_type: str, indent: int):
        context = self._current_context()
        if context is None:
            return

        if any(node_path.startswith(prefix) for prefix in self.suppressed_prefixes):
            return

        label = humanize(node_path.split('.')[-1])

        if node_type.startswith("attribute[") or node_type.startswith("attribute[enum"):
            context["simple"].append((label, self._format_scalar(value)))
        elif node_type.startswith("reference→"):
            link_text, link_anchor = self._reference_link(value)
            if link_anchor:
                context["simple"].append((label, f"[{link_text}](#{link_anchor})"))
            else:
                context["simple"].append((label, link_text))
        elif node_type.startswith("array[reference→") or node_type == "array[object]":
            table_lines = self._render_object_array_table(label, value)
            if table_lines:
                context["arrays"].append({
                    "type": "table",
                    "heading": label,
                    "lines": table_lines
                })
            if node_type == "array[object]":
                self.suppressed_prefixes.add(f"{node_path}.")
        elif node_type.startswith("array[") or node_type == "array":
            if node_type == "array":
                bullet_lines = self._render_untyped_array(label, value)
                if bullet_lines:
                    context["arrays"].append({
                        "type": "list",
                        "heading": label,
                        "lines": bullet_lines
                    })
            else:
                line = self._render_primitive_array_line(label, value)
                if line:
                    context["arrays"].append({
                        "type": "inline",
                        "heading": label,
                        "lines": [line]
                    })
        elif node_type == "object":
            if value is None:
                context["simple"].append((label, ""))
        else:
            context["simple"].append((label, self._format_scalar(value)))

    def finish(self):
        # Append any remaining open contexts (should not happen)
        while self.context_stack:
            context = self.context_stack.pop()
            block = self._render_section(context)
            self._extend_with_block(self.lines, block)
        # Trim trailing blank lines
        while self.lines and self.lines[-1] == "":
            self.lines.pop()

    def get_output_lines(self) -> list:
        return self.lines

    def _push_context(self, display_name: str, heading_level: int, anchor: str, descriptor: str):
        title = display_name
        if descriptor and descriptor != title:
            title = f"{title}: {descriptor}"
        self.context_stack.append({
            "title": title,
            "anchor": anchor,
            "heading_level": heading_level,
            "simple": [],
            "arrays": [],
            "inline_sections": [],
            "child_sections": []
        })

    def _append_to_parent(self, block: list):
        if not block:
            return
        if self.context_stack:
            self.context_stack[-1]["child_sections"].append(block)
        else:
            self._extend_with_block(self.lines, block)

    def _current_context(self):
        return self.context_stack[-1] if self.context_stack else None

    def _format_scalar(self, value):
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def _describe_object(self, obj):
        if not isinstance(obj, dict):
            return None
        name_val = obj.get("name")
        if isinstance(name_val, str) and name_val.strip():
            return name_val.strip()
        desc_val = obj.get("description")
        if isinstance(desc_val, str) and desc_val.strip():
            return desc_val.strip()
        id_val = obj.get("id")
        if isinstance(id_val, str) and id_val.strip():
            return self._label_from_identifier(id_val.strip())
        # Fallback to concatenation of up to three simple values
        values = []
        for key, val in obj.items():
            if isinstance(val, (dict, list)) or val in values:
                continue
            if val is None:
                continue
            if isinstance(val, bool):
                values.append("true" if val else "false")
            else:
                values.append(str(val))
            if len(values) == 3:
                break
        return " ".join(values) if values else None

    def _reference_link(self, value):
        if isinstance(value, str):
            target = self.id_index.get(value)
            text = self._describe_object(target) or value if target else value
            anchor = value if target else None
            return text or "", anchor
        elif isinstance(value, dict):
            target_id = value.get('id')
            text = self._describe_object(value)
            return text or (target_id or ""), target_id
        return self._format_scalar(value), None

    def _render_object_array_table(self, label: str, value):
        if not value:
            return []

        entries = []
        for item in value:
            if isinstance(item, dict):
                entries.append(item)
            elif isinstance(item, str):
                resolved = self.id_index.get(item)
                if resolved:
                    entries.append(resolved)
                else:
                    entries.append({"id": item})

        if not entries:
            return []

        column_label = self._singularize(label)
        simple_keys = []
        for item in entries:
            if not isinstance(item, dict):
                continue
            for key, val in item.items():
                if isinstance(val, (dict, list)):
                    continue
                if key not in simple_keys:
                    simple_keys.append(key)

        header = [column_label] + [humanize(key) for key in simple_keys]
        rows = []
        for item in entries:
            if isinstance(item, dict):
                first_cell = self._link_cell(item)
                row = [first_cell]
                for key in simple_keys:
                    row.append(self._format_scalar(item.get(key)))
                rows.append(row)
            else:
                text = self._format_scalar(item)
                rows.append([text] + [""] * len(simple_keys))

        return self._build_table(header, rows)

    def _render_primitive_array_line(self, label: str, value):
        if not value:
            return f"{label}:"
        formatted = []
        for item in value:
            if isinstance(item, bool):
                formatted.append("true" if item else "false")
            else:
                formatted.append(str(item))
        return f"{label}: {' '.join(formatted)}"

    def _render_untyped_array(self, label: str, value):
        lines = [f"{label}:"]
        if not value:
            return lines
        for item in value:
            if isinstance(item, dict):
                parts = []
                for key, val in item.items():
                    if isinstance(val, (dict, list)):
                        continue
                    parts.append(f"{humanize(key)}: {self._format_scalar(val)}")
                summary = " ".join(parts) if parts else self._format_scalar(item)
                lines.append(f"- {summary}")
            else:
                lines.append(f"- {self._format_scalar(item)}")
        return lines

    def _build_table(self, header, rows):
        line_header = "| " + " | ".join(header) + " |"
        line_divider = "| " + " | ".join("-" * max(3, len(h)) for h in header) + " |"
        table_lines = [line_header, line_divider]
        for row in rows:
            table_lines.append("| " + " | ".join(row) + " |")
        return table_lines

    def _link_cell(self, obj: dict):
        if not isinstance(obj, dict):
            text = self._format_scalar(obj)
            return text
        target_id = obj.get('id')
        text = self._describe_object(obj) or (target_id or "")
        if target_id:
            return f"[{text}](#{target_id})"
        return text

    def _singularize(self, label: str):
        if label.endswith('ies'):
            return label[:-3] + 'y'
        if label.endswith('s') and len(label) > 3:
            return label[:-1]
        return label

    def _render_leaf_table(self, context: dict) -> list:
        headers = [label for label, _ in context["simple"]]
        row = [value for _, value in context["simple"]]
        if not headers:
            return []
        table_lines = self._build_table(headers, [row])
        return table_lines

    def _render_array_block(self, block: dict, parent_heading_level: int) -> list:
        heading = block.get("heading")
        lines = []
        if block["type"] == "table":
            heading_level = min(6, parent_heading_level + 1)
            heading_text = heading or "Items"
            lines.append(f"{'#' * heading_level} {heading_text}")
            lines.append("")
            lines.extend(block["lines"])
        elif block["type"] == "list":
            lines.extend(block["lines"])
        else:
            lines.extend(block["lines"])
        return lines

    def _label_from_identifier(self, identifier: str) -> str:
        stripped = self._strip_prefix(identifier)
        stripped = stripped.replace('-', '_')
        stripped = stripped.strip('_')
        humanized = humanize(stripped) if stripped else identifier
        return humanized or identifier

    def _strip_prefix(self, identifier: str) -> str:
        for prefix in self.id_prefixes:
            if identifier.startswith(prefix):
                return identifier[len(prefix):]
        return identifier

    def _render_section(self, context: dict) -> list:
        lines = []
        if context["anchor"]:
            lines.append(f'<a id="{context["anchor"]}"></a>')
        lines.append(f"{'#' * context['heading_level']} {context['title']}")
        if context["simple"] or context["arrays"] or context["inline_sections"] or context["child_sections"]:
            lines.append("")

        is_leaf = (
            context["simple"]
            and not context["arrays"]
            and not context["inline_sections"]
            and not context["child_sections"]
        )

        if is_leaf:
            lines.extend(self._render_leaf_table(context))
        elif context["simple"]:
            for label, value in context["simple"]:
                lines.append(f"{label}: {value}")

        if context["arrays"]:
            if context["simple"] and not is_leaf:
                lines.append("")
            for idx, block in enumerate(context["arrays"]):
                if idx > 0:
                    lines.append("")
                lines.extend(self._render_array_block(block, context["heading_level"]))

        if context["inline_sections"]:
            if (context["simple"] and not is_leaf) or context["arrays"]:
                lines.append("")
            for idx, block in enumerate(context["inline_sections"]):
                if idx > 0:
                    lines.append("")
                lines.extend(block)

        if context["child_sections"]:
            if context["simple"] or context["arrays"] or context["inline_sections"]:
                lines.append("")
            for idx, block in enumerate(context["child_sections"]):
                if idx > 0:
                    lines.append("")
                lines.extend(block)

        return self._trim_blank_edges(lines)

    def _extend_with_block(self, target: list, block: list):
        block = self._trim_blank_edges(block)
        if not block:
            return
        if target and target[-1] != "":
            target.append("")
        target.extend(block)
        if target[-1] != "":
            target.append("")

    def _trim_blank_edges(self, lines: list) -> list:
        result = lines[:]
        while result and result[0] == "":
            result.pop(0)
        while result and result[-1] == "":
            result.pop()
        return result


def load_document(doc_file: str) -> dict:
    """Load YAML document (model/instance)."""
    with open(doc_file, 'r') as f:
        docs = list(yaml.safe_load_all(f))
        return docs[0] if docs else {}


def build_id_index(data: dict) -> dict:
    """Build an index of all objects by their ID."""
    index = {}

    def index_object(obj):
        if isinstance(obj, dict) and 'id' in obj:
            index[obj['id']] = obj

        if isinstance(obj, dict):
            for value in obj.values():
                if isinstance(value, list):
                    for item in value:
                        index_object(item)
                elif isinstance(value, dict):
                    index_object(value)
        elif isinstance(obj, list):
            for item in obj:
                index_object(item)

    index_object(data)
    return index


def resolve_reference(ref_value, id_index: dict):
    """Resolve a reference (ID string) to an actual object."""
    if isinstance(ref_value, str):
        return id_index.get(ref_value)
    elif isinstance(ref_value, list):
        results = []
        for item in ref_value:
            if isinstance(item, str) and item in id_index:
                results.append(id_index[item])
        return results if results else None
    return None


def get_object_id(obj):
    """Get a unique identifier for an object for cycle detection."""
    if isinstance(obj, dict):
        obj_id = obj.get('id')
        if obj_id:
            return f"obj:{obj_id}"
    return f"id:{id(obj)}"


def visit_value(node_path: str, data_context: dict, type_info: dict,
                root_data: dict) -> tuple:
    """Resolve value and capture node metadata."""
    node_type = type_info.get(node_path, "type")
    field_name = node_path.split('.')[-1]

    if isinstance(data_context, dict) and field_name in data_context:
        value = data_context[field_name]
    elif root_data and isinstance(root_data, dict) and field_name in root_data:
        value = root_data[field_name]
    else:
        value = None

    return value, node_type


def visit_tree(node_name: str, relationships: dict, type_info: dict, data_context: dict,
               id_index: dict, root_data: dict, visitor: NodeVisitor,
               visited_global: set, path_stack: list, schema_types: set, indent: int = 0):
    """
    Recursively visit all nodes in the tree.

    Args:
        visited_global: Set of (node_name, object_id) tuples we've fully processed
        path_stack: Current path to detect immediate cycles
        schema_types: Set of schema type names from the schema definition
    """
    obj_id = get_object_id(data_context)
    visit_key = f"{node_name}@{obj_id}"

    if visit_key in visited_global:
        return

    if visit_key in path_stack:
        return

    path_stack = path_stack + [visit_key]
    is_schema_type = '.' not in node_name and node_name in schema_types

    if is_schema_type:
        visitor.enter_schema_node(node_name, data_context, indent)
        visited_global.add(visit_key)

        children = relationships.get(node_name, [])
        for child in children:
            visit_tree(child, relationships, type_info, data_context,
                       id_index, root_data, visitor, visited_global, path_stack, schema_types, indent + 1)
        visitor.exit_schema_node(node_name, data_context, indent)
    else:
        value, node_type = visit_value(node_name, data_context, type_info, root_data)
        visitor.handle_property(node_name, value, node_type, indent)

        visited_global.add(visit_key)

        if isinstance(value, list) and 'array[reference→' in node_type:
            if value and isinstance(value[0], dict):
                resolved_objects = value
            elif value and isinstance(value[0], str):
                resolved_objects = resolve_reference(value, id_index)
            else:
                resolved_objects = None

            if resolved_objects:
                children = relationships.get(node_name, [])
                for resolved_obj in resolved_objects:
                    if isinstance(resolved_obj, dict):
                        for child in children:
                            visit_tree(child, relationships, type_info, resolved_obj,
                                       id_index, root_data, visitor,
                                       visited_global, path_stack, schema_types, indent + 1)

        elif 'reference→' in node_type and isinstance(value, str):
            resolved_obj = resolve_reference(value, id_index)
            if resolved_obj and isinstance(resolved_obj, dict):
                children = relationships.get(node_name, [])
                for child in children:
                    visit_tree(child, relationships, type_info, resolved_obj,
                               id_index, root_data, visitor,
                               visited_global, path_stack, schema_types, indent + 1)

        elif isinstance(value, list) and 'array[object]' in node_type:
            children = relationships.get(node_name, [])
            for item in value:
                if isinstance(item, dict):
                    for child in children:
                        visit_tree(child, relationships, type_info, item,
                                   id_index, root_data, visitor,
                                   visited_global, path_stack, schema_types, indent + 1)

        elif node_type == "object" and isinstance(value, dict):
            visitor.enter_inline_object(node_name, value, indent)
            children = relationships.get(node_name, [])
            for child in children:
                visit_tree(child, relationships, type_info, value,
                           id_index, root_data, visitor,
                           visited_global, path_stack, schema_types, indent + 1)
            visitor.exit_inline_object(node_name, value, indent)
        else:
            children = relationships.get(node_name, [])
            for child in children:
                visit_tree(child, relationships, type_info, data_context,
                           id_index, root_data, visitor,
                           visited_global, path_stack, schema_types, indent + 1)


def main(schema_file: str, document_file: str, output_file: str, trace: bool = False):
    """Main function to visit document and output values."""

    # Load schema and build tree
    print(f"Loading schema from {schema_file}...")
    schema = load_schema(schema_file)
    type_defs = extract_types(schema)
    relationships, type_info, schema_types = build_relationships(type_defs)
    id_prefixes = extract_id_prefixes(schema)

    # Load document
    print(f"Loading document from {document_file}...")
    full_data = load_document(document_file)

    # Build ID index
    print("Building ID index...")
    id_index = build_id_index(full_data)
    print(f"Indexed {len(id_index)} objects by ID")

    print("Visiting nodes...")
    if trace:
        visitor = TraceVisitor()
    else:
        visitor = MarkdownVisitor(relationships, type_info, id_index, id_prefixes)
    visitor.start(schema_file, document_file, len(id_index))
    visited_global = set()

    # Find root schema type in the document
    # Try common root names or use first schema type found in data
    root_type = None
    for schema_type in schema_types:
        if schema_type in full_data:
            root_type = schema_type
            break

    if root_type:
        print(f"Starting visit from root type: {root_type}")
        visit_tree(root_type, relationships, type_info, full_data[root_type],
                   id_index, full_data, visitor, visited_global, [], schema_types, 0)
    else:
        print(f"Warning: No root schema type found in document. Available keys: {list(full_data.keys())[:5]}")

    visitor.finish()
    output_lines = visitor.get_output_lines()

    # Write output
    print(f"Writing output to {output_file}...")
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))

    total_lines = len(output_lines)
    print("Done!")
    print(f"  Total lines: {total_lines}")
    print(f"  Unique visits: {len(visited_global)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    trace = False
    if "--trace" in args:
        trace = True
        args.remove("--trace")

    if len(args) < 3:
        print("Usage: python yaml_visitor.py <schema_file> <document_file> <output_file> [--trace]")
        sys.exit(1)

    schema_file, document_file, output_file = args[:3]

    main(schema_file, document_file, output_file, trace)
