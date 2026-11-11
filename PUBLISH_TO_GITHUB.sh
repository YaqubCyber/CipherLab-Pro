#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/YaqubCyber/CipherLab-Pro.git"
BRANCH="main"

printf '\n=== CipherLab Pro: publish final project ===\n'
printf 'Target repository: %s\n' "$REPO_URL"
printf 'Target branch: %s\n\n' "$BRANCH"

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: Git is not installed or Git Bash cannot find it."
  exit 1
fi

if [ -e .git ]; then
  echo "ERROR: This folder already contains .git."
  echo "For safety, run this script only from the freshly extracted CipherLab-Pro folder."
  exit 1
fi

if [ ! -f main.py ] || [ ! -f README.md ]; then
  echo "ERROR: main.py or README.md is missing. Open Git Bash in the project root folder."
  exit 1
fi

printf '1/5 Initializing Git in this fresh project folder...\n'
git init -b "$BRANCH"

git config user.name "Yaqub Ismail Solan"
git config user.email "yaqubsolan111@damil.com"

printf '\n2/5 Connecting to your existing GitHub repository...\n'
git remote add origin "$REPO_URL"

printf '\n3/5 Fetching the existing repository history (without downloading its old working files)...\n'
git fetch origin

if ! git show-ref --verify --quiet "refs/remotes/origin/$BRANCH"; then
  echo "ERROR: The remote branch '$BRANCH' was not found."
  echo "Check the repository default branch on GitHub before continuing."
  exit 1
fi

printf '\n4/5 Preparing the final project as a new commit on the existing history...\n'
# Move the new local branch to the current GitHub commit without checking out
# or restoring the old files; keep this fresh package's working files intact.
git reset --mixed "origin/$BRANCH"
git add -A

if git diff --cached --quiet; then
  echo "No file differences found; the GitHub repository already matches this package."
else
  git commit -m "Release 1.0.0: finalize CipherLab Pro"
fi

printf '\n5/5 Pushing to the existing GitHub repository...\n'
git push -u origin "$BRANCH"

printf '\nSUCCESS: CipherLab Pro has been pushed to %s\n' "$REPO_URL"
printf 'Open: https://github.com/YaqubCyber/CipherLab-Pro\n'
