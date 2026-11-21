# Execution

## Establish scope and readiness

Accept a task list supplied with the command, an explicitly identified issue or issue list,
or a repository task file identified by the developer. Read the original sources. If no
list is identifiable, ask for that source before work. Freeze the item IDs, requirements,
acceptance criteria, dependencies, and order in the progress record. Derive criteria from
the request and repository evidence; ask only about ambiguities that change the outcome.
New discoveries belong in a separate backlog unless required to satisfy an existing item.
Do not silently expand the authorized list.

Complete the invocation, model, context, identity, repository access, and merge-policy
preflight from the platform reference. Read repository instructions and use the minimal-code
and git-hygiene skills. Preserve unrelated local changes; use isolated branches or worktrees
where needed. Follow repository branch, commit, CI, and merge conventions. Default to squash
only when policy permits it and the repository has no contrary convention.

Choose a durable, developer-accessible progress record in the repository's existing task
tracking location; otherwise use a local `ship-until-done-progress.md` outside the committed
source tree. Record its path in progress reports. Never put credentials or internal reasoning
in it. Persist after every transition and before a pause:

| Field | Record |
| --- | --- |
| Scope | Invocation source, original requirements, frozen item IDs, criteria, dependencies |
| Item | Status: pending, implementing, reviewing, approved, merged, blocked |
| Work | Repository, base, branch/worktree, PR URL, current HEAD SHA |
| Review | Implementer/reviewer model IDs, reviewer context ID and GitHub login, reviewed SHA, findings and replies, reviewer-confirmed resolutions, verdict |
| Approval | Review ID/URL, approver login, state, approved SHA |
| Checks | Check names, inspected SHA, result URLs and conclusions; merge-candidate SHA and its relationship to the PR HEAD/base when applicable |
| Merge | Method, confirmed merged state, merge SHA and URL |
| Blocker | Exact failed operation, evidence, attempts, next action, dependent items |

## Repeat for each item

1. Implement the item and run relevant checks plus repository-required validation. Diagnose
   failures from evidence and repair causes. Keep the diff scoped. Never disable required
   checks, lower criteria, conceal failures, or mark an unsuccessful check as passing.
2. Commit and open one PR for this item with the requirements, behavior, and actual validation.
   Look up an existing PR for the branch before creating one. Record its HEAD SHA.
3. Spawn the required other-model reviewer with inheritance disabled and the
   [review packet](review-packet.md). The reviewer reads requirements, repository rules, PR
   diff and related code, performs relevant validation, and posts actionable findings on the
   PR. Passing tests or the implementer's account alone cannot justify approval.
4. Evaluate every finding against requirements, code, rules, and reproducible evidence. For
   accepted findings, fix and reply with the change and validation results. For rejected
   findings, reply with the specific disagreement and checkable evidence. Distinguish optional
   improvements from defects; handling all comments does not mean accepting every suggestion.
5. Request re-review from the same reviewer using the compact update in the review packet.
   Preserve the complete finding ledger and its accessible location in the progress record.
   The reviewer independently verifies both fixes and rebuttals and confirms each finding's
   disposition. Resolve threads only when appropriate under repository conventions. An
   implementer's Resolve action cannot replace reviewer confirmation or final approval.
6. If the same dispute repeats for two rounds without new evidence, record the issue, both
   positions, evidence and attempted checks. Seek a discriminating test or the original
   requirement. Ask the developer one concrete question only if that cannot resolve it.
   Never replace a reviewer to seek approval or hide unresolved findings from any successor.
   If the reviewer is unavailable, preserve the blocker and full review record.
7. Repeat steps 4–6 until every finding has a reviewer-confirmed disposition and the reviewer
   independently approves the final revision. Require an actual GitHub `APPROVED` review
   from the eligible reviewer identity with its `commit_id` equal to the reviewed HEAD.
   A comment saying “approved,” resolved threads, or the implementer's assertion is insufficient.
8. Read and apply [the merge gate](merge.md), merge using the allowed method, then fetch
   the PR to verify actual merged state and merge SHA. A queued or requested merge remains pending. Only
   after merge confirmation mark the item merged and proceed directly to the next ready item.
