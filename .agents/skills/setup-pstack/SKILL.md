---
name: setup-pstack
description: Configure the available Codex models and reasoning effort pstack uses per role. Use for $pstack:setup-pstack, configure pstack models, pstack budget, or changing model choices.
---

Before following this workflow, read the [Codex adapter](../poteto-mode/references/codex.md) once per session.

# Setup pstack

Write `.agents/pstack-models.md` in the active project. Use `~/.agents/pstack-models.md` only when the user asks for personal settings. Project settings take precedence. Every pstack skill explicitly reads this configuration through the adapter; it is not an automatically applied Codex rule.

## 1. Detect available choices and load current state

Use the actual subagent tool schema or a model-list capability exposed by this Codex session. Validate reasoning levels separately from model IDs. Do not infer entitlement from public documentation or copy a model slug from upstream. If the host cannot enumerate overrides, offer `inherit-parent` and `auto`; ask for a validated model only when the user wants an override.

Read project configuration first, otherwise personal configuration. Preserve existing role choices. With no file, every role inherits the parent model and reasoning. Panel defaults are two independent workers on the parent model.

## 2. Choose the budget and models

Use the available user-input tool, or a concise text question when it is unavailable. Offer:

- `inherit-parent` — keep the session's model and reasoning
- `unlimited` — max reasoning when supported
- `large` — xhigh reasoning when supported
- `medium` — high reasoning when supported
- `small` — medium reasoning when supported

A budget changes only explicit model entries. For each entry, choose a supported reasoning level at or below the requested level. If none is known, leave effort inherited and disclose it. Model IDs and reasoning are separate values; never construct an effort-suffixed model slug. `auto` and `inherit-parent` always inherit both.

Show all roles and their values, plus any removed retired roles. Let the user accept or change specific roles. A scalar role takes `inherit-parent`, `auto`, `<validated-model>`, or `<validated-model> <validated-effort>`. Panel roles take comma-separated entries; every entry, including aliases, creates one seat. `arena cross-judge pool` is a pool, but Arena runs one judge. It tries only values from a family other than the parent's, in list order, so order it by preference. An `inherit-parent` or `auto` value never judges.

## 3. Validate and write

Every explicit model and reasoning level must be supported by the session. Never guess a replacement when a model is unavailable. Explain the issue and keep the previous configuration until the user chooses a valid value.

Write the complete file idempotently, preserving the chosen scope. No YAML frontmatter is needed. Default shape:

```text
# pstack model configuration. Missing roles inherit the parent.
# budget: inherit-parent
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent, inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent, inherit-parent
interrogate reviewers: inherit-parent, inherit-parent
```

Role labels can contain commas. Split a line at its first colon before parsing its scalar or panel value. Do not change Codex's global model configuration, managed settings, or `AGENTS.md`.

## 4. Confirm and offer verification

Report the written path and any supported-override limitations. The next pstack task reads the file; a restart is unnecessary.

If the project lacks a `verify-*` skill or real-app harness, offer once to run `$pstack:create-verification-skill`. If it lacks formal verification, offer once to run `$pstack:create-formal-verification-skill` for a suitable critical property. These are optional; declining does not block configuration. New skills always go in `.agents/skills/`.
