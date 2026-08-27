#!/usr/bin/env bash
# Wrapper de execução para figuras_devtools.py.
#
# NOTA DE AUTORIA: este script e o gerador Python que ele chama foram escritos
# por assistente de IA generativa nesta sessão, a pedido do membro responsável
# pelo FOCO_02. Dois motivos declarados para existir a ferramenta:
#   1. Evitar publicar captura real do DevTools sobre a plataforma analisada —
#      a diretriz da disciplina proíbe expor a marca da fonte de inspiração
#      (não-escopo FE06). A reconstrução permite ilustrar o processo com os
#      mesmos dados reais, já anonimizados, sem esse risco.
#   2. Baratear a produção do material: regerar as seis figuras após um ajuste
#      de layout custa um comando, não uma nova sessão de captura de tela.
# Uso registrado em docs/Base/Relatorios/1.1.1.SubEquipe_01/5.IAGenerativa.md.
# Os números desenhados vêm sempre de EV-01 a EV-06 — nada é inventado pela IA.
#
# Este script gera as figuras do bloco Performance/Latência (BLOCO_NFR em
# figuras_devtools.py). Para outro bloco da divisão em 4 NFRs da subequipe
# (ver 3.EngenhariaReversa.md §0), copie figuras_devtools.py e este wrapper,
# ajustando o nome e as cenas — não reaproveite este arquivo em execução.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# o shell não interativo pode carregar shims do nvm; sem efeito aqui (o script
# é só Python), mas mantém o mesmo padrão de segurança dos demais scripts
unset -f node npm npx 2>/dev/null || true
export PATH="/usr/bin:$PATH"

python3 "$RAIZ/tools/engenharia-reversa/figuras_devtools.py" "$@"
