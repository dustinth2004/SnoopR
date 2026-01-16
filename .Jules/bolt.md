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
