## 2024-05-23 - String Replacement Performance
**Learning:** In Python 3.x, for a small number of replacements (e.g., 11 chars) on moderate length strings, a simple loop with `str.replace()` can be significantly faster (approx 2.5x) than `str.translate()`, possibly due to the overhead of creating the translation table or Unicode handling nuances in the specific environment.
**Action:** Measure before optimizing string manipulations; don't assume `translate` is always faster than multiple `replace` calls.
