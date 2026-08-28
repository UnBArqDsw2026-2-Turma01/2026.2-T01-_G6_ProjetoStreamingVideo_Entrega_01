"""Especificações dos diagramas BPMN da SubEquipe_01.

Estes sete módulos (D0-D5) são o bloco Performance/Latência — um dos 4 blocos
em que a subequipe dividiu o FOCO_02, um por NFR (ver
docs/Base/Relatorios/1.1.1.SubEquipe_01/3.EngenhariaReversa.md §0). A ordem de
TODOS é a ordem de leitura recomendada na documentação: o modelo integrador
primeiro, depois o pipeline de produção, o fluxo mínimo do foco e os processos
chamados por ele.

Um novo bloco (Usabilidade/Interatividade, Confiabilidade/Disponibilidade,
Segurança) cria seus próprios módulos neste mesmo diretório, com o prefixo de
letra do seu bloco (U, C, S — ver tools/README.md) em vez de D, e os importa e
lista aqui, ao lado de TODOS, sem misturar os IDs com os deste bloco.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from d0_cadeia import D0  # noqa: E402
from d1_ingestao import D1  # noqa: E402
from d2_assistir import D2  # noqa: E402
from d2b_ciclo import D2B  # noqa: E402
from d3_abr import D3  # noqa: E402
from d4_recuperacao import D4  # noqa: E402
from d5_tempo_real import D5  # noqa: E402

TODOS = [D0, D1, D2, D2B, D3, D4, D5]
