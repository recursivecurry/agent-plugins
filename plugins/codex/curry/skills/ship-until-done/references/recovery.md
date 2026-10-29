# Block, continue, and resume

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
