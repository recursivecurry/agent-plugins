---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Edit the following README paragraph so it reads naturally. Return only the edited paragraph.

Wondering how the cache works? You're in the right place. This isn't merely a speed upgrade; it's a reliability upgrade. Our cache layer is lightweight, resilient, and future-proof, and it was carefully designed to handle up to 12,000 requests per second with a default TTL of 300 seconds. Industry leaders recognize that caching is essential. Entries older than the TTL are evicted lazily on the next read, not by a background sweeper, so a stale entry can survive past its TTL until something reads it. The result? A cache you can trust.
