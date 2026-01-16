## 2026-01-15 - String Sanitization Bottleneck
**Learning:** `extract_device_detections` is a primary bottleneck. `sanitize_string` accounted for ~37% of execution time. Benchmarking showed `re.sub` is faster than `str.replace` loop and `str.translate` for this specific case (possibly due to string characteristics or overhead).
**Action:** Use `re.compile` and `re.sub` for sanitization.

## 2026-01-15 - Redundant String Processing
**Learning:** `extract_device_detections` called `sanitize_string` multiple times for the same field (Common Name) when checking `is_drone`.
**Action:** Assign sanitized values to variables and reuse them.

## 2026-01-15 - Drone Detection Optimization
**Learning:** `is_drone` used linear search over lists. Using `re.compile` for SSIDs and `set` for MAC prefixes improved its performance by ~2.5x-4x.
**Action:** Use sets for O(1) lookups and compiled regex for pattern matching.
