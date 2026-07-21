#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check relative .md links under docs/ and optional thin '完整卷' warnings."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# [text](./foo.md) or [text](foo.md) or [text](./foo.md#anchor)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FULL_VOL_MARKERS = ("完整卷",)


def is_internal_md(href: str) -> bool:
    href = href.strip()
    if not href or href.startswith(("#", "http://", "https://", "mailto:")):
        return False
    path = href.split("#", 1)[0].strip()
    if not path or path.startswith("//"):
        return False
    return path.endswith(".md")


def main() -> int:
    missing: list[str] = []
    checked = 0
    thin_warnings: list[str] = []

    for md in sorted(DOCS.rglob("*.md")):
        # archive is historical; dead links there do not fail the site
        if "archive" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        rel = md.relative_to(ROOT)

        for m in LINK_RE.finditer(text):
            href = m.group(1).strip().strip("<>")
            # strip optional title 'path' "title"
            if " " in href:
                href = href.split(" ", 1)[0]
            if not is_internal_md(href):
                continue
            target_name = href.split("#", 1)[0]
            target = (md.parent / target_name).resolve()
            checked += 1
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                missing.append(f"{rel}: outside root -> {href}")
                continue
            if not target.is_file():
                missing.append(f"{rel}: missing -> {href}")

        size = md.stat().st_size
        name = md.name
        if "高频面试题与知识点" in name and size < 2500:
            thin_warnings.append(f"{rel} ({size} bytes) 体量偏薄，请确认是否应标精简")

    print(f"checked_links={checked}")
    print(f"missing={len(missing)}")
    for line in missing:
        print("MISSING", line)
    print(f"thin_knowledge_pages={len(thin_warnings)}")
    for line in thin_warnings[:40]:
        print("THIN", line)
    if len(thin_warnings) > 40:
        print(f"THIN ... and {len(thin_warnings) - 40} more")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
