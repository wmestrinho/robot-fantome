# AGENTS.md — robot-fantome

Canonical path
- `/Users/wmestrinho/Workspace/Projects/robot-fantome`

Legacy path
- `/Users/wmestrinho/.openclaw/workspace/projects/robot-fantome`
- Treat the legacy path as deprecated after migration. Do not start new work there unless Luiz explicitly says the migration is paused or reversed.

Project purpose
- See `README.md` for project-specific purpose and usage.

Required baseline for AI agents
- Read this file before editing.
- Check `git status --short --branch` before editing, committing, rebasing, or pushing.
- Preserve project-specific instructions in `CLAUDE.md` if present.
- Keep deployment notes current in `README.md`.
- Keep a visible version rule for web UIs.
- Run validation before commit.

Version rule
- Single source of truth: `VERSION` unless this repo already documents another version source in `README.md` or `CLAUDE.md`.
- Current baseline version: `v3.4.1 beta`
- Web UIs must visibly display the version.
- Bump version for behavior/UI changes.

Deployment
- Cloudflare Workers/Pages via Wrangler. Config: `wrangler.jsonc` or `wrangler.toml`.

Validation
- Run: `python3 scripts/validate_agent_baseline.py`
- Also run any project-specific test/build/validation commands documented in `README.md`, `CLAUDE.md`, package scripts, or CI workflows.

Coordination warning
- Multiple AI agents may be working across this workspace. Do not run destructive git commands, delete files, rebase, or force-push without checking status and coordinating with Luiz.
