#!/usr/bin/env bash
# Usage: ./new-project.sh <notes|paper> <name>   — copies templates/<type>/ into a new folder
set -euo pipefail
cd "$(dirname "$0")"
[ $# -eq 2 ] || { echo "Usage: $0 <notes|paper> <name>"; exit 1; }
[ -d "templates/$1" ] || { echo "No template '$1'. Available: $(ls templates | tr '\n' ' ')"; exit 1; }
[ -e "$2" ] && { echo "$2 already exists"; exit 1; }
cp -r "templates/$1" "$2"
echo "Created $2/ from templates/$1"

