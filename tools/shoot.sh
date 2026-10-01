#!/usr/bin/env bash
# Renders every key screen of the prototype for the critic.
# Usage: bash tools/shoot.sh <iteration-number>
# Selectors must match exactly one element (browse rule).
# Needs gstack browse (~/.claude/skills/gstack/browse/dist/browse).
set -u
N="${1:?iteration number}"
B="$HOME/.claude/skills/gstack/browse/dist/browse"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/04_prototype/screenshots/iter-$N"
mkdir -p "$OUT"
URL="file:///C:/Users/USUARIO/OneDrive/Documents/Claude%20apps/UNI%20SHORES/FINAL%20PROJECT/Kids%20App/04_prototype/index.html"
AUDIT="$(cat "$ROOT/tools/audit.js")"
# Every shot also checks that the app hasn't scrolled (hidden layers leaking into view).
shot() {
  $B screenshot --selector .device "$OUT/$1.png" >/dev/null
  local sc; sc=$($B js "document.querySelector('#app').scrollTop + document.scrollingElement.scrollTop" | tr -dc '0-9')
  if [ "${sc:-0}" != "0" ]; then echo "  $1   !! APP SCROLLED ($sc px): hidden layers visible"; else echo "  $1"; fi
}
audit() { echo "  audit $1: $($B js "$AUDIT")"; }
pause() { sleep "${1:-0.7}"; }

$B viewport 1280x900 >/dev/null
$B goto "$URL" >/dev/null
$B js "localStorage.clear()" >/dev/null
$B reload >/dev/null; pause 2.5
$B screenshot "$OUT/00-desktop.png" >/dev/null; echo "  00-desktop"
shot 01-hello
$B click "#goBtn" >/dev/null; pause
shot 02-edad
audit edad
$B click "[data-age='10']" >/dev/null; pause 0.3
$B click "[data-onb-next]" >/dev/null; pause
$B click ".opts .opt:first-child" >/dev/null; pause 0.3
shot 03-barrio
$B click "[data-onb-next]" >/dev/null; pause
$B click "[data-gusto='futbol']" >/dev/null; $B click "[data-gusto='musica']" >/dev/null; pause 0.3
shot 04-gustos
$B click "[data-onb-next]" >/dev/null; pause
$B fill "#gPhone" "1234567" >/dev/null; $B click "[data-guardian]" >/dev/null; pause 0.3
shot 05-adulto-error
$B fill "#gPhone" "12345678" >/dev/null; $B click "[data-guardian]" >/dev/null; pause 3
shot 06-mapa
audit mapa
$B click "#cards .card:first-child" >/dev/null; pause 1
shot 07-ficha
audit ficha
$B click "#sheet [data-route]" >/dev/null; pause 1.8
shot 07b-ruta
$B click "[data-route-done]" >/dev/null; pause 0.5
$B click "#cards .card:first-child" >/dev/null; pause 1
$B click "#sheet [data-checkin]" >/dev/null; pause
shot 08-bloqueo-adulto
$B click ".presenter [data-demo='guardian']" >/dev/null; pause
shot 08b-vista-adulto
$B click "[data-g-approve]" >/dev/null; pause
$B click "#cards .card:first-child" >/dev/null; pause 0.9
$B click "#sheet [data-checkin]" >/dev/null; pause
shot 09-escanear
$B click "[data-tap]" >/dev/null; pause
shot 09b-ubicacion-una-vez
$B press Escape >/dev/null; pause
$B click "#cards .card:first-child" >/dev/null; pause 0.9
$B click "#sheet [data-checkin]" >/dev/null; pause
$B click "[data-scan]" >/dev/null; pause 1.2
shot 10-sticker
$B click "[data-rate]" >/dev/null; pause
$B click "[data-face='2']" >/dev/null; $B click "[data-falta]:first-child" >/dev/null; $B click "[data-safe]:first-child" >/dev/null; pause 0.3
shot 11-calificar
audit calificar
$B click "[data-send]" >/dev/null; pause
shot 12-gracias
$B press Escape >/dev/null; pause
$B click "[data-wish]" >/dev/null; pause
$B click "[data-w='patin']" >/dev/null; $B click "[data-w='musica']" >/dev/null; pause 0.3
shot 12b-deseo
$B click "[data-wish-send]" >/dev/null; pause 0.4
$B click ".nav [data-view='agenda']" >/dev/null; pause
shot 13-agenda
$B click ".nav [data-view='album']" >/dev/null; pause
shot 14-album
$B click ".nav [data-view='yo']" >/dev/null; pause
shot 15-yo
audit yo
$B click "#helpBtn" >/dev/null; pause
shot 16-ayuda
audit ayuda
$B press Escape >/dev/null; pause
$B click ".presenter [data-demo-mode='night']" >/dev/null
$B click ".nav [data-view='map']" >/dev/null; pause 3
shot 17-noche-mapa
audit noche-mapa
$B click "#cards .card:first-child" >/dev/null; pause 1
$B click "#sheet [data-going]" >/dev/null; pause 0.3
shot 18-noche-ficha
$B click "#sheet [data-checkin]" >/dev/null; pause; $B click "[data-scan]" >/dev/null; pause 1.2
shot 18c-noche-checkin
$B click "[data-rate]" >/dev/null; pause
shot 18d-noche-calificar
$B press Escape >/dev/null; pause
$B click ".nav [data-view='album']" >/dev/null; pause
shot 18e-noche-lugares
$B click ".nav [data-view='yo']" >/dev/null; pause
shot 18b-noche-yo
audit noche-yo
$B click ".nav [data-view='map']" >/dev/null; pause
$B click ".presenter [data-demo='planner']" >/dev/null; pause
$B screenshot "$OUT/19-municipio.png" >/dev/null; echo "  19-municipio"
$B click "[data-close-planner]" >/dev/null
$B viewport 360x740 >/dev/null; $B reload >/dev/null; pause 2.5
$B screenshot "$OUT/20-movil-360.png" >/dev/null; echo "  20-movil-360"
$B viewport 390x844 >/dev/null; $B goto "$URL?offline=1" >/dev/null; pause 4
$B screenshot "$OUT/21-sin-internet.png" >/dev/null; echo "  21-sin-internet"
echo "console:"; $B console --errors
$B viewport 1280x900 >/dev/null
