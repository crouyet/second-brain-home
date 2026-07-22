#!/usr/bin/env bash
# Reproduce una playlist de Spotify por AppleScript. Uso:
#   play_playlist.sh spotify:playlist:6wR8aHRRetV3pTxc62m2Ly
set -euo pipefail
URI="${1:?falta el spotify:playlist:ID}"
osascript -e "tell application \"Spotify\" to activate" \
          -e "tell application \"Spotify\" to play track \"${URI}\""
