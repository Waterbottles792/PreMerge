#!/usr/bin/env bash
# Builds a disposable demo repo and runs every PreMerge feature against it.
# Usage: bash docs/review3/demo.sh [target-dir]
set -e
D="${1:-/tmp/premerge-demo}"
rm -rf "$D"; mkdir -p "$D"; cd "$D"
git init -q -b main
git config user.email demo@premerge.dev; git config user.name "Demo Dev"

# History where auth.py and session.py always change together
for i in 1 2 3 4; do
  echo "def login_v$i(): pass"   > auth.py
  echo "def refresh_v$i(): pass" > session.py
  git add -A; git commit -q -m "auth+session round $i"
done
echo "x = 1" > utils.py; git add -A; git commit -q -m "add utils"

# feature-a and feature-b edit the SAME lines of auth.py  -> direct conflict
git checkout -q -b feature-a main
printf 'def login_v4(): pass\ndef oauth_a(): pass\n' > auth.py; git commit -q -am "feature-a: oauth"
git checkout -q -b feature-b main
printf 'def login_v4(): pass\ndef saml_b(): pass\n' > auth.py;  git commit -q -am "feature-b: saml"

# feature-c touches only auth.py, feature-d only session.py -> HIDDEN coupling
git checkout -q -b feature-c main
printf 'def login_v4(): pass\ndef mfa(): pass\n' > auth.py; git commit -q -am "feature-c: mfa"
git checkout -q -b feature-d main
printf 'def refresh_v4(): pass\ndef ttl(): pass\n' > session.py; git commit -q -am "feature-d: session ttl"

# feature-e touches an unrelated file -> low risk
git checkout -q -b feature-e main
echo "x = 2" > utils.py; git commit -q -am "feature-e: utils"
git checkout -q main
echo "demo repo ready at $D"
