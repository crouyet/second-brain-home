#!/usr/bin/env bash
# Instala el LaunchAgent del bot (correr DESPUÉS de completar ~/.hestia/telegram.env).
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$DIR/../.." && pwd)"
PLIST="$HOME/Library/LaunchAgents/com.hestia.bot.plist"

[ -f "$HOME/.hestia/telegram.env" ] || { echo "Primero completá ~/.hestia/telegram.env (ver SETUP.md)"; exit 1; }

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.hestia"
sed -e "s|__VAULT_REPO__|$REPO|g" -e "s|__HOME__|$HOME|g" "$DIR/com.hestia.bot.plist" > "$PLIST"

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✓ hestia-bot corriendo (launchctl list | grep hestia para verificar)"
echo "Log: ~/.hestia/bot.log"
