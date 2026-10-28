# Upstream sources

Imported unchanged before the Codex port:

- `pstack/` from [`cursor/plugins` at `c742dd61706fbacc1b95f1a20b7b988cf096ce6c`](https://github.com/cursor/plugins/tree/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack), version `0.15.36`, by Lauren Tan.
- `deslop`, `control-cli`, and `control-ui` skills from cursor/plugins at the same commit, by Eric Zakariasson, following the [agy-pstack example](https://github.com/pstack-ports/agy-pstack).

The first Git commit is the imported source snapshot. The Codex port follows in a separate commit for review. The original MIT license and assets are retained.

The port moves skills to `.agents/skills/`, replaces the manifests with `.codex-plugin/plugin.json`, converts explicit-only skill metadata to `agents/openai.yaml`, and adds one shared host adapter. Most workflow bodies and all core orchestration, PR-watching, plan-checking, and statechart logic remain upstream. Setup, webhook UI instructions, transcript discovery, and Benny's host integration are adapted where their original APIs do not exist in Codex.

This repository targets Codex only. It does not register Cursor or Claude Code compatibility layouts. External Slack/tracker integrations, event runners, and repository-specific verification tools remain prerequisites for the workflows that use them.
