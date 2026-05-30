"""Validate local references used by the GitHub Pages docs homepage."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "docs"
INDEX = SITE_ROOT / "index.html"


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.references.append(value)


def is_local_reference(reference: str) -> bool:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc:
        return False
    if reference.startswith("#") or reference.startswith("mailto:"):
        return False
    return True


def main() -> int:
    parser = ReferenceParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    missing: list[str] = []
    for reference in parser.references:
        if not is_local_reference(reference):
            continue
        relative_path = reference.split("#", 1)[0].split("?", 1)[0]
        if not relative_path:
            continue
        local_path = SITE_ROOT / relative_path
        generated_markdown_source = local_path.with_suffix(".md") if local_path.suffix == ".html" else None
        if not local_path.exists() and not (generated_markdown_source and generated_markdown_source.exists()):
            missing.append(reference)

    if missing:
        for reference in missing:
            print(f"ERROR missing docs site reference: {reference}")
        return 1

    print("OK: docs site references exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
