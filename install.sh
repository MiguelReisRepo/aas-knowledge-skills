#!/usr/bin/env bash
# Symlink every skill in ./skills into a Claude skills directory.
# Usage:
#   ./install.sh                       # -> ~/.claude/skills (user-level, all projects)
#   ./install.sh PATH/.claude/skills   # -> a specific project
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:-$HOME/.claude/skills}"
mkdir -p "$DEST"

for d in "$REPO_DIR"/skills/*/; do
  name="$(basename "$d")"
  target="$DEST/$name"
  if [ -L "$target" ]; then
    rm -f "$target"                       # refresh an existing symlink
  elif [ -e "$target" ]; then
    echo "skip (real dir exists, not overwriting): $target"
    continue
  fi
  ln -s "$REPO_DIR/skills/$name" "$target"
  echo "linked: $target -> $REPO_DIR/skills/$name"
done
