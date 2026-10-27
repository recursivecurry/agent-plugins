# Execution and recovery

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
5. Request re-review from the same reviewer, supplying new SHA, changes, replies and evidence.
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
8. Apply the merge gate below, merge using the allowed method, then fetch the PR to verify
   actual merged state and merge SHA. A queued or requested merge remains pending. Only
   after merge confirmation mark the item merged and proceed directly to the next ready item.

## Merge gate

Immediately before merging, fetch fresh PR metadata, reviews, required checks, and applicable
repository rules. Use the available GitHub API, connector or CLI; record the returned evidence
and SHAs rather than assuming a tool's success message establishes approval or checks.

Require the current PR HEAD to equal the recorded reviewed and approved SHA. Verify the
approval is submitted, still valid, from the required account, and not dismissed; account for
blocking reviews and all repository-required approvals. Require all findings to have a
reviewer-confirmed disposition. Fetch check runs and commit statuses for this revision and
require the conclusions accepted by repository policy. Pending, failed, missing, stale or
uninspectable required results block merge. Record an explicitly verified absence of required
checks if the repository has none; absence of access is not evidence of absence.

If CI validates a synthetic merge commit or merge-queue candidate, verify its relationship
to the current HEAD and base according to repository policy and record both SHAs. Refresh
candidate checks when that relationship changes. If the HEAD changes after approval, return
to validation and independent re-review for the new revision; never reuse approval for an
older SHA. Merge with an expected-head condition when the tool supports it. If it does not,
require an equivalent atomic repository gate protecting the approved revision; otherwise
stop rather than risk merging an unreviewed race. Never use an admin bypass or turn off rules.

## Block, continue, and resume

Repair ordinary implementation and check failures autonomously. For a transient external
failure, allow at most three attempts of the same operation, with bounded backoff and a
status update; do not replay a mutation until checking whether it succeeded remotely.
Permission denial, unavailable models, invalid review identity, unsupported isolation or
invocation, contradictory requirements, and exhausted external retries are real blockers.
Record them precisely instead of retrying indefinitely or asking for routine permission.

Continue with independent ready items when an item is blocked. Keep its dependents blocked.
Global invocation or model/identity prerequisites block the whole workflow. When no item
can proceed, report item states, evidence and the smallest missing input or capability.

After interruption, load the progress record, original requirements and current repository
state. Reuse branches, PRs and the existing reviewer; do not duplicate PRs or skip unfinished
items. Refresh remote HEAD, approval, checks and merge state, and invalidate stale evidence.
Continue within the original invocation's scope when its trusted authorization is preserved;
otherwise require a new actual slash invocation. A resumed conversation is not proof of merge.

The final report lists every item, PR, actual merge result and merge SHA. Include incomplete
states and blockers. Claim overall completion only when all items have verified merges.
