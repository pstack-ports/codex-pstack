# Upstream sources

Imported unchanged before the Codex port:

- `pstack/` from [`cursor/plugins` at `2f87c854fe3e2fcda44ca86b46ede35aad3c46b7`](https://github.com/cursor/plugins/tree/2f87c854fe3e2fcda44ca86b46ede35aad3c46b7/pstack), version `0.15.43`, by Lauren Tan.
- `deslop`, `control-cli`, and `control-ui` skills from cursor/plugins at the same commit, by Eric Zakariasson, following the [agy-pstack example](https://github.com/pstack-ports/agy-pstack).

The first Git commit is the imported source snapshot. The Codex port follows in a separate commit for review. The original MIT license and assets are retained.

The port moves skills to `.agents/skills/`, replaces the manifests with `.codex-plugin/plugin.json`, converts explicit-only skill metadata to `agents/openai.yaml`, and adds one shared host adapter. Most workflow bodies and all core orchestration, PR-watching, and statechart logic remain upstream. Setup, webhook UI instructions, and transcript discovery are adapted where their original APIs do not exist in Codex.

Future upstream syncs must skip the Benny automation pack (`pstack/automations/benny/`).

`.agents/skills/poteto-mode/scripts/worktree-audit.sh` carries a patch over the pin. The patch reads worktree paths with `git worktree list --porcelain -z` and passes each full path to git. The pinned script splits those paths on whitespace. Keep the patch until cursor/plugins ships its own fix for that split. On that sync, take upstream's script verbatim and remove the patch and this note.

The script reads Codex transcripts from `PSTACK_TRANSCRIPTS_DIR` instead of `~/.cursor/projects/<slug>/agent-transcripts`.

This repository targets Codex only. It does not register Cursor or Claude Code compatibility layouts. External Slack/tracker integrations, event runners, and repository-specific verification tools remain prerequisites for the workflows that use them.
