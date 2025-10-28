#!/usr/bin/env bash

# Build script for coiled

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."

cd "$REPO_ROOT"

echo "============================================="
echo "Building coiled"
echo "============================================="
echo ""

check_command() {
    local cmd=$1
    local install_url=$2
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ Error: $cmd is not installed"
        echo "   Install it from: $install_url"
        exit 1
    fi
    echo "   ✓ $cmd found: $($cmd --version | head -n 1)"
}

echo "1. Checking prerequisites..."
check_command uv "https://docs.astral.sh/uv/getting-started/installation/"

check_command pnpm "https://pnpm.io/installation"


echo ""
echo "2. Installing Python dependencies..."
uv sync --frozen


echo ""
echo "3. Installing pnpm packages..."
pnpm install


echo "4. Type checking TypeScript widgets..."
pnpm --filter '@habemus-papadum/coiled-widgets' typecheck


echo "5. Building TypeScript widgets..."
pnpm --filter '@habemus-papadum/coiled-widgets' build:python


echo ""
echo "============================================="
echo "✅ Build complete!"
echo "============================================="
