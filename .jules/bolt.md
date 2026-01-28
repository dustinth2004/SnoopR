## 2026-01-04 - Optimize SnoopR.py Device Extraction
**Learning:** `str.replace` in a loop was faster than `str.translate` for the specific sanitization required in this Python environment.
**Action:** When optimizing string operations, verify assumptions with benchmarks, as theoretical big-O benefits might be outweighed by implementation overhead for small datasets or specific patterns. Also, reducing redundant function calls and dictionary lookups in tight loops (like `extract_device_detections`) yields measurable improvements.
## 2026-01-03 - Reuse Sanitized Strings
**Learning:** In a tight loop processing 50k+ items, redundant string sanitization calls for the same field (once for display, once for logic checks) add measurable overhead.
**Action:** Assign the sanitized result to a variable and reuse it.
## 2024-05-23 - [Optimization Surprise]
**Learning:** Python's  can be faster than  for simple sanitization tasks where the characters to be removed are rare. In this specific case,  was ~2x slower than iterative  calls.
**Action:** Always benchmark micro-optimizations. Don't assume standard library 'optimized' methods are always faster for every workload.
## 2024-05-23 - [Optimization Surprise]
**Learning:** Python's str.replace can be faster than str.translate for simple sanitization tasks where the characters to be removed are rare. In this specific case, str.translate was ~2x slower than iterative replace calls.
**Action:** Always benchmark micro-optimizations. Don't assume standard library 'optimized' methods are always faster for every workload.
## 2024-05-23 - [Sanitization Optimization Surprise]
**Learning:** `str.translate` is not always faster than multiple `str.replace` calls.
**Action:** Always benchmark specific use cases. In this project, `sanitize_string` with iterative `replace` (11 chars) was ~2x faster than `translate` for short strings. This counter-intuitive result prevented a "optimization" that would have been a regression.
## 2026-02-01 - Inline Math vs Functions
**Learning:** In tight loops like `haversine`, replacing `map(radians, ...)` and `sin(...)**2` with inline multiplication and squaring provided a ~2x speedup.
**Action:** Prefer inline arithmetic over helper functions or high-level abstractions in critical math paths.
