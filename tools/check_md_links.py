#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check relative .md links under docs/ and thin knowledge-page policy."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WHITELIST_FILE = Path(__file__).resolve().parent / "thin_knowledge_whitelist.txt"
THIN_BYTES = 2500

# [text](./foo.md) or [text](foo.md) or [text](./foo.md#anchor)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def is_internal_md(href: str) -> bool:
    href = href.strip()
    if not href or href.startswith(("#", "http://", "https://", "mailto:")):
        return False
    path = href.split("#", 1)[0].strip()
    if not path or path.startswith("//"):
        return False
    return path.endswith(".md")


def load_whitelist() -> set[str]:
    if not WHITELIST_FILE.is_file():
        return set()
    names: set[str] = set()
    for line in WHITELIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.add(line)
    return names


def has_thin_banner(text: str) -> bool:
    head = text[:2000]
    return ("本文是精简页" in head) or ("本文是入口页" in head)


def main() -> int:
    missing: list[str] = []
    thin_warnings: list[str] = []
    thin_policy_fail: list[str] = []
    checked = 0
    whitelist = load_whitelist()

    for md in sorted(DOCS.rglob("*.md")):
        if "archive" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        rel = md.relative_to(ROOT)

        for m in LINK_RE.finditer(text):
            href = m.group(1).strip().strip("<>")
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
        if "高频面试题与知识点" not in name:
            continue
        if size >= THIN_BYTES:
            continue

        # thin knowledge page
        thin_warnings.append(f"{rel} ({size} bytes)")
        if name not in whitelist:
            thin_policy_fail.append(
                f"{rel}: 薄知识点未在 tools/thin_knowledge_whitelist.txt 登记（{size} bytes）"
            )
        if not has_thin_banner(text):
            thin_policy_fail.append(
                f"{rel}: 薄知识点缺少「本文是精简页/入口页」横幅"
            )

    print(f"checked_links={checked}")
    print(f"missing={len(missing)}")
    for line in missing:
        print("MISSING", line)
    print(f"thin_knowledge_pages={len(thin_warnings)}")
    for line in thin_warnings[:40]:
        print("THIN", line)
    print(f"thin_policy_fail={len(thin_policy_fail)}")
    for line in thin_policy_fail:
        print("THIN_POLICY", line)
    print(f"whitelist_size={len(whitelist)}")

    if missing or thin_policy_fail:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
