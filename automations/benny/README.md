# benny

benny gives you two Codex-compatible automation jobs for slack issue reports. one triages each report. the other reproduces confirmed bugs and may prepare a small draft fix.

the files in this directory are dormant setup and automation sources. they do not appear as slash skills.

## set it up

1. point Codex at [`FOR_AGENTS.md`](./FOR_AGENTS.md) and name the target repository.
2. let setup merge this whole directory into the target at `.agents/automations/benny/`. it must preserve destination-only files and review conflicts instead of overwriting local edits.
3. resolve shared pstack skills from the target project's `.agents/skills/`, with companion `agents/` and `docs/` resources. No editor plugin settings are needed.
4. keep user-owned configuration outside the copied pack, for example in `.agents/benny/`. adapt [`configuration.example.yaml`](./templates/configuration.example.yaml) and [`feature-map.example.md`](.agents/skills/reproduce-and-fix-issues/references/feature-map.example.md).
5. commit the target project's `.agents/skills/` installation, `.agents/automations/benny/`, and any secret-free configuration before enabling either automation.
6. review each new automation draft or update existing automations in their editors. then send a harmless test report and verify every source-channel post stays in the original thread.

A live Slack trigger requires a documented external event runner or an available host integration with event support. Without one, setup prepares prompts and configuration and leaves activation pending.
