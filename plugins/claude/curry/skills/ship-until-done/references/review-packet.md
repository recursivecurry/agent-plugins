# Independent review packet

Supply this packet to a reviewer created with no implementer conversation history. Fill in
facts and source links; do not include the implementer's internal conclusions or prescribe
the verdict. Ensure the reviewer can independently access all sources and repository files.

```text
Task: Independently review this item through final GitHub approval or evidence-backed rejection.
Original developer requirements: <verbatim text or accessible original source>
Item and acceptance criteria: <item ID, each criterion, relevant dependencies>
Repository and instructions: <repository URL/path; instruction file locations>
PR: <URL and number>
Revision: <exact HEAD SHA, base ref/SHA>
Validation: <required checks, commands, environment constraints, evidence locations>
Reviewer setup: <required other-model ID; isolated context; eligible GitHub identity>
Finding ledger: <accessible location; complete findings, replies, SHAs and verification evidence>
Progress record: <location>

Read the original requirements, repository instructions, diff and related code yourself.
Verify relevant behavior and run necessary checks; do not approve from an implementer
summary or a claim that tests passed. Do not change implementation files during review.
For each finding, post location, triggering condition, expected impact and checkable evidence
(code, requirement, rule or reproduction). Label it required correction or optional suggestion.
Independently recheck each fix and rebuttal. State whether each finding is resolved and why;
thread resolution by the implementer is not your confirmation. Review the final HEAD and
record that SHA, verification results and verdict. If every criterion is met and all findings
have a justified disposition, submit APPROVE on GitHub for that exact SHA using the eligible
reviewer identity. Otherwise request changes with evidence or report the precise blocker.
```

## Re-review update

Reuse the existing reviewer context. Send only the new HEAD/base SHAs, changes since the
last round, finding IDs with fixes or rebuttals and verification evidence, and the complete
ledger's location. The reviewer reads the changed diff, verifies the ledger including every
unresolved or disputed finding, and independently applies the same final-approval criteria.
Do not resend unchanged requirements or the full transcript while they remain in context.
If reviewer context is lost, reload this packet and the complete ledger before review;
if a successor is unavoidable, preserve the blocker and never replace a dissenting reviewer
to seek approval.

Reply to each finding with its ID/location, accepted or disputed disposition, the code change
or counterevidence, validation command/result and relevant SHA. The reviewer checks these
claims directly and records confirmation or the remaining problem. Keep every prior finding
accessible on re-review, including disputed and unresolved findings; never filter by whether the implementer agrees.
