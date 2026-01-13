## 2024-10-24 - String Optimization Surprises
**Learning:** In Python, iterative `str.replace` can be faster than `str.translate` or `re.sub` for simple character removals on short strings. `is_drone` optimization using `set` lookup and compiled Regex was ~3.5x faster.
**Action:** Always benchmark string manipulations before assuming `translate` or `regex` is faster. Prefer `set` for containment checks.

## 2024-10-24 - Redundant Sanitization
**Learning:** Reusing the result of expensive (or even cheap but frequent) functions like `sanitize_string` in tight loops is a low-hanging fruit.
**Action:** Assign sanitized values to variables and reuse them.
