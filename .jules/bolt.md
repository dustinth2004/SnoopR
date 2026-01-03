## 2026-01-03 - Reuse Sanitized Strings
**Learning:** In a tight loop processing 50k+ items, redundant string sanitization calls for the same field (once for display, once for logic checks) add measurable overhead.
**Action:** Assign the sanitized result to a variable and reuse it.
