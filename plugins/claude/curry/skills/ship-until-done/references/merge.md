# Merge gate

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
