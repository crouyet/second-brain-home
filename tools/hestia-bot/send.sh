#!/usr/bin/env bash
# Manda un mensaje de Hestia a la usuaria por Telegram. Uso:
#   send.sh "texto del mensaje"
#   send.sh --with-checkin "mensaje de la mañana"   (3 botones de energía 🪫🔋⚡)
#   send.sh --with-mood "mensaje de la noche"        (6 botones de mood, callback_data mood:*)
set -euo pipefail

ENV_FILE="$HOME/.hestia/telegram.env"
[ -f "$ENV_FILE" ] || { echo "Falta $ENV_FILE (ver SETUP.md)" >&2; exit 1; }
# shellcheck disable=SC1090
source "$ENV_FILE"

KEYBOARD=""
if [ "${1:-}" = "--with-checkin" ]; then
  KEYBOARD='{"inline_keyboard":[[{"text":"🪫 baja","callback_data":"baja"},{"text":"🔋 media","callback_data":"media"},{"text":"⚡️ alta","callback_data":"alta"}]]}'
  shift
elif [ "${1:-}" = "--with-mood" ]; then
  KEYBOARD='{"inline_keyboard":[[{"text":"😄 Amazing","callback_data":"mood:Amazing"},{"text":"🙂 Good","callback_data":"mood:Good"},{"text":"😐 Neutral","callback_data":"mood:Neutral"}],[{"text":"😮‍💨 Heavy","callback_data":"mood:Heavy"},{"text":"😠 Angry","callback_data":"mood:Angry"},{"text":"😔 Sad","callback_data":"mood:Sad"}]]}'
  shift
fi

TEXT="${1:?falta el texto}"

ARGS=(--data-urlencode "chat_id=${CHAT_ID}" --data-urlencode "text=${TEXT}")
[ -n "$KEYBOARD" ] && ARGS+=(--data-urlencode "reply_markup=${KEYBOARD}")

curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" "${ARGS[@]}" >/dev/null
