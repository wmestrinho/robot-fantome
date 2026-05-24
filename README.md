# robot fantôme — robotfantome.com

Clean rebuild of [robotfantome.com](https://robotfantome.com) in plain HTML/CSS/JS.
No Canva. No build tools. No dependencies. Just our code.

**Live:** [robotfantome.com](https://robotfantome.com)

Auto-deploys via **Cloudflare Pages** on every push to `main`.
No build step — the repo root is served directly.

To preview locally:

```sh
python3 -m http.server 8080
```

---

*absolutely plausible by robot fantôme*

---

## AI Agent Handoff

Canonical local path:
- `/Users/wmestrinho/Workspace/Projects/robot-fantome`

Legacy local path:
- `/Users/wmestrinho/.openclaw/workspace/projects/robot-fantome`

Before editing:
- Read `AGENTS.md`.
- Check `git status --short --branch`.
- Preserve any project-specific instructions in `CLAUDE.md`.

Deployment notes:
- Cloudflare Workers/Pages via Wrangler. Config: `wrangler.jsonc` or `wrangler.toml`.

Version rule:
- Current baseline version: `v3.4.1 beta`
- Keep version source documented.
- Web UIs must visibly display the version.

Validation:
- Run `python3 scripts/validate_agent_baseline.py`.
- Also run project-specific tests/builds when present.

