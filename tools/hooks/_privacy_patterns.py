"""Shared denylist for the privacy guards in tools/hooks/ and tools/check_template_integrity.py.

No personal name is hardcoded here on purpose — this repo is a public template used
by more than one person, so any name lives outside it, in ~/.hestia/private-denylist.txt
(one literal string per line, # for comments; gitignored, outside the repo entirely).
The only pattern baked in here is the Notion UUID shape, which isn't personally
identifying by itself — it just means "an unresolved placeholder".
"""
import re
from pathlib import Path

UUID_PATTERN = (
    r"collection://[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    "ID real de Notion (no placeholder)",
)

DENYLIST_FILE = Path.home() / ".hestia" / "private-denylist.txt"


def load_extra_terms():
    if not DENYLIST_FILE.exists():
        return []
    terms = []
    for line in DENYLIST_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def find_hits(text):
    hits = []
    pattern, why = UUID_PATTERN
    if re.search(pattern, text):
        hits.append(why)
    for term in load_extra_terms():
        # Palabra completa, no substring: un nombre corto de pila aparecería
        # dentro de otra palabra, y un guard que grita en falso se termina ignorando.
        if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, re.IGNORECASE):
            hits.append(f"término personal en denylist: '{term}'")
    return hits
