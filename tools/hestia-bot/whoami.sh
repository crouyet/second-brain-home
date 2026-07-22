#!/usr/bin/env bash
# Muestra el chat_id de quien le escribió al bot (para completar CHAT_ID en el env).
# Uso: TELEGRAM_TOKEN=123:ABC ./whoami.sh   (o con el env ya parcialmente completo)
set -euo pipefail
[ -z "${TELEGRAM_TOKEN:-}" ] && source "$HOME/.hestia/telegram.env"
curl -sS "https://api.telegram.org/bot${TELEGRAM_TOKEN}/getUpdates" |
  python3 -c "import json,sys; [print('chat_id:', m['message']['chat']['id'], '—', m['message']['chat'].get('first_name','')) for m in json.load(sys.stdin)['result'] if 'message' in m]" |
  sort -u
