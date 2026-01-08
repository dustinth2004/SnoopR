## 2024-05-22 - Unexpected Performance of str.translate
**Learning:** In this environment/codebase, iterative `str.replace` was found to be faster (~3x) than `str.translate` for the specific string sanitization task. This might be due to the overhead of creating the translation table or the nature of the strings being processed.
**Action:** When optimizing string manipulation, always benchmark `str.translate` vs `str.replace` rather than assuming `translate` is faster.

## 2024-05-22 - Optimizing Lookup Lists
**Learning:** `known_drone_mac_prefixes` was implemented as a list with an iterative substring check (`any(x in y for x in list)`). Since the prefix length matches the slice length, this is effectively an equality check. Converting to a set and using O(1) lookup yielded ~2x speedup in microbenchmarks.
**Action:** Always check if iterative list lookups can be replaced with set lookups when matching fixed-length keys.
