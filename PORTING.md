# Porting guide

This guide explains how the source pstack package is adapted for Codex and how to repeat the work when a newer source revision is available. Keep this file current with the source pin, local exceptions, and host-compatibility decisions.

## Current baseline

The current port is based on the `pstack` directory in [cursor/plugins](https://github.com/cursor/plugins/tree/0b46ec399d55f2829e88822998f53b84944837d3/pstack).

| Field | Value |
| --- | --- |
| Source revision | `0b46ec399d55f2829e88822998f53b84944837d3` |
| Source version | `0.15.46` |
| Primary source author | Lauren Tan |
| Additional bundled skills | `deslop`, `control-cli`, and `control-ui` |
| Target host | Codex |
| License | MIT, retained with the repository |

The port keeps the workflow content, orchestration logic, pull-request watcher, and statechart tooling where they work on Codex. Host-specific instructions, paths, metadata, and integrations are adapted at the boundary.

## Repository layout

| Purpose | Location in this repository |
| --- | --- |
| Codex plugin manifest | `.codex-plugin/plugin.json` |
| Local marketplace entry | `.agents/plugins/marketplace.json` |
| Skills | `.agents/skills/<skill-name>/` |
| Skill invocation metadata | `.agents/skills/<skill-name>/agents/openai.yaml` when the skill needs it |
| Delegated role briefs | `agents/*.md` |
| Shared host adapter | `.agents/skills/poteto-mode/references/codex.md` |
| User-facing documentation | `README.md` and `docs/` |
| Skill-owned scripts and tests | The `scripts/` directory inside the owning skill |
| Durable run state | `${CODEX_HOME:-~/.codex}/pstack/<workspace-key>/` |

Skills must stay one level below `.agents/skills/`, with each skill's entry point at `SKILL.md`. Resolve paths from the installed plugin root when a workflow runs outside this checkout.

## Porting rules

### Preserve source behavior

Keep workflow steps, prompts, examples, and tests intact when they describe behavior that is independent of the host. Make the smallest targeted edit when a host assumption is incompatible. Preserve legal notices and source assets.

### Adapt the package boundary

Map source package metadata into `.codex-plugin/plugin.json`. Keep the marketplace entry in `.agents/plugins/marketplace.json` aligned with the manifest. The manifest's `skills` path must resolve to `.agents/skills/`.

### Adapt skill metadata

Translate invocation and policy metadata into the `agents/openai.yaml` format supported by Codex. Keep the skill's `SKILL.md` as the source of workflow instructions. Role files in `agents/` are prompt briefs for delegates. They do not register new agent types.

### Centralize host differences

Put Codex-specific mappings in `.agents/skills/poteto-mode/references/codex.md` and make each affected skill read that adapter. Keep tool names, path rules, model settings, durable state, history lookup, delegation, and host-feature behavior in one place. Do not scatter replacement APIs through otherwise preserved workflow text.

The adapter currently covers these mappings.

- Cursor skill names become namespaced Codex skills such as `$pstack:poteto-mode`.
- Cursor `Task` and role parameters become native collaboration operations with the role requirements included in the brief.
- Cursor stores and project trackers become the external pstack state directory and its `notes.md` tracker.
- Cursor dashboard checks become the host's read-only agent status operation plus local receipts.
- Cursor custom modes and keyboard shortcuts become explicit skill invocation.
- Cursor loops, automations, webhook triggers, and secret cards require a documented Codex or external integration before they can be used.
- Source-relative script paths become absolute paths resolved from the installed plugin root.

### Keep the target scope explicit

This repository targets Codex. Do not add compatibility layouts for other hosts unless the port explicitly requires them. External Slack, issue-tracker, event-runner, and repository-specific verification integrations remain prerequisites for workflows that call them.

The removed Benny automation pack stays excluded from future source imports. Do not reintroduce `pstack/automations/benny/` during a sync.

## Fresh port procedure

Use a separate branch or worktree for a new port. Keep the source revision and the port changes reviewable.

1. **Pin the source.** Record the repository URL, exact commit, version, authorship, license, and the source subdirectory. Do not use a moving branch as the reproducibility record.
2. **Inventory the source.** List skills, scripts, tests, assets, manifests, role files, automations, and documentation. Mark each item as preserved, adapted, excluded, or replaced.
3. **Copy the source snapshot.** Import the source files with their executable bits and assets intact. Preserve the source license.
4. **Normalize the layout.** Move skills under `.agents/skills/`, write the Codex plugin and marketplace manifests, and place delegate briefs under `agents/`.
5. **Add Codex metadata.** Create or update `agents/openai.yaml` for each skill that needs invocation policy or other Codex metadata. Keep names and descriptions consistent with `SKILL.md`.
6. **Apply the adapter.** Read the shared adapter and update host-specific paths, tools, stores, history, delegation, and optional integrations. Keep the workflow body unchanged when the adapter can express the difference.
7. **Resolve unsupported features.** Replace a source host feature only when a documented Codex capability or external integration provides the same contract. Otherwise record the missing dependency at the affected workflow boundary and leave the source behavior clear.
8. **Apply repository exclusions.** Omit removed automation packs and any other explicitly excluded source paths. Check the imported file list after the copy so excluded files cannot return accidentally.
9. **Update documentation.** Point installation and source-scope links at the current files. Explain any user-visible invocation or prerequisite changes in `README.md` and the relevant guide pages.
10. **Run validation.** Use the checks in [Verification](#verification). Read the complete diff and inspect every added, removed, and renamed file.
11. **Record the result.** Update the source baseline and local exception sections in this guide. Commit the source snapshot and the Codex adaptation separately when that makes review easier.

## Sync procedure

Use this sequence for each later source revision.

1. Fetch or obtain the new source revision and record its exact commit and version.
2. Compare source inventories and file-level changes against the current pinned revision.
3. Import new and changed source files into a temporary sync area. Do not overwrite the adapter, manifests, repository documentation, or local patches blindly.
4. Review renames and deletions. Migrate local edits to the new path before removing a file.
5. Reapply the layout and metadata rules above. Check every changed skill for stale source paths, host commands, role names, and invocation syntax.
6. Reapply repository exclusions, especially `pstack/automations/benny/`.
7. Reconcile local patches with the new source. The worktree audit patch described below can be removed only after the source contains an equivalent full-path fix.
8. Update the source revision and version in this guide, the plugin manifest, and any installation documentation that names the version.
9. Run the full verification set, then review the diff for accidental source drift and lost Codex adaptations.
10. Commit the sync and adaptation in reviewable units. Include the source revision in the sync commit message.

## Local exceptions

### Worktree audit path handling

`.agents/skills/poteto-mode/scripts/worktree-audit.sh` carries a local fix over the pinned source. It reads `git worktree list --porcelain -z` and passes complete paths to Git, so a worktree directory containing spaces is handled as one path. Keep this patch until the source script has the same behavior. When that happens, take the source version, remove the local patch, and delete this exception.

### Removed automation

The Benny automation pack is not part of this port. Future imports must continue to omit its source directory and its associated documentation, skills, and templates.

### Removed bot UI skill

The source `make-bot-ui` skill is not part of this port. Its provider-specific webhook workflow has no documented Codex integration, so future imports must continue to omit the skill and its user-facing documentation unless a supported integration is documented.

## Verification

Run the checks from the repository root after every port or sync.

```sh
git diff --check
jq empty .codex-plugin/plugin.json .agents/plugins/marketplace.json
```

Run the bundled TypeScript tests and typecheck from the owning script directory.

```sh
cd .agents/skills/poteto-mode/scripts
bun install --frozen-lockfile
bun test
bun run typecheck
```

Check the installed package through the same path used by CI. The workflow in `.github/workflows/plugin-install.yml` installs the current Codex CLI, adds this repository as a marketplace, installs the plugin, verifies required skills, and compares every file under `.agents/` with the installed copy.

Before opening the sync for review, also check the following.

- Every skill has a readable `SKILL.md` and any required `agents/openai.yaml`.
- Every relative skill link resolves from its owning directory.
- Every script reference points to the installed plugin root or the owning skill.
- No excluded automation files were imported.
- The plugin manifest version and source baseline agree.
- README and guide links resolve after file renames.
- The diff contains only intentional source updates, Codex adaptations, and documentation updates.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| A skill is missing after installation | Confirm the manifest's `skills` path and verify the skill has a top-level `SKILL.md`. |
| A skill invokes with the wrong name | Check the package namespace, the skill directory name, and `agents/openai.yaml`. |
| A workflow refers to an unavailable tool | Update the shared adapter with the documented host operation or record the missing external prerequisite. |
| A script works in the checkout but fails after installation | Replace checkout-relative paths with paths resolved from the installed plugin root. |
| A linked worktree is reported incorrectly | Check the NUL-delimited worktree parsing in `worktree-audit.sh`. |
| A source sync reintroduces excluded files | Compare the imported file list with the exclusions before running tests. |
| Tests cannot start | Confirm Bun is installed and run the commands from the script directory so its lockfile and package manifest are used. |
