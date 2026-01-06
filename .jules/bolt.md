## 2024-05-23 - [Sanitization Optimization Surprise]
**Learning:** `str.translate` is not always faster than multiple `str.replace` calls.
**Action:** Always benchmark specific use cases. In this project, `sanitize_string` with iterative `replace` (11 chars) was ~2x faster than `translate` for short strings. This counter-intuitive result prevented a "optimization" that would have been a regression.
