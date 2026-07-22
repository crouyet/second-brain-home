#!/usr/bin/env bash
# Instala el LaunchAgent del health-receiver.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$DIR/../.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/com.hestia.health-receiver.plist"

[ -f "$HOME/.hestia/health-receiver.env" ] || { echo "Falta ~/.hestia/health-receiver.env"; exit 1; }

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.hestia"
sed -e "s|__VAULT_REPO__|$REPO|g" -e "s|__HOME__|$HOME|g" "$DIR/com.hestia.health-receiver.plist" > "$PLIST"

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✓ health-receiver corriendo (puerto $(grep PORT "$HOME/.hestia/health-receiver.env" | cut -d= -f2))"
echo "Log: ~/.hestia/health-receiver.log"
