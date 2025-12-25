## 2025-12-25 - Performance Optimizations in SnoopR.py

**Learning:**
A significant performance gain (77% in benchmark) was achieved by converting a list of MAC prefixes to a set for O(1) lookup in the `is_drone` function.
A minor but "free" optimization was achieved by moving the list of characters to remove in `sanitize_string` to a global constant, avoiding repeated allocation.
Redundant substring checks in `known_drone_ssids` were removed (e.g. "DJI" covers "DJI-Mavic"), simplifying the loop.

**Action:**
When optimizing Python detection loops:
1. Always prefer `set` lookups over list iteration for existence checks.
2. Avoid re-creating constant lists/objects inside frequently called functions.
3. Simplify substring match lists by removing specific items covered by broader terms.
4. Be careful with mixed types (datetime vs timestamp) when collecting data from different sources into a single list for sorting.
