#!/bin/sh
# Pre-push hygiene check.
#
# Blocks pushes that introduce filenames matching prefixes considered
# private (strategy/roadmap/monetization/etc). Generic by design — the
# specifics of what's considered private live outside this repo.
#
# To install:
#   cp scripts/pre-push.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
#
# To bypass once (use sparingly):
#   git push --no-verify
#
# This is a local backstop. Server-side branch protection and operator
# habit (eyeballing `git diff` before push) are the primary defenses.

set -eu

forbidden='(^|/)((STRATEGY|ROADMAP|MONETIZATION|PRICING|PRODUCT_V|PHASE|RETRO|COMPOUND|GROWTH|AUDIENCE|FUNNEL|INTERNAL|PRIVATE|DRAFT|IDEAS|NOTES)_)'

zero='0000000000000000000000000000000000000000'
fail=0

while read local_ref local_sha remote_ref remote_sha; do
    [ "$local_sha" = "$zero" ] && continue

    if [ "$remote_sha" = "$zero" ]; then
        # New branch: check all files reachable from local_sha that
        # aren't on any other ref.
        files=$(git diff --name-only "$local_sha" "$(git rev-list --max-parents=0 "$local_sha" | tail -1)" 2>/dev/null || git ls-tree -r --name-only "$local_sha")
    else
        files=$(git diff --name-only "$remote_sha" "$local_sha")
    fi

    bad=$(echo "$files" | grep -E "$forbidden" || true)
    if [ -n "$bad" ]; then
        echo "ERROR: pre-push: forbidden filename pattern detected:"
        echo "$bad" | sed 's/^/  /'
        echo
        echo "If this is intentional, push with: git push --no-verify"
        fail=1
    fi
done

exit "$fail"
