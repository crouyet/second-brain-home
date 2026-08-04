#!/usr/bin/env python3
"""Whole-repo integrity audit for the second-brain-home template.

Three checks, each catching something a first-time /setup run would hit:
1. Personal-data leaks anywhere in tracked files (same baseline as the
   pre-commit hook in tools/hooks/, but scanning everything, not just a diff).
2. {{PLACEHOLDER}} tokens used in skills/docs that config.example.md never
   defines — a fresh user would have nothing to fill in for them.
3. vault/... file paths referenced in skills/docs that don't exist in the
   shipped template — dangling links a fresh user hits immediately.

Run: python3 tools/check_template_integrity.py
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "hooks"))
from _privacy_patterns import find_hits  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def tracked_text_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True
    ).stdout
    for rel in out.splitlines():
        p = REPO_ROOT / rel
        if p.suffix in {".md", ".py", ".json", ".toml", ".sh"}:
            yield rel, p


def check_personal_leaks(files):
    hits = []
    for rel, p in files:
        for why in find_hits(p.read_text(errors="ignore")):
            hits.append(f"{rel}: {why}")
    return hits


def check_placeholders(files):
    used = set()
    for rel, p in files:
        if rel.startswith(".claude/skills/") or rel.startswith("vault/"):
            used |= set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", p.read_text(errors="ignore")))
    config_example = (REPO_ROOT / "vault/Projects/Sistema/config.example.md").read_text()
    # config.example.md documents fields as bold names (**HABITS_DB_ID:**), not as
    # literal {{...}} — only its intro blockquote uses {{...}} as illustration.
    documented = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", config_example))
    documented |= set(re.findall(r"\*\*([A-Z0-9_]+):\*\*", config_example))
    return sorted(used - documented)


DANGLING_EXEMPT = {
    # generado por /setup a partir de config.example.md — no viene en el template
    "vault/Projects/Sistema/config.md",
}


def check_dangling_links(files):
    hits = []
    pattern = re.compile(r"`?(vault/[A-Za-z0-9_./ áéíóúñÁÉÍÓÚÑ-]+?\.md)`?")
    for rel, p in files:
        text = p.read_text(errors="ignore")
        for m in pattern.findall(text):
            if m in DANGLING_EXEMPT:
                continue
            if not (REPO_ROOT / m).exists():
                hits.append(f"{rel}: referencia rota -> {m}")
    return hits


def main():
    files = list(tracked_text_files())
    leaks = check_personal_leaks(files)
    undocumented = check_placeholders(files)
    dangling = check_dangling_links(files)

    ok = True
    if leaks:
        ok = False
        print("Datos personales sin generalizar:")
        for h in leaks:
            print(f"  - {h}")
    if undocumented:
        ok = False
        print("Placeholders usados pero no documentados en config.example.md:")
        for u in undocumented:
            print(f"  - {{{{{u}}}}}")
    if dangling:
        ok = False
        print("Referencias a archivos del vault que no existen en el template:")
        for d in dangling:
            print(f"  - {d}")

    print("OK — sin leaks, placeholders documentados, sin referencias rotas." if ok else "")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
