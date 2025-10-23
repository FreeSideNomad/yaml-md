import re
import sys
import unittest
from pathlib import Path
from typing import Dict, Iterator, List, Set, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = ROOT / "samples"
OUTPUT_DIR = ROOT / "output"
INDEX_FILE = SAMPLES_DIR / "INDEX.md"
SCRIPTS_DIR = ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def iter_schema_model_pairs() -> Iterator[Tuple[Path, Path]]:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Missing samples index: {INDEX_FILE}")

    with INDEX_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            cells = [col.strip().strip("`") for col in stripped.strip("|").split("|")]
            if not cells or cells[0] in {"Schema", "---"}:
                continue
            schema_rel, model_rel = cells[:2]
            if schema_rel and model_rel:
                yield SAMPLES_DIR / schema_rel, SAMPLES_DIR / model_rel


def schema_types_with_id(schema_path: Path) -> Set[str]:
    schema = yaml.safe_load(schema_path.read_text())
    defs = schema.get("$defs", {})
    types = set()
    for type_name, definition in defs.items():
        if isinstance(definition, dict):
            properties = definition.get("properties", {})
            if "id" in properties:
                types.add(type_name)
    return types


def collect_ids_from_model(model_path: Path, typed_types: Set[str]) -> Dict[str, Set[str]]:
    documents = list(yaml.safe_load_all(model_path.read_text()))
    ids_by_type: Dict[str, Set[str]] = {}

    def record_ids(obj):
        if isinstance(obj, dict):
            if "id" in obj:
                value = str(obj["id"])
                ids_by_type.setdefault(current_type, set()).add(value)
            for value in obj.values():
                record_ids(value)
        elif isinstance(obj, list):
            for item in obj:
                record_ids(item)

    for doc in documents:
        if not isinstance(doc, dict):
            continue
        for key, value in doc.items():
            detected_type = infer_type_from_key(key, typed_types)
            if detected_type is None and isinstance(value, dict):
                detected_type = infer_type_from_key(value.get("type"), typed_types)
            if detected_type is None:
                continue
            current_type = detected_type
            if isinstance(value, list):
                for item in value:
                    record_ids(item)
            else:
                record_ids(value)

    return ids_by_type


def infer_type_from_key(key: str, typed_types: Set[str]) -> str:
    if not key:
        return None
    normalized = key.lower().replace("-", "_").rstrip("s")
    for schema_type in typed_types:
        if normalized == schema_type.lower():
            return schema_type
    return None


def load_output_text(output_path: Path) -> str:
    if not output_path.exists():
        return ""
    return output_path.read_text(encoding="utf-8", errors="ignore").lower()


class SampleGenerationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import importlib

        cls.visitor_module = importlib.import_module("yaml_visitor")

    def test_samples_cover_ids(self):
        pairs = list(iter_schema_model_pairs())
        self.assertGreater(len(pairs), 0, "No schema/model pairs discovered in samples/INDEX.md")

        for schema_path, model_path in pairs:
            with self.subTest(schema=schema_path, model=model_path):
                self.assertTrue(schema_path.exists(), f"Schema not found: {schema_path}")
                self.assertTrue(model_path.exists(), f"Model not found: {model_path}")

                typed_types = schema_types_with_id(schema_path)
                ids_by_type = collect_ids_from_model(model_path, typed_types)

                output_subdir = schema_path.parent.relative_to(SAMPLES_DIR)
                output_dir = OUTPUT_DIR / output_subdir
                output_dir.mkdir(parents=True, exist_ok=True)

                outputs = {}
                for ext in ("html", "md"):
                    output_file = output_dir / f"{model_path.stem}.{ext}"
                    self.visitor_module.main(str(schema_path), str(model_path), str(output_file))
                    self.assertTrue(output_file.exists(), f"Expected output file missing: {output_file}")
                    self.assertGreater(output_file.stat().st_size, 0, f"Generated file empty: {output_file}")
                    outputs[ext] = load_output_text(output_file)

                for schema_type, ids in ids_by_type.items():
                    for identifier in ids:
                        needle = identifier.lower()
                        html_present = needle in outputs["html"]
                        md_present = needle in outputs["md"]
                        if not html_present or not md_present:
                            self.fail(
                                f"Missing id '{identifier}' for type '{schema_type}' in outputs "
                                f"(HTML present: {html_present}, Markdown present: {md_present}) "
                                f"for schema {schema_path} and model {model_path}"
                            )


if __name__ == "__main__":
    unittest.main()
