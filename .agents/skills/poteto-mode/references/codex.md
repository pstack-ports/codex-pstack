# Codex adapter

Read this once per session before following any pstack workflow. Apply these mappings wherever the preserved upstream text uses Cursor tool names or defaults. Include this file's absolute path in every delegate's brief. Host instructions, tool schemas, permissions, and the user's authorization always take precedence over a workflow.

## Skills and paths

The plugin root contains `.codex-plugin/plugin.json`, `.agents/skills/`, `agents/`, and `docs/`. Resolve sibling skills at `../../<name>/SKILL.md` from this file's directory, or `../<name>/SKILL.md` from a skill directory. Prefer the path in the session's skill catalog. Read a referenced skill and follow it; do not assume a separate skill-invocation tool exists. This package is discovered as `pstack:<name>`: user prompts use `$pstack:poteto-mode`, `$pstack:setup-pstack`, and `$pstack:<name>` in place of upstream `/name` examples. If skills are copied without a package manifest, use the unprefixed names actually shown in the catalog. Match skills by their leaf name when resolving a namespaced catalog entry.

Create project skills only at `.agents/skills/<name>/SKILL.md` and personal skills only at `~/.agents/skills/<name>/SKILL.md`. Keep one skill per immediate child directory; do not introduce personal category nesting. Explicit-only skills use `policy.allow_implicit_invocation: false` in their `agents/openai.yaml`. Use `skill-creator` when available; otherwise write valid YAML `name` and `description` frontmatter and follow the installed Codex skill guidance. The bundled `deslop`, `control-cli`, and `control-ui` replace the upstream cursor-team-kit dependency.

Read bundled guides locally. An upstream URL ending in `pstack/skills/<path>` refers to `<plugin-root>/.agents/skills/<path>`; other bundled upstream paths resolve from the plugin root. Do not fetch a file already shipped locally. The role files in `agents/` are prompt briefs, not registered Codex agent types.

Apply the same mapping to shell commands and generated plans. Replace `pstack/skills/<path>` with the installed absolute path. A `git show <ref>:pstack/skills/<path>` instruction, or a request to re-read a bundled playbook from trunk, means read the installed plugin file; it does not mean that pstack exists in the target repository's Git tree. Record the plugin root and manifest version at program start, reuse those resources for the run, and give delegates absolute paths. Invoke bundled `scripts/<path>` through the owning skill's absolute directory while keeping the working directory in the target repository or worktree. Read the target repository's own files from its resolved base ref when the playbook requires trunk evidence.

## Durable state and recovery

Where upstream says the agent's store, use `${CODEX_HOME:-~/.codex}/pstack/<workspace-key>/`. Derive a stable workspace key from the primary Git worktree's directory name plus the first 12 hex characters of the SHA-256 of its canonical absolute path encoded as UTF-8, so linked worktrees share state and unrelated repositories do not collide. Outside Git, use the canonical workspace path. Record the resolved absolute directory in the plan and every delegate brief. Plans go under its `docs/`; orchestration uses `orchestrate/<project-slug>/`. Pass that orchestration directory as `--store <absolute-path>` or `ORCH_STORE` on every `orch` call. Keep this state outside the plugin cache and the target repository.

Replace Cursor dashboard checks with the native read-only agent status/list operation when available, plus the ledger, worktrees, and forge evidence. Never resume an idle worker just to probe it. A local worktree persists files, not a running worker. After a host restart, inspect saved agent IDs through the supported host tools; reattach only when the host confirms the worker still exists. Otherwise recover the saved brief, branch, head SHA, and receipts and spawn a replacement. Do not assume cloud workers survived or promise unattended execution without a documented runner. Respect the session's concurrency and nesting limits instead of upstream fleet sizes.

## Tools and delegation

Use only tools and arguments actually exposed in the session. The names below describe the operation; choose the matching native tool, including namespaced variants.

| Upstream instruction | Codex operation |
| --- | --- |
| `Task` | Spawn a subagent with `spawn_agent` or `collaboration.spawn_agent`. Supply the task in `message` and a name when required. |
| `subagent_type`, `TypeName`, `generalPurpose`, `poteto-agent`, `comment-sicko` | Choose an available general agent and put the requested role in its brief. For the two pstack roles, require it to read `<plugin-root>/agents/<role>.md` first. Never pass an unregistered agent type. |
| `readonly: true` | Tell the worker to inspect only and never edit. Use a supported read-only agent if available; otherwise review workspace status afterward. This is a brief constraint, not an invented sandbox field. |
| `run_in_background: true` | Native spawns already return while the agent works. |
| `resume`, messages, follow-up | Use the session's send/resume/follow-up operation with the returned agent ID. Preserve the upstream preference for a fresh worker unless state is costly to transfer. |
| `environment: "cloud"`, `cloud_base_branch` | Create an isolated Git worktree at the named branch/commit and give its absolute path to the worker. Assign separate app ports and runtime state when needed; worktrees share the host machine. Native agents otherwise share the workspace. Do not claim remote isolation. |
| `file_attachments` | Put the absolute file paths in the brief. |
| Wait for workers | Use the native agent wait operation, then collect actual reports and inspect diffs. Respect the exposed concurrency limit and release finished workers when supported. |
| `AskQuestion` | Use the available user-input tool in a mode that supports it. Otherwise ask one concise question in text; required approval must receive a real answer. |
| Open/update a todo list | Use the available plan tool, or keep a concise checklist in the conversation if none exists. |
| `Read`, `Grep`, `Glob`, `Shell` | Use file tools or `exec_command` with `rg`, `rg --files`, and a bounded file read. |
| Built-in PR tool | Use the available forge integration or `gh` commands given by the playbook. |

