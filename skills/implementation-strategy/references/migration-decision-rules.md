# Migration decision rules

Prefer direct rewrite unless at least one is true:
1. a released consumer depends on the old shape
2. durable external data already exists in that shape
3. the user explicitly asked for backward compatibility or deprecation support

If none of the above are true, do not add shims just because the old shape exists on the current branch.
