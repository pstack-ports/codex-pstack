# Codex worktree audit

The [pinned upstream script](https://github.com/cursor/plugins/blob/2f87c854fe3e2fcda44ca86b46ede35aad3c46b7/pstack/skills/poteto-mode/scripts/worktree-audit.sh) splits Git’s worktree paths on whitespace. A path such as `feature branch` can be truncated to `feature`, causing the audit to inspect the wrong directory and report uncommitted work as clean.

The [Codex script](.agents/skills/poteto-mode/scripts/worktree-audit.sh) reads NUL-delimited paths from Git. If Git cannot report a worktree’s status, the audit marks it `unknown` and sends it to `review`.

Upstream looks for chat history in Cursor’s project directory. For Codex, set `PSTACK_TRANSCRIPTS_DIR` to a directory of transcripts already scoped to the repository. When it is unset, the audit omits chat recency.
