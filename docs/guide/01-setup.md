# Set up pstack in Codex

Open this checkout in a fresh Codex session. Project skills are discovered from `.agents/skills/`. See the [README](../../README.md#install) for installing into another project or using the plugin manifest.

Run `$pstack:setup-pstack`. Every unconfigured role inherits the current Codex model and reasoning. Setup can select explicit models and separate reasoning levels only when the host confirms they are available. Project configuration lives at `.agents/pstack-models.md`; personal configuration, when requested, lives at `~/.agents/pstack-models.md`. Pstack reads the file itself; it is not a host rule and needs no restart.

Panel roles use comma-separated lists, with one worker per entry, including `inherit-parent`. A cross-judge pool selects one judge. Two workers using the same model are independent perspectives, not a multi-model comparison. Start with the inherited defaults and change only the roles you need.

Setup offers `$pstack:create-verification-skill` if the project has no real-app harness, and `$pstack:create-formal-verification-skill` if a critical property would benefit from a proof or model checker. Both are optional. Generated skills go in `.agents/skills/`.

Start a task with:

```text
$pstack:poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

Pstack chooses a playbook, tracks its steps, and uses the [Codex adapter](../harness/codex.md) for tools and delegation. Start each new task that needs this workflow with `$pstack:poteto-mode`. Long-running goals and scheduled/event-driven work require a facility actually available in your host.

Next: [Route work through poteto-mode](./02-poteto-mode.md).
