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

Pit Board — owner decisions (read at session start)
- Every question only Luiz can answer lives on the workspace-wide **AP Ops Pit
  Board** (ops.absolutelyplausible.com → Pit Board). Read this repo's items
  before planning work:
  `node ../ap-ops/scripts/pitboard.mjs read --answered --repo robot-fantome`
  (Seat 1 reads D1 directly; Seats 2–3 use the seat's Access service token —
  `ap-ops/docs/SATELLITE-OFFICE.md` § Board access).
- Act only on what he chose. Close what you finish, in the same commit as the
  work: `node ../ap-ops/scripts/pitboard.mjs close <key> "<what actually happened>"`.
- File new questions there (`pitboard.mjs file <item.json>`, `"repo": "robot-fantome"`),
  never in chat. Never invent an answer he has not given.
- Rules: `ap-ops/docs/PITBOARD.md`.

Version rule
- Versioning, CHANGELOG, LICENSE, and CI conventions: [`ap-ops/docs/PROJECT-RULES.md`](https://github.com/wmestrinho/ap-ops/blob/main/docs/PROJECT-RULES.md) — canonical for every AP repo.

Deployment
- GitHub Pages from `main` (root path, no build step). `CNAME` sets the custom domain; Cloudflare provides DNS/CDN in front.
- The old Cloudflare Workers/Wrangler deploy path is retired; `wrangler.jsonc` was removed 2026-06-11. Do not reintroduce it without updating `README.md` and `CLAUDE.md`.

Validation
- Run: `python3 scripts/validate_agent_baseline.py`
- Also run any project-specific test/build/validation commands documented in `README.md`, `CLAUDE.md`, package scripts, or CI workflows.

Coordination warning
- Multiple AI agents may be working across this workspace. Do not run destructive git commands, delete files, rebase, or force-push without checking status and coordinating with Luiz.
