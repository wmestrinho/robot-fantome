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
- Current version: read it from `VERSION` — do not trust hardcoded version strings in docs.
- Web UIs must visibly display the version (site footer).
- Bump version for behavior/UI changes.

Deployment
- GitHub Pages from `main` (root path, no build step). `CNAME` sets the custom domain; Cloudflare provides DNS/CDN in front.
- The old Cloudflare Workers/Wrangler deploy path is retired; `wrangler.jsonc` was removed 2026-06-11. Do not reintroduce it without updating `README.md` and `CLAUDE.md`.

Validation
- Run: `python3 scripts/validate_agent_baseline.py`
- Also run any project-specific test/build/validation commands documented in `README.md`, `CLAUDE.md`, package scripts, or CI workflows.

Coordination warning
- Multiple AI agents may be working across this workspace. Do not run destructive git commands, delete files, rebase, or force-push without checking status and coordinating with Luiz.
