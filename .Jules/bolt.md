## 2026-01-16 - [Regex vs Loop Performance]
**Learning:** `re.compile().sub()` is significantly faster (~2x) than iterative `str.replace()` loops for sanitizing short strings (common case), but slightly slower for very long strings. Since this application mostly processes short fields (SSID, Type), regex is the better choice.
**Action:** Use compiled regex for string sanitization on short fields, but verify with benchmarks on representative data.

## 2024-10-24 - String Optimization Surprises
**Learning:** In Python, iterative `str.replace` can be faster than `str.translate` or `re.sub` for simple character removals on short strings. `is_drone` optimization using `set` lookup and compiled Regex was ~3.5x faster.
**Action:** Always benchmark string manipulations before assuming `translate` or `regex` is faster. Prefer `set` for containment checks.

## 2024-10-24 - Redundant Sanitization
**Learning:** Reusing the result of expensive (or even cheap but frequent) functions like `sanitize_string` in tight loops is a low-hanging fruit.
**Action:** Assign sanitized values to variables and reuse them.
