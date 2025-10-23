#!/usr/bin/env python3
"""
YAML Schema Tree Generator
Generates ASCII tree visualization of schema hierarchies
"""

import yaml
from collections import defaultdict
import sys


def load_schema(schema_file: str) -> dict:
    """Load and parse YAML schema file."""
    with open(schema_file, 'r') as f:
        # Handle multiple documents - take the first one
        docs = list(yaml.safe_load_all(f))
        return docs[0] if docs else {}


def extract_types(schema: dict) -> dict:
    """Extract all type definitions from schema."""
    return schema.get('$defs', {})


def process_properties(parent_name: str, properties: dict, relationships: dict, type_info: dict):
    """Recursively process properties to find nested structures and references."""
    for prop_name, prop_def in properties.items():
        prop_type = prop_def.get('type')

        # Check for array
        if prop_type == 'array':
            items = prop_def.get('items', {})
            items_type = items.get('type') if items else None

            # Array of references - show as both edge AND node for navigation
            if items_type == 'reference':
                child_type = items.get('ref_type')
                # Create a reference array node
                inline_name = f"{parent_name}.{prop_name}"
                if inline_name not in relationships[parent_name]:
                    relationships[parent_name].append(inline_name)
                    type_info[inline_name] = f"array[reference→{child_type}]"
                # Also add the referenced type as child of the array node
                if child_type and child_type not in relationships[inline_name]:
                    relationships[inline_name].append(child_type)

            # Array of inline objects
            elif items_type == 'object':
                inline_name = f"{parent_name}.{prop_name}"
                if inline_name not in relationships[parent_name]:
                    relationships[parent_name].append(inline_name)
                    type_info[inline_name] = "array[object]"
                # Recursively process nested properties
                inline_props = items.get('properties', {})
                if inline_props:
                    process_properties(inline_name, inline_props, relationships, type_info)

            # Array of simple types - show as leaf
            elif items_type in ['string', 'number', 'integer', 'boolean']:
                inline_name = f"{parent_name}.{prop_name}"
                if inline_name not in relationships[parent_name]:
                    relationships[parent_name].append(inline_name)
                    type_info[inline_name] = f"array[{items_type}]"

            # Array without items definition or unknown type
            else:
                inline_name = f"{parent_name}.{prop_name}"
                if inline_name not in relationships[parent_name]:
                    relationships[parent_name].append(inline_name)
                    type_info[inline_name] = "array"

        # Single nested object (not array)
        elif prop_type == 'object':
            inline_name = f"{parent_name}.{prop_name}"
            if inline_name not in relationships[parent_name]:
                relationships[parent_name].append(inline_name)
                type_info[inline_name] = "object"
            # Recursively process nested properties
            nested_props = prop_def.get('properties', {})
            if nested_props:
                process_properties(inline_name, nested_props, relationships, type_info)

        # Direct reference - show as node for navigation
        elif prop_type == 'reference':
            ref_type = prop_def.get('ref_type')
            inline_name = f"{parent_name}.{prop_name}"
            if inline_name not in relationships[parent_name]:
                relationships[parent_name].append(inline_name)
                type_info[inline_name] = f"reference→{ref_type}"
            # Also add the referenced type as child
            if ref_type and ref_type not in relationships[inline_name]:
                relationships[inline_name].append(ref_type)

        # Simple types - show as leaf attributes
        elif prop_type in ['string', 'number', 'integer', 'boolean', 'enum']:
            inline_name = f"{parent_name}.{prop_name}"
            if inline_name not in relationships[parent_name]:
                relationships[parent_name].append(inline_name)
                if prop_type == 'enum':
                    values = prop_def.get('values', [])
                    type_info[inline_name] = f"attribute[enum: {', '.join(map(str, values[:3]))}{'...' if len(values) > 3 else ''}]"
                else:
                    type_info[inline_name] = f"attribute[{prop_type}]"


def pluralize(word: str) -> str:
    """Simple pluralization for type names."""
    # Handle compound words with underscore
    if '_' in word:
        parts = word.split('_')
        parts[-1] = pluralize(parts[-1])
        return '_'.join(parts)

    # Simple pluralization rules
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    else:
        return word + 's'


def add_reverse_relationships(type_defs: dict, relationships: dict, type_info: dict):
    """
    Add reverse relationships for reference fields.
    If Type A has a reference to Type B, add Type A as child of Type B.
    """
    reverse_refs = defaultdict(list)

    # Collect all reference relationships
    for parent_name, children in list(relationships.items()):
        for child in children:
            # Check if this is a reference node
            if child in type_info and 'reference→' in type_info[child]:
                # Extract the referenced type
                ref_type = type_info[child].split('→')[1]
                if ref_type and ref_type != 'None' and ref_type in type_defs:
                    # Get the parent type (before the first dot)
                    parent_type = parent_name.split('.')[0] if '.' in parent_name else parent_name
                    if parent_type in type_defs and parent_type != ref_type:
                        # Track reverse relationship
                        reverse_refs[ref_type].append(parent_type)

    # Add reverse reference arrays to relationships
    for ref_type, parent_types in reverse_refs.items():
        # Remove duplicates
        parent_types = list(set(parent_types))
        for parent_type in parent_types:
            # Create a synthetic reverse reference array with proper naming
            plural_name = pluralize(parent_type)
            reverse_key = f"{ref_type}.{plural_name}"
            if reverse_key not in relationships[ref_type]:
                relationships[ref_type].append(reverse_key)
                type_info[reverse_key] = f"array[reference→{parent_type}]"
                # Add the parent type as child of the reverse array
                if parent_type not in relationships[reverse_key]:
                    relationships[reverse_key].append(parent_type)


