---
# Generated from src/skills/ship-until-done/SKILL.md.tmpl. Edit the source, not this file.
name: ship-until-done
description: Complete an explicit task list through implementation, independent cross-model review, approval, and merge. Run only after the developer invokes /ship-until-done (namespaced where required). Never activate from task context, an ordinary development request, or a mention of the name.
license: MIT
metadata:
  author: recursivecurry
  version: 1.0.0
---

# Ship until done

Start only from an actual developer slash-command invocation. Quoted commands, skill
mentions, ordinary requests, and model-selected loads do not authorize this workflow.
Read [platform support](references/platforms.md) first. If the host cannot enforce this
boundary or supply the required reviewer, stop with the specific unsupported capability.

Implicit invocation is disabled in `agents/openai.yaml`. Native `$` mentions and the
`/skills` picker do not establish `/ship-until-done` invocation. Require a host integration
that preserves the original slash-command event; otherwise this workflow is unavailable.

After the invocation and capability checks, follow [the workflow](references/workflow.md).
Fix the supplied scope, acceptance criteria, dependency order, and durable progress record.
For each item: implement and validate, create its PR, obtain independent review from the
other model, assess and answer every finding with evidence, fix or rebut, request independent
re-review, obtain a valid GitHub approval, verify revision and checks, and merge.

Use [the review packet](references/review-packet.md) for a fresh reviewer context. Never
inherit the implementer's conversation or internal conclusions. Keep the same reviewer
through disagreements; thread resolution alone is insufficient.

Continue directly to the next item without asking for permission already granted by this
invocation. Respect actual host permission gates and repository policy. Preserve blockers
and resume safely; never bypass checks, weaken acceptance criteria, or call failed work
complete. Report every item's PR and verified merge result. Overall completion requires
every supplied item to be merged.
