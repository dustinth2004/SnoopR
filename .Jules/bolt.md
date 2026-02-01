## 2026-01-16 - [Regex vs Loop Performance]
**Learning:** `re.compile().sub()` is significantly faster (~2x) than iterative `str.replace()` loops for sanitizing short strings (common case), but slightly slower for very long strings. Since this application mostly processes short fields (SSID, Type), regex is the better choice.
**Action:** Use compiled regex for string sanitization on short fields, but verify with benchmarks on representative data.
## 2024-05-23 - String Replacement Performance
**Learning:** In Python 3.x, for a small number of replacements (e.g., 11 chars) on moderate length strings, a simple loop with `str.replace()` can be significantly faster (approx 2.5x) than `str.translate()`, possibly due to the overhead of creating the translation table or Unicode handling nuances in the specific environment.
**Action:** Measure before optimizing string manipulations; don't assume `translate` is always faster than multiple `replace` calls.
## 2026-01-16 - [Regex vs Loop Performance]
**Learning:** `re.compile().sub()` is significantly faster (~2x) than iterative `str.replace()` loops for sanitizing short strings (common case), but slightly slower for very long strings. Since this application mostly processes short fields (SSID, Type), regex is the better choice.
**Action:** Use compiled regex for string sanitization on short fields, but verify with benchmarks on representative data.

## 2024-10-24 - String Optimization Surprises
**Learning:** In Python, iterative `str.replace` can be faster than `str.translate` or `re.sub` for simple character removals on short strings. `is_drone` optimization using `set` lookup and compiled Regex was ~3.5x faster.
**Action:** Always benchmark string manipulations before assuming `translate` or `regex` is faster. Prefer `set` for containment checks.

## 2024-10-24 - Redundant Sanitization
**Learning:** Reusing the result of expensive (or even cheap but frequent) functions like `sanitize_string` in tight loops is a low-hanging fruit.
**Action:** Assign sanitized values to variables and reuse them.
## 2026-01-15 - String Sanitization Bottleneck
**Learning:** `extract_device_detections` is a primary bottleneck. `sanitize_string` accounted for ~37% of execution time. Benchmarking showed `re.sub` is faster than `str.replace` loop and `str.translate` for this specific case (possibly due to string characteristics or overhead).
**Action:** Use `re.compile` and `re.sub` for sanitization.

## 2026-01-15 - Redundant String Processing
**Learning:** `extract_device_detections` called `sanitize_string` multiple times for the same field (Common Name) when checking `is_drone`.
**Action:** Assign sanitized values to variables and reuse them.

## 2026-01-15 - Drone Detection Optimization
**Learning:** `is_drone` used linear search over lists. Using `re.compile` for SSIDs and `set` for MAC prefixes improved its performance by ~2.5x-4x.
**Action:** Use sets for O(1) lookups and compiled regex for pattern matching.
## 2024-05-23 - String Replacement vs Translate
**Learning:** `str.replace` in a loop (11 iterations) proved to be 4x FASTER than `str.translate` for stripping special characters from short strings in this Python environment.
**Action:** Do not blindly assume `translate` is faster for deletion. For short strings and small delete sets, `replace` often wins due to lower setup overhead and optimized implementation for non-matching cases.

## 2024-05-23 - Set vs List for Prefix Matching
**Learning:** Using a set for checking MAC address prefixes provided a significant speedup (approx 1.7x) compared to iterating a list.
**Action:** Convert small lookup lists to sets when doing repeated membership checks, even for prefixes if length is fixed.

## 2024-05-23 - Regex vs List Iteration for Substring Matching
**Learning:** Using `re.compile(r'|'.join(...))` to check if any of a list of substrings is present in a string is significantly faster (approx 2.5x-4x) than `any(sub in s for sub in list)`.
**Action:** Use regex for multi-substring search.

## 2026-02-01 - Haversine Optimization
**Learning:** `map(func, list)` in Python has overhead due to iterator creation and function calls. Replacing `map(radians, ...)` with inline multiplication (`x * CONST`) yielded a ~1.6x speedup for the `haversine` function.
**Action:** Prefer inline arithmetic over `map` for simple element-wise transformations in hot loops.