Never silently manufacture an independent review. When subagents are unavailable or disallowed, say which independent check cannot run and perform the useful serial work. A skill does not authorize external messages, deployments, or other gated actions beyond the user's request.

## Models and reasoning

At task start read `.agents/pstack-models.md` in the active project when present, otherwise `~/.agents/pstack-models.md`. This file is explicitly read by pstack; Codex does not automatically load it as a rule. Do not write model choices into `AGENTS.md` or change the host's global model settings.

The embedded upstream Claude, Grok, Composer, effort-suffixed slugs, and family-specific fallback rules are historical defaults. In Codex, **every unconfigured role inherits the parent model and reasoning effort**. A panel with no configuration retains its upstream seat count, with one fresh parent-model worker per seat. Describe this as independent perspectives on the same model, not multiple model families.

`inherit-parent` and `auto` omit model and reasoning overrides. A real configured value is `<model>` or `<model> <reasoning_effort>`; confirm both against the session's available choices. Keep model and reasoning in separate supported tool fields. Do not append an effort or `-fast` suffix to a model ID. For a collaboration tool that requires `fork_turns: "none"` for overrides, use it and supply a complete brief. Preserve full parent context when inheriting if useful. Use a speed/service-tier option only when actually supported and authorized.

If a configured override cannot be expressed or is rejected, inherit the parent and disclose the fallback once. Never try guessed model IDs or another provider's default. Use different model families only when multiple validated models are available. `$pstack:setup-pstack` configures the same role labels the upstream workflows use.

## History

Prefer the host's session/history tools. With app-server access, use workspace-filtered `thread/list` and `thread/read` or the equivalent exposed operations. Do not start an inference turn merely to read history.

For local history without a session tool, Codex rollouts may be under `${CODEX_HOME:-~/.codex}/sessions/` and `archived_sessions/`. Inspect only `session_meta` metadata first and select entries whose payload `cwd` matches the active workspace or an explicitly in-scope Git worktree. Only then search/read the selected conversation bodies. Never grep all session bodies across projects. JSONL entries include typed metadata, messages, and tool events; decode their `type` and `payload` rather than treating every line as a message. Skip another workspace unless the user explicitly includes it. If history is unavailable, use the visible conversation and say what evidence is missing.

For `worktree-audit.sh`, optionally set `PSTACK_TRANSCRIPTS_DIR` to a temporary directory containing only already-scoped transcripts. Without it the audit omits chat recency; it must not treat that as evidence that no recent chat exists.

## Host features

| Upstream feature | Codex behavior |
| --- | --- |
| Custom modes, Option/Alt+Enter | Invoke `$pstack:poteto-mode` for each task that needs it. Do not promise Cursor UI gestures in Codex. |
| `/loop` | Use a supported goal/long-running facility only when explicitly requested. Otherwise work within the active session; do not promise unattended continuation after it ends. |
| Cursor Automations, `/automate`, `update_state` routines | Use an available, documented Codex scheduling/automation integration. Scheduling alone does not provide Slack events or webhook triggers. For those, verify an existing external event runner and its actual API. If absent, prepare prompts/configuration and report the missing runner; never call a Cursor backend. |
| `SendToUser` secret requests | Use an actual secret-entry facility when exposed, or have the user set the named server-side environment variable outside chat. Do not request a secret in chat or claim a nonexistent secret card. |
| Grok Bot/webhook UI | Follow this port's `make-bot-ui` skill: a local server starts Codex through its supported CLI or a documented app-server integration. |
| Bugbot / agentic security review | Read existing forge checks/comments as ordinary review evidence. Do not start or wait for a service absent from this repository. Use the independent-review playbook when applicable. |
| Built-in skill/test/eval helpers | Discover actual installed capabilities. Use pstack's bundled skill or repository scripts when possible. State any missing check instead of claiming it ran. |

When a step requires a missing host feature, record `unavailable: <feature>; <effect on the task>` and continue independent work. If the missing result is necessary for the requested outcome, report the remaining dependency. Never invent a URL, credential, trigger, successful check, or approval.
