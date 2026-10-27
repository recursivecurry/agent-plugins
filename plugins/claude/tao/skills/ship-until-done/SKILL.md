---
# Generated from src/skills/ship-until-done/SKILL.md.tmpl. Edit the source, not this file.
name: ship-until-done
description: Complete a task list through implementation, independent cross-model review, approval, and merge. Use only on direct /ship-until-done invocation (namespaced where required), never from ordinary requests, quoted commands, or name mentions.
disable-model-invocation: true
argument-hint: "[task list or source]"
license: MIT
metadata:
  author: recursivecurry
  version: 1.1.0
---

# Ship until done

Start only on direct developer slash invocation, never quoted commands or incidental mentions.
Plugin command: `/tao:ship-until-done`. Review pair: Fable ↔ Opus.

Load references at their stage; do not preload later stages:

1. **Before work:** read [preflight](references/platforms.md) and [execution](references/workflow.md).
   Verify capabilities and identities; freeze scope, criteria and dependencies in a durable record.
2. **Each ready item:** implement, validate, open its PR. At first review, read
   [review packet](references/review-packet.md). Use an isolated other-model reviewer; retain
   that reviewer through fixes, rebuttals and re-review.
3. **Before every merge:** read [merge gate](references/merge.md). Require reviewer-confirmed
   findings, current-SHA approval and required checks. Confirm actual merge and merge SHA.
4. **Blocker or resume:** read [recovery](references/recovery.md); preserve state, refresh
   evidence and continue independent items.

Re-read references lost from context. Continue within the authorized scope without redundant
permission requests; respect repository rules and host gates. Never bypass checks, weaken
criteria or replace a dissenting reviewer. Report every item's PR, merge result and SHA.
Completion requires every supplied item to be verified merged.
