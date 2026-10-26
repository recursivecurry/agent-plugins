---
type: llm
weight: 1
---

The response is a single edited paragraph with no commentary, scores, or badges.

It removes the staged opener ("Wondering how the cache works? You're in the right place."), the empty contrast ("isn't merely a speed upgrade; it's a reliability upgrade"), the forced triad ("lightweight, resilient, and future-proof"), the vague authority ("Industry leaders recognize"), and the dramatic closer ("The result? A cache you can trust."). Rewording these into another phrase of the same kind does not count as removing them.

It preserves every fact: 12,000 requests per second, a default TTL of 300 seconds, lazy eviction on the next read rather than a background sweeper, and that a stale entry can survive past its TTL until something reads it. The causal relationship between lazy eviction and stale survival is intact.

It adds no facts that were not in the source.
