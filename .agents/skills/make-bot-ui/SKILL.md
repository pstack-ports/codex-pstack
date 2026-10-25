---
name: make-bot-ui
description: Build a local page or dashboard whose buttons start Codex work through a server, with optional authenticated webhooks and Tailscale access.
---

Before following this workflow, read the [Codex adapter](../poteto-mode/references/codex.md) once per session.

# Make a bot UI

Build a page the user clicks. A local server validates a small JSON action and starts a Codex job in the intended workspace. Keep credentials and process execution on the server.

## Choose the Codex entry point

Reuse the repository's existing agent runner when available. Otherwise inspect the installed `codex exec --help` and use its supported flags. A typical invocation is `codex exec --json -C <workspace> <prompt>`, started as a subprocess with an argument array, never a shell-interpolated command. For persistent conversations, use an existing documented Codex app-server integration and its actual session/turn schema.

Define a fixed action-to-prompt mapping. Put the validated request fields into a clearly delimited data section of that prompt. Treat those fields as untrusted data, not instructions or shell code. Run under the configured Codex permissions; do not add sandbox/approval bypass flags. A process starting is not evidence that its task succeeded.

## Build the local server and page

1. Find the project's runtime and reuse its HTTP/UI stack.
2. Define the allowed actions, input types, workspace, and observable result for each action.
3. Add a health route that performs no agent inference, plus a job route that validates input and returns a job ID.
4. Capture the job's structured output, errors, exit status, and final result separately. Give the page a truthful queued/running/succeeded/failed state.
5. Bound concurrent jobs and give each writing job its own worktree when parallel edits would conflict. Set a timeout and clean up children on cancellation.
6. Bind to `127.0.0.1` for local use. Validate browser origins and prevent arbitrary command execution. Keep tokens in server-side environment variables or the actual available secret store, never in browser bundles or logs.

Probe the health route, then test one harmless authorized action through the real UI. Inspect its resulting Codex output before claiming the job succeeded.

## Optional external webhook

Use the user's existing documented webhook or event runner only when requested. Verify the endpoint and authentication contract. Do not invent a routine-creation tool, webhook URL, secret-request card, or credential-file location.

If a sender key is required, have the user enter it through an available secret facility or set the named server-side environment variable outside chat. Browser requests go to the local server; only that server sends the authenticated webhook request. Apply the endpoint's real headers and response semantics, a bounded timeout, and idempotency for retried actions. Never claim an HTTP acceptance response proves the downstream task finished.

## Optional Tailscale access

When the user requests access from tailnet peers, inspect `tailscale status` and `tailscale ip -4` and reuse the existing node. Use the installed version's documented serve/bind options. Keep authentication at the job endpoint and restrict access to the intended peers. If Tailscale is absent or needs login, use its supported installation/login flow and report that dependency before claiming the UI is reachable. Do not request credentials in chat.

Test from the intended access path and report the observed URL. Clean up temporary servers, job processes, and profiles when the task is done unless the user asked to keep the UI running.
