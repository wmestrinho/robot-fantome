#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(path, label):
    if not path.exists():
        errors.append(f"Missing {label}: {path.relative_to(ROOT)}")

require(ROOT / "README.md", "README")
if not (ROOT / "AGENTS.md").exists() and not (ROOT / "CLAUDE.md").exists():
    errors.append("Missing AI-agent instructions: AGENTS.md or CLAUDE.md")
require(ROOT / "VERSION", "VERSION")

if (ROOT / "VERSION").exists():
    version = (ROOT / "VERSION").read_text(errors="replace").strip().splitlines()[0].strip()
    if not re.fullmatch(r"v\d+\.\d+\.\d+(?: (?:alpha|beta|rc))?", version):
        errors.append(f"VERSION has invalid format: {version!r}")

readme = ROOT / "README.md"
if readme.exists():
    txt = readme.read_text(errors="replace")
    for phrase in ["Deployment", "Version", "Validation"]:
        if phrase.lower() not in txt.lower():
            errors.append(f"README.md missing {phrase} notes")

if errors:
    print("AGENT BASELINE VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("AGENT BASELINE VALIDATION OK")