def build_relationships(type_defs: dict) -> tuple:
    """
    Build parent->children relationship map.
    Returns: (relationships dict, type_info dict, schema_types set)
    """
    relationships = defaultdict(list)
    type_info = {}

    for type_name, type_def in type_defs.items():
        properties = type_def.get('properties', {})
        process_properties(type_name, properties, relationships, type_info)

    # Add reverse relationships for better navigation
    add_reverse_relationships(type_defs, relationships, type_info)

    # Return set of schema types for generic detection
    schema_types = set(type_defs.keys())

    return relationships, type_info, schema_types


def find_root_types(type_defs: dict, relationships: dict) -> list:
    """Find types that are not children of any other type."""
    all_types = set(type_defs.keys())
    child_types = set()

    for children in relationships.values():
        # Only count schema types as children (not inline properties)
        child_types.update([c for c in children if c in all_types])

    roots = all_types - child_types
    return sorted(list(roots))


def humanize(name: str) -> str:
    """Convert snake_case to Title Case."""
    # Handle inline objects (type.property.subproperty... format)
    if '.' in name:
        parts = name.split('.')
        humanized_parts = [' '.join(word.capitalize() for word in part.split('_')) for part in parts]
        return '.'.join(humanized_parts)
    return ' '.join(word.capitalize() for word in name.split('_'))


def print_tree(type_name: str, relationships: dict, type_info: dict, prefix: str = "", is_last: bool = True,
               visited: set = None, show_humanized: bool = True, global_shown: set = None):
    """Recursively print ASCII tree with cycle detection and deduplication."""
    if visited is None:
        visited = set()
    if global_shown is None:
        global_shown = set()

    # Determine connector
    connector = "└── " if is_last else "├── "

    # Display name
    display_name = humanize(type_name) if show_humanized else type_name

    # Add type prefix if available
    type_prefix = type_info.get(type_name, "")
    if type_prefix:
        display_name = f"{type_prefix}: {display_name}"

    # Check for cycles in current path
    if type_name in visited:
        print(f"{prefix}{connector}{display_name} [→ see above]")
        return

    # Print current node
    print(f"{prefix}{connector}{display_name}")

    # Mark as visited in current path
    visited.add(type_name)

    # Mark as shown globally
    global_shown.add(type_name)

    # Get children
    children = relationships.get(type_name, [])

    # Filter out children that have already been shown
    children_to_show = [c for c in children if c not in global_shown]

    # Prepare prefix for children
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Print children
    for i, child in enumerate(children_to_show):
        is_last_child = (i == len(children_to_show) - 1)
        print_tree(child, relationships, type_info, child_prefix, is_last_child, visited.copy(),
                   show_humanized, global_shown)


def print_statistics(type_defs: dict, relationships: dict):
    """Print schema statistics."""
    total_types = len(type_defs)
    root_types = len(find_root_types(type_defs, relationships))
    leaf_types = len([t for t in type_defs if not relationships.get(t)])

    print("Schema Statistics:")
    print(f"- Total types: {total_types}")
    print(f"- Root types: {root_types}")
    print(f"- Leaf types: {leaf_types}")
    print()


def main(schema_file: str, show_stats: bool = False, show_humanized: bool = True):
    """Main function to generate tree from schema."""
    # Load schema
    schema = load_schema(schema_file)

    # Extract type definitions
    type_defs = extract_types(schema)

    if not type_defs:
        print("No type definitions found in schema.")
        return

    # Build relationships
    relationships, type_info, schema_types = build_relationships(type_defs)

    # Show statistics if requested
    if show_stats:
        print_statistics(type_defs, relationships)

    # Find root types
    roots = find_root_types(type_defs, relationships)

    if not roots:
        print("No root types found. Showing all types:")
        roots = sorted(type_defs.keys())

    # Generate tree for each root
    for i, root in enumerate(roots):
        print_tree(root, relationships, type_info, "", True, set(), show_humanized)
        if i < len(roots) - 1:
            print()  # Blank line between multiple trees


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yaml_schema_tree.py <schema_file> [--stats] [--no-humanize]")
        sys.exit(1)

    schema_file = sys.argv[1]
    show_stats = "--stats" in sys.argv
    show_humanized = "--no-humanize" not in sys.argv

    main(schema_file, show_stats, show_humanized)
