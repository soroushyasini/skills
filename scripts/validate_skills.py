"""Validate skill packages and local Markdown file links without network access."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def prose(text: str) -> str:
    """Exclude fenced examples so sample paths are not treated as dependencies."""
    lines = []
    active = None
    for line in text.splitlines():
        fence = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            marker, suffix = fence.groups()
            if active is None:
                active = marker
            elif marker[0] == active[0] and len(marker) >= len(active) and not suffix.strip():
                active = None
            continue
        if active is None:
            lines.append(line)
    return "\n".join(lines)


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    skills = root / "skills"
    if not skills.is_dir():
        return ["Missing skills/ directory"]
    folders = sorted(path for path in skills.iterdir() if path.is_dir() and not path.name.startswith("."))
    if not folders:
        errors.append("No skill packages found in skills/")
    for folder in folders:
        entry = folder / "SKILL.md"
        label = folder.relative_to(root).as_posix()
        if not entry.is_file():
            errors.append(f"{label}: missing SKILL.md")
            continue
        match = FRONTMATTER.match(entry.read_text(encoding="utf-8"))
        if not match:
            errors.append(f"{label}: missing or malformed YAML frontmatter")
            continue
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            errors.append(f"{label}: invalid YAML: {error}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{label}: frontmatter must be a mapping")
            continue
        name = data.get("name")
        if not isinstance(name, str) or len(name) > 64 or not NAME.fullmatch(name):
            errors.append(f"{label}: name must use lowercase letters, digits and hyphens, up to 64 characters")
        elif name != folder.name:
            errors.append(f"{label}: name {name!r} must match the folder name")
        description = data.get("description")
        if not isinstance(description, str) or not description.strip() or len(description) > 1024:
            errors.append(f"{label}: description must be non-empty text, up to 1024 characters")
        if "metadata" in data and not isinstance(data["metadata"], dict):
            errors.append(f"{label}: metadata must be a mapping")
        for key in ("version", "language"):
            if key in data:
                errors.append(f"{label}: place {key} under metadata")
    for markdown in sorted(root.rglob("*.md")):
        relative = markdown.relative_to(root)
        if any(part.startswith(".") or part in {"__pycache__", "node_modules"} for part in relative.parts):
            continue
        for target in LINK.findall(prose(markdown.read_text(encoding="utf-8"))):
            url = urlsplit(target.strip().removeprefix("<").removesuffix(">"))
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            destination = (root / path.lstrip("/")) if path.startswith("/") else (markdown.parent / path)
            destination = destination.resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f"{relative.as_posix()}: missing or external local target {target!r}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    count = sum(1 for _ in (root / "skills").glob("*/SKILL.md"))
    print(f"Validated {count} skill packages and local Markdown file links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
