# Platform support

Installation does not establish that a host can run the workflow. Check the installed
host's controls and exposed tool schemas before changing code or creating a PR.
The Hermes distribution does not register this workflow as a skill or slash command.
Its files are reference-only. No invocation adapter or native implicit-invocation policy
has been verified for this workflow, so stop before implementation, PR creation, or merge.
Hermes model families are not automatically mapped to runtime IDs. Independent model
selection, fresh reviewer context, and a distinct eligible GitHub identity would also
need verification before a future integration could enable execution.


Quoted commands, ordinary requests and incidental skill mentions never authorize execution.
No always-on hook starts this workflow. Missing invocation controls block all work.

## Models and independent context

Read the actual implementer model ID and advertised reviewer IDs from the host. Select the
opposite family below; record exact IDs and the host evidence that maps them to these families.


Unknown families, absent counterparts or an unidentifiable implementer block execution.
Never substitute the same model or treat other deployment mappings as supported review pairs.

Use a separate reviewer context with conversation inheritance disabled.
Use the host's documented fresh-context and model-selection controls for other tools.
Do not invent those arguments on an incompatible tool. If isolation cannot be established,
stop; a second role in the same conversation does not qualify. Give the reviewer only the
review packet and independently accessible evidence. Reuse that reviewer for subsequent
rounds so findings persist, while keeping implementer history out of its context.

## GitHub identities

Before implementation, identify the PR author account, the reviewer's authenticated account,
and their repository permissions. Different models do not create different GitHub users.
Require an authorized reviewer identity distinct from the PR author that can submit a valid
`APPROVE` review and satisfies repository policy. The reviewer must control submission of
its own verdict. Never relabel an implementation account's comment as reviewer approval,
use unprovided credentials, or count self-approval. Missing access or an eligible account is
a blocker. Preserve any review already performed, but do not merge without valid approval.

## Sources and limits

Verified against primary platform documentation; recheck controls if the host changes:

- [Claude Code skills](https://code.claude.com/docs/en/skills): invocation control, direct
  commands, and plugin namespacing.
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): separate contexts and
  Claude model selection. Verify available models and selectors in the running host.
- [OpenAI skills](https://developers.openai.com/codex/skills/): `$`, `/skills`, and
  Codex's native skill invocation policy (not a Hermes execution control).
- [OpenAI subagents](https://developers.openai.com/codex/subagents/): host configuration
  and model selection. An installed version's exposed tool schema remains decisive.
- [GitHub review permissions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews):
  reviews, approval, and restrictions on approving one's own PR.
