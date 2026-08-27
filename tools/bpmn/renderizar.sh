#!/usr/bin/env bash
# Renderiza os .bpmn de docs/assets/bpmn/ em PNG usando o próprio bpmn-js
# (a mesma biblioteca do Camunda Modeler / bpmn.io) dentro de um Chromium headless.
#
# O PNG é um *preview* versionado para a documentação; o arquivo-fonte editável
# continua sendo o .bpmn, que abre normalmente no Camunda Modeler.
#
# Requisitos: chromium, node e npm. A primeira execução instala bpmn-js em
# tools/bpmn/.render/ (pasta fora do versionamento).
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ASSETS="$RAIZ/docs/assets/bpmn"
TRAB="$RAIZ/tools/bpmn/.render"
ESCALA="${ESCALA:-1.5}"   # ampliação do PNG sobre o tamanho declarado no DI

# o shell não interativo pode carregar shims do nvm; força os binários do sistema
unset -f node npm npx 2>/dev/null || true
export PATH="/usr/bin:$PATH"

mkdir -p "$TRAB"
if [ ! -d "$TRAB/node_modules/bpmn-js" ]; then
  echo "instalando bpmn-js em $TRAB ..."
  printf '{"name":"render-bpmn","private":true}\n' > "$TRAB/package.json"
  (cd "$TRAB" && npm install --silent bpmn-js@18)
fi

VIEWER="$TRAB/node_modules/bpmn-js/dist/bpmn-navigated-viewer.production.min.js"
CSS="$TRAB/node_modules/bpmn-js/dist/assets/bpmn-js.css"
DIAGRAMA_CSS="$TRAB/node_modules/bpmn-js/dist/assets/diagram-js.css"

for arquivo in "$ASSETS"/*.bpmn; do
  nome="$(basename "$arquivo" .bpmn)"

  # a janela do navegador acompanha a caixa declarada no DI, para que o texto
  # saia do mesmo tamanho em todos os diagramas
  dimensoes="$(python3 "$RAIZ/tools/bpmn/medir_di.py" "$arquivo")"
  largura="${dimensoes% *}"
  altura="${dimensoes#* }"

  python3 "$RAIZ/tools/bpmn/montar_pagina.py" \
    "$arquivo" "$TRAB/$nome.html" "$VIEWER" "$CSS" "$DIAGRAMA_CSS"

  chromium --headless --disable-gpu --hide-scrollbars --no-sandbox \
    --force-device-scale-factor="$ESCALA" \
    --virtual-time-budget=8000 \
    --window-size="$largura,$altura" \
    --screenshot="$ASSETS/$nome.png" \
    "file://$TRAB/$nome.html" >/dev/null 2>&1

  echo "$(basename "$ASSETS/$nome.png")  ${largura}x${altura} css @ ${ESCALA}x"
done
