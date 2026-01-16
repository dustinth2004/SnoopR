## 2026-01-16 - [Regex vs Loop Performance]
**Learning:** `re.compile().sub()` is significantly faster (~2x) than iterative `str.replace()` loops for sanitizing short strings (common case), but slightly slower for very long strings. Since this application mostly processes short fields (SSID, Type), regex is the better choice.
**Action:** Use compiled regex for string sanitization on short fields, but verify with benchmarks on representative data.
