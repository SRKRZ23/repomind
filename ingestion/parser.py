"""Tree-sitter-aware parsing with graceful fallback.

If `tree-sitter-languages` isn't installed we degrade to a regex-based
top-level-symbol extractor — good enough for unit tests and for
languages we don't yet have grammars for.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


# Map filesystem extensions to tree-sitter grammar names.
LANG_BY_EXT = {
    ".py": "python", ".pyi": "python",
    ".rs": "rust",
    ".go": "go",
    ".js": "javascript", ".jsx": "javascript",
    ".ts": "typescript", ".tsx": "tsx",
    ".c": "c", ".h": "c",
    ".cc": "cpp", ".cpp": "cpp", ".cxx": "cpp", ".hpp": "cpp",
    ".java": "java",
    ".rb": "ruby",
    ".php": "php",
    ".cs": "c_sharp",
    ".swift": "swift",
    ".kt": "kotlin", ".kts": "kotlin",
    ".sh": "bash", ".bash": "bash",
    ".sql": "sql",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml", ".yml": "yaml",
    ".toml": "toml",
    ".md": "markdown", ".markdown": "markdown",
}


@dataclass
class Symbol:
    name: str
    kind: str          # function / class / method / module / heading
    start_line: int
    end_line: int


def detect_language(path: str | Path) -> Optional[str]:
    suffix = Path(path).suffix.lower()
    return LANG_BY_EXT.get(suffix)


def extract_symbols(text: str, language: Optional[str]) -> List[Symbol]:
    """Top-level structural symbols. Tree-sitter when available; regex fallback."""
    if not text.strip():
        return []
    try:
        return _ts_symbols(text, language)
    except Exception:
        return _regex_symbols(text, language)


# ---- tree-sitter path -----------------------------------------------------

def _ts_symbols(text: str, language: Optional[str]) -> List[Symbol]:
    if not language:
        raise RuntimeError("no language")
    try:
        from tree_sitter_languages import get_parser  # type: ignore
    except ImportError as e:
        raise RuntimeError("tree_sitter_languages not installed") from e

    parser = get_parser(language)
    tree = parser.parse(text.encode("utf-8"))
    out: List[Symbol] = []

    interesting = {
        "function_definition", "function_declaration", "method_definition",
        "class_definition", "class_declaration", "struct_item", "trait_item",
        "impl_item", "enum_item", "type_alias_declaration",
        "atx_heading", "setext_heading",
    }

    def walk(node):
        if node.type in interesting:
            name = _node_name(node, text) or node.type
            kind = _kind_for(node.type)
            out.append(Symbol(
                name=name, kind=kind,
                start_line=node.start_point[0] + 1,
                end_line=node.end_point[0] + 1,
            ))
        for c in node.children:
            walk(c)

    walk(tree.root_node)
    return out


def _node_name(node, text: str) -> Optional[str]:
    for c in node.children:
        if c.type == "identifier" or c.type == "type_identifier":
            return text[c.start_byte:c.end_byte]
        for cc in c.children:
            if cc.type in ("identifier", "type_identifier"):
                return text[cc.start_byte:cc.end_byte]
    if node.type in ("atx_heading", "setext_heading"):
        return text[node.start_byte:node.end_byte].strip().lstrip("#").strip()
    return None


def _kind_for(node_type: str) -> str:
    if "class" in node_type or "struct" in node_type or "trait" in node_type or "impl" in node_type:
        return "class"
    if "method" in node_type:
        return "method"
    if "function" in node_type:
        return "function"
    if "heading" in node_type:
        return "heading"
    return "symbol"


# ---- regex fallback -------------------------------------------------------

PY_DEF = re.compile(r"^(?P<indent>\s*)(?:async\s+)?def\s+(?P<name>[A-Za-z_][\w]*)\s*\(", re.MULTILINE)
PY_CLASS = re.compile(r"^(?P<indent>\s*)class\s+(?P<name>[A-Za-z_][\w]*)", re.MULTILINE)
RS_FN = re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?fn\s+(?P<name>[A-Za-z_][\w]*)", re.MULTILINE)
GO_FN = re.compile(r"^\s*func\s+(?:\([^)]*\)\s+)?(?P<name>[A-Za-z_][\w]*)", re.MULTILINE)
JS_FN = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+(?P<name>[A-Za-z_$][\w$]*)", re.MULTILINE)
MD_HEADING = re.compile(r"^(#{1,6})\s+(?P<name>.+)$", re.MULTILINE)


def _regex_symbols(text: str, language: Optional[str]) -> List[Symbol]:
    lines = text.split("\n")
    out: List[Symbol] = []

    def add(name: str, kind: str, m: re.Match):
        line = text[:m.start()].count("\n") + 1
        out.append(Symbol(name=name, kind=kind, start_line=line, end_line=line))

    if language == "python":
        for m in PY_CLASS.finditer(text):
            add(m.group("name"), "class", m)
        for m in PY_DEF.finditer(text):
            indent = m.group("indent")
            kind = "method" if indent else "function"
            add(m.group("name"), kind, m)
    elif language == "rust":
        for m in RS_FN.finditer(text):
            add(m.group("name"), "function", m)
    elif language == "go":
        for m in GO_FN.finditer(text):
            add(m.group("name"), "function", m)
    elif language in ("javascript", "typescript", "tsx"):
        for m in JS_FN.finditer(text):
            add(m.group("name"), "function", m)
    elif language == "markdown":
        for m in MD_HEADING.finditer(text):
            add(m.group("name").strip(), "heading", m)
    return out
