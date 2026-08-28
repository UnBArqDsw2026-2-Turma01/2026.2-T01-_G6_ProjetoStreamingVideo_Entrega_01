#!/usr/bin/env bash
# Coleta reprodutível das evidências do FOCO_02 (SubEquipe_01).
#
# Repete, fora do navegador, exatamente as requisições que o player da aplicação
# de referência faz sozinho ao abrir um canal ao vivo — as mesmas que aparecem na
# aba Network do DevTools. Nada aqui contorna autenticação, paywall ou proteção:
# são requisições públicas, feitas sem sessão, no volume de uma sessão de leitura.
#
# Os endereços NÃO ficam no repositório (diretriz: não nomear a fonte de
# inspiração). Copie `alvo.env.exemplo` para `alvo.env`, preencha, e rode:
#
#     ./tools/engenharia-reversa/coletar.sh <canal> <diretorio-de-saida>
#
# O diretório de saída É OBRIGATÓRIO: a SubEquipe_01 dividiu este foco em 4
# blocos, um por NFR (ver 3.EngenhariaReversa.md §0). Cada membro roda a coleta
# para a sua própria subpasta, para não sobrescrever a evidência de outro:
#
#     .../subequipe_01/performance-latencia         (Performance/Latência)
#     .../subequipe_01/usabilidade-interatividade    (Usabilidade/Interatividade)
#     .../subequipe_01/confiabilidade-disponibilidade (Confiabilidade/Disponibilidade)
#     .../subequipe_01/seguranca                     (Segurança)
#
# Saída: capturas brutas em `saida/bruto/` e versões anonimizadas em `saida/`.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONF="$RAIZ/tools/engenharia-reversa/alvo.env"
CANAL="${1:?uso: coletar.sh <canal> <diretorio-de-saida> — ver os 4 blocos no cabeçalho deste script}"
SAIDA="${2:?uso: coletar.sh <canal> <diretorio-de-saida> — sem padrão, para não sobrescrever a evidência de outro membro}"
BRUTO="$SAIDA/bruto"

if [ ! -f "$CONF" ]; then
  echo "falta $CONF — copie alvo.env.exemplo e preencha os endereços" >&2
  exit 1
fi
# shellcheck source=/dev/null
set -a; . "$CONF"; set +a   # exporta também as marcas usadas na anonimização
: "${GQL_URL:?defina GQL_URL em alvo.env}"
: "${USHER_URL:?defina USHER_URL em alvo.env}"
: "${CLIENT_ID:?defina CLIENT_ID em alvo.env}"
: "${QUERY_HASH:?defina QUERY_HASH em alvo.env}"

mkdir -p "$BRUTO"
FMT='http=%{http_code} versao=%{http_version} dns=%{time_namelookup} tcp=%{time_connect}'
FMT="$FMT tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total} bytes=%{size_download}\n"

echo "== 1/5 token de reprodução =="
curl -sS -o "$BRUTO/ev01-token.json" -w "$FMT" "$GQL_URL" \
  -H "Client-Id: $CLIENT_ID" \
  -H 'Content-Type: text/plain;charset=UTF-8' \
  --data-raw "{\"operationName\":\"PlaybackAccessToken\",\"variables\":{\"isLive\":true,\"login\":\"$CANAL\",\"isVod\":false,\"vodID\":\"\",\"playerType\":\"site\",\"platform\":\"web\"},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"$QUERY_HASH\"}}}" \
  | tee "$BRUTO/ev04-tempos.txt"

echo "== 2/5 manifesto mestre =="
python3 "$RAIZ/tools/engenharia-reversa/montar_url.py" \
  "$BRUTO/ev01-token.json" "$USHER_URL" "$CANAL" > "$BRUTO/usher-url.txt"
curl -sS -D "$BRUTO/ev02-cabecalhos.txt" -o "$BRUTO/ev02-manifesto-mestre.m3u8" \
  -w "$FMT" "$(cat "$BRUTO/usher-url.txt")" | tee -a "$BRUTO/ev04-tempos.txt"

echo "== 3/5 manifesto de mídia e segmento =="
python3 "$RAIZ/tools/engenharia-reversa/medir_playlist.py" \
  "$BRUTO/ev02-manifesto-mestre.m3u8" "$BRUTO"

echo "== 4/5 anonimização =="
for f in "$BRUTO"/ev0*; do
  base="$(basename "$f")"
  python3 "$RAIZ/tools/engenharia-reversa/anonimizar.py" "$f" "$SAIDA/$base"
done

echo "== 5/5 pronto =="
echo "bruto (NÃO versionar): $BRUTO"
echo "anonimizado (versionar): $SAIDA"
