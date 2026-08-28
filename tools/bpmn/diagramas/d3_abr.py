"""D3 — Adaptar a Qualidade durante a Exibição (ABR).

Fluxo extra da SubEquipe_01, chamado por D2b a cada segmento anexado.
O algoritmo real é caixa-preta (FE03 do escopo); o que se modela aqui são as
ENTRADAS observáveis da decisão e o efeito observável dela, não a regra interna.
"""

from comum import Diagram, F, N, Pool, T

D3 = Diagram(
    id="D3",
    name="Adaptar a Qualidade durante a Exibição",
    arquivo="subequipe_01_bpmn-d3-adaptacao-qualidade.bpmn",
    descricao="Decisão de troca de faixa de qualidade a cada segmento.",
    pools=[
        Pool("d3_p_abr", "Player — adaptação de qualidade", "d3_proc_abr"),
    ],
    nodes=[
        N("d3_start", "start", "Segmento anexado ao buffer", "d3_p_abr", 0, 0),
        N("d3_split", "and", "Coletar as entradas da decisão", "d3_p_abr", 1, 0),
        N("d3_m_thr", "service", "Medir a taxa de transferência do último segmento",
          "d3_p_abr", 2, 0),
        N("d3_m_buf", "service", "Medir a ocupação do buffer", "d3_p_abr", 2, 1),
        N("d3_m_view", "service", "Observar o tamanho de exibição do player", "d3_p_abr", 2, 2),
        N("d3_join", "and", "Consolidar", "d3_p_abr", 3, 0),
        N("d3_est", "rule", "Estimar a maior faixa sustentável", "d3_p_abr", 4, 0),
        N("d3_gw1", "xor", "Faixa alvo difere da atual?", "d3_p_abr", 5, 0),
        N("d3_keep", "end", "Manter a faixa atual", "d3_p_abr", 5, 1),
        N("d3_gw2", "xor", "Subir ou descer?", "d3_p_abr", 6, 0),
        N("d3_down", "service", "Descer de faixa imediatamente", "d3_p_abr", 7, 1),
        N("d3_hold", "service", "Aguardar N segmentos estáveis antes de subir", "d3_p_abr", 7, 0),
        N("d3_gw3", "xor", "Continua estável?", "d3_p_abr", 8, 0),
        N("d3_up", "service", "Subir uma faixa", "d3_p_abr", 9, 0),
        N("d3_apply", "service", "Aplicar a troca na próxima fronteira de segmento",
          "d3_p_abr", 10, 0),
        N("d3_end", "end", "Qualidade ajustada", "d3_p_abr", 11, 0),
        N("d3_abort", "end", "Desistir da subida", "d3_p_abr", 8, 2),
    ],
    flows=[
        F("d3_start", "d3_split"),
        F("d3_split", "d3_m_thr"),
        F("d3_split", "d3_m_buf"),
        F("d3_split", "d3_m_view"),
        F("d3_m_thr", "d3_join"),
        F("d3_m_buf", "d3_join"),
        F("d3_m_view", "d3_join"),
        F("d3_join", "d3_est"),
        F("d3_est", "d3_gw1"),
        F("d3_gw1", "d3_keep", "não", condition=True),
        F("d3_gw1", "d3_gw2", "sim", condition=True),
        F("d3_gw2", "d3_hold", "subir", condition=True),
        F("d3_gw2", "d3_down", "descer", condition=True),
        F("d3_hold", "d3_gw3"),
        F("d3_gw3", "d3_up", "sim", condition=True),
        F("d3_gw3", "d3_abort", "não", condition=True),
        F("d3_up", "d3_apply"),
        F("d3_down", "d3_apply"),
        F("d3_apply", "d3_end"),
    ],
    notes=[
        T("d3_n1",
          "Medição (EV-04): segmento de 720p60 com 859.724 B em 0,266 s ≈ 26 Mbit/s, "
          "contra 3,42 Mbit/s declarados para a faixa — margem de cerca de 7×.",
          "d3_m_thr", "d3_p_abr", 2, 3),
        T("d3_n2",
          "Buffer observado: 4,1 s a 5,0 s à frente do ponto exibido (EV-05). É a "
          "reserva que o algoritmo tem para errar sem que o espectador perceba.",
          "d3_m_buf", "d3_p_abr", 4, 3),
        T("d3_n3",
          "Observação de duas sessões distintas (EV-05): em uma delas o player "
          "estabilizou em 720p60 e na outra na fonte 1080p60, com a mesma janela de "
          "exibição de 700x394 CSS. A regra interna é caixa-preta (não-escopo FE03); "
          "o modelo registra as entradas, não o algoritmo.",
          "d3_est", "d3_p_abr", 6.2, 3),
        T("d3_n4",
          "Assimetria deliberada: descer é imediato, subir espera confirmação. Errar "
          "para cima custa travamento; errar para baixo custa só nitidez. É o mesmo "
          "trade-off do SIG entre Baixa Latência e Continuidade (C01).",
          "d3_gw2", "d3_p_abr", 8.4, 3),
        T("d3_n5",
          "A troca só vale na fronteira do próximo segmento, porque cada segmento "
          "começa em quadro-chave: entre decidir e ver o efeito há até uma duração "
          "de segmento (~2 s).",
          "d3_apply", "d3_p_abr", 10.6, 3),
    ],
)
