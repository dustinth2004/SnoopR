## 2024-05-23 - [Optimization Surprise]
**Learning:** Python's  can be faster than  for simple sanitization tasks where the characters to be removed are rare. In this specific case,  was ~2x slower than iterative  calls.
**Action:** Always benchmark micro-optimizations. Don't assume standard library 'optimized' methods are always faster for every workload.
## 2024-05-23 - [Optimization Surprise]
**Learning:** Python's str.replace can be faster than str.translate for simple sanitization tasks where the characters to be removed are rare. In this specific case, str.translate was ~2x slower than iterative replace calls.
**Action:** Always benchmark micro-optimizations. Don't assume standard library 'optimized' methods are always faster for every workload.
