#!/usr/bin/env python3
"""Generate tokens.css (CSS custom properties) from tokens.json (Tokens Studio format).

Usage:
    python design/tokens/build_css.py

The JSON file is the single source of truth, shared with Figma (Tokens Studio plugin).
This script resolves {references}, converts numeric types to px, and flattens
token paths to CSS variable names (dots -> dashes, set name dropped).
"""

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "tokens.json"
OUT = HERE / "tokens.css"

PX_TYPES = {"fontSizes", "spacing", "borderRadius", "sizing"}
REF_RE = re.compile(r"\{([^}]+)\}")


def flatten(node: dict, path: tuple = ()) -> dict:
    """Flatten a token set into {path_tuple: {value, type}}."""
    tokens = {}
    for key, val in node.items():
        if isinstance(val, dict) and "value" in val and "type" in val:
            tokens[path + (key,)] = val
        elif isinstance(val, dict):
            tokens.update(flatten(val, path + (key,)))
    return tokens


def load_tokens() -> dict:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    sets = data.get("$metadata", {}).get("tokenSetOrder", [])
    merged = {}
    for set_name in sets:
        # Set name is dropped: references in Tokens Studio are set-agnostic.
        merged.update(flatten(data[set_name]))
    return merged


def resolve(tokens: dict, path: tuple, seen: frozenset = frozenset()):
    """Resolve {references} recursively; returns (value, type)."""
    if path in seen:
        raise ValueError(f"Circular reference: {'.'.join(path)}")
    token = tokens.get(path)
    if token is None:
        raise KeyError(f"Unknown token reference: {'.'.join(path)}")
    value, ttype = token["value"], token["type"]
    if isinstance(value, str):
        match = REF_RE.fullmatch(value.strip())
        if match:
            ref_path = tuple(match.group(1).split("."))
            ref_value, ref_type = resolve(tokens, ref_path, seen | {path})
            # Keep the referencing token's type for px conversion semantics.
            return ref_value, ttype or ref_type
    return value, ttype


def shadow_to_css(value) -> str:
    layers = value if isinstance(value, list) else [value]
    return ", ".join(
        f"{l['x']}px {l['y']}px {l['blur']}px {l['spread']}px {l['color']}"
        for l in layers
    )


def to_css_value(value, ttype: str) -> str:
    if ttype == "boxShadow":
        return shadow_to_css(value)
    if ttype in PX_TYPES:
        return f"{value}px"
    return str(value)


def main() -> None:
    tokens = load_tokens()
    lines = [
        "/* AUTO-GENERATED from tokens.json — do not edit by hand.",
        " * Regenerate with: python design/tokens/build_css.py */",
        "",
        ":root {",
    ]
    for path in tokens:
        value, ttype = resolve(tokens, path)
        var_name = "--" + "-".join(path)
        lines.append(f"  {var_name}: {to_css_value(value, ttype)};")
    lines += ["}", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK — {len(tokens)} tokens -> {OUT.name}")


if __name__ == "__main__":
    main()
