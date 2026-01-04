## 2026-01-04 - Optimize SnoopR.py Device Extraction
**Learning:** `str.replace` in a loop was faster than `str.translate` for the specific sanitization required in this Python environment.
**Action:** When optimizing string operations, verify assumptions with benchmarks, as theoretical big-O benefits might be outweighed by implementation overhead for small datasets or specific patterns. Also, reducing redundant function calls and dictionary lookups in tight loops (like `extract_device_detections`) yields measurable improvements.
