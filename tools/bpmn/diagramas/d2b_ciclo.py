"""D2b — Ciclo de Reprodução por Segmento (expansão do subprocesso de D2).

É aqui que a latência do fluxo "assistir ao vivo" é gasta e recuperada: o
manifesto de mídia é rebaixado a cada volta, o segmento é buscado na borda e
o buffer é realimentado. Todas as medições da SubEquipe_01 caem neste ciclo.
"""

from comum import DataFlow, Diagram, F, Lane, MsgFlow, N, Pool, T

L_CTRL, L_TEL = "d2b_l_ctrl", "d2b_l_tel"
L_EDGE, L_ORIG = "d2b_l_edge", "d2b_l_orig"

D2B = Diagram(
    id="D2b",
    name="Ciclo de Reprodução por Segmento",
    arquivo="subequipe_01_bpmn-d2b-ciclo-reproducao.bpmn",
    descricao="Expansão do subprocesso de estado estacionário de D2.",
    pools=[
        Pool("d2b_p_player", "Player de vídeo (expansão do subprocesso de D2)",
             "d2b_proc_player", [
                 Lane(L_CTRL, "Controle do ciclo"),
                 Lane(L_TEL, "Telemetria"),
             ]),
        Pool("d2b_p_man", "Plataforma — serviço de manifesto de mídia", "d2b_proc_man"),
        Pool("d2b_p_cdn", "Rede de distribuição (CDN)", "d2b_proc_cdn", [
            Lane(L_EDGE, "PoP de borda"),
            Lane(L_ORIG, "Origem / origin shield"),
        ]),
    ],
    nodes=[
        # ---------------- Controle do ciclo ----------------
        N("d2b_start", "start", "Ciclo iniciado com a qualidade escolhida", L_CTRL, 0, 0),
        N("d2b_pl", "service", "Baixar o manifesto de mídia da qualidade corrente",
          L_CTRL, 1, 0),
        N("d2b_gwe", "eventgw", "O que ocorrer primeiro", L_CTRL, 2, 0),
        N("d2b_c_seg", "catch", "Manifesto traz segmento novo", L_CTRL, 3, 0,
          trigger="conditional"),
        N("d2b_c_to", "catch", "Sem segmento novo por 3× a duração-alvo", L_CTRL, 3, 1.5,
          trigger="timer", timer="PT6S"),
        N("d2b_c_down", "catch", "Fim de transmissão anunciado", L_CTRL, 3, 2.8,
          trigger="message", ref="Fim de transmissão anunciado"),
        N("d2b_seg", "service", "Baixar o próximo segmento de ~2 s", L_CTRL, 4, 0),
        N("d2b_b_slow", "boundary", "Download passa de 2 s", L_CTRL, 0, 0,
          trigger="timer", timer="PT2S", attached_to="d2b_seg", interrupting=False),
        N("d2b_b_err", "boundary", "Erro ao baixar o segmento", L_CTRL, 0, 0,
          trigger="error", ref="Falha ao baixar segmento", attached_to="d2b_seg",
          label_dy=46),
        N("d2b_append", "service", "Anexar ao buffer de mídia do navegador", L_CTRL, 5, 0),
        N("d2b_gwbuf", "xor", "Buffer acima do alvo?", L_CTRL, 6, 0),
        N("d2b_abr", "call", "Avaliar troca de qualidade (ver D3)", L_CTRL, 7, 0,
          called="d3_proc_abr"),
        N("d2b_refill", "task", "Pausar e reencher o buffer (travamento visível)",
          L_CTRL, 7, 1.5),
        N("d2b_wait", "catch", "Aguardar ~1 duração de segmento", L_CTRL, 8, 0,
          trigger="timer", timer="PT2S"),
        N("d2b_gwtok", "xor", "Token ainda válido?", L_CTRL, 9, 0),
        N("d2b_renew", "service", "Renovar o token de reprodução", L_CTRL, 9, 1.5),
        N("d2b_rec", "call", "Recuperar reprodução (ver D4)", L_CTRL, 4.4, 1.5,
          called="d4_proc_player"),
        N("d2b_gwrec", "xor", "Reprodução retomada?", L_CTRL, 5.6, 1.5),
        N("d2b_endfail", "end", "Encerrar com falha", L_CTRL, 6.6, 1.5,
          trigger="escalation", ref="Reprodução não recuperada"),
        N("d2b_endoff", "end", "Encerrar o ciclo: canal fora do ar", L_CTRL, 4.4, 2.8),
        N("d2b_d_seg", "data", "Segmento de ~2 s", L_CTRL, 6.2, 2.8),

        # ---------------- Telemetria ----------------
        N("d2b_tel", "service", "Registrar risco de esgotamento do buffer", L_TEL, 5, 0),
        N("d2b_tel_end", "end", "Telemetria enviada", L_TEL, 6, 0),

        # ---------------- Serviço de manifesto ----------------
        N("d2b_m_start", "start", "Pedido de manifesto de mídia", "d2b_p_man", 1, 0,
          trigger="message", ref="Pedido de manifesto de mídia"),
        N("d2b_m_build", "service", "Montar a janela deslizante e as marcações da sessão",
          "d2b_p_man", 2, 0),
        N("d2b_m_end", "end", "Manifesto de mídia devolvido", "d2b_p_man", 3, 0,
          trigger="message", ref="Manifesto de mídia"),

        # ---------------- CDN ----------------
        N("d2b_c_start", "start", "Pedido de segmento", L_EDGE, 4, 0, trigger="message",
          ref="Pedido de segmento"),
        N("d2b_c_gw", "xor", "Segmento já está na borda?", L_EDGE, 5, 0),
        N("d2b_c_hit", "service", "Servir do cache da borda", L_EDGE, 6, 0),
        N("d2b_c_miss", "service", "Buscar o segmento na camada de origem", L_EDGE, 6, 1.5),
        N("d2b_c_store", "service", "Guardar o segmento na borda", L_EDGE, 8, 1.5),
        N("d2b_c_join", "xor", "Entregar", L_EDGE, 9, 0),
        N("d2b_c_end", "end", "Segmento entregue ao player", L_EDGE, 10, 0,
          trigger="message", ref="Segmento"),
        N("d2b_ds_cache", "datastore", "Cache do PoP de borda", L_EDGE, 5, 1.5),
        N("d2b_o_fetch", "service", "Ler o segmento da origem protegida", L_ORIG, 7, 0),
    ],
    flows=[
        F("d2b_start", "d2b_pl"),
        F("d2b_pl", "d2b_gwe"),
        F("d2b_gwe", "d2b_c_seg"),
        F("d2b_gwe", "d2b_c_to"),
        F("d2b_gwe", "d2b_c_down"),
        F("d2b_c_seg", "d2b_seg"),
        F("d2b_seg", "d2b_append"),
        F("d2b_append", "d2b_gwbuf"),
        F("d2b_gwbuf", "d2b_abr", "sim", condition=True),
        F("d2b_gwbuf", "d2b_refill", "não", condition=True, waypoints="v"),
        F("d2b_refill", "d2b_wait"),
        F("d2b_abr", "d2b_wait"),
        F("d2b_wait", "d2b_gwtok"),
        F("d2b_gwtok", "d2b_pl", "sim — próxima volta", condition=True, waypoints="loop"),
        F("d2b_gwtok", "d2b_renew", "não", condition=True, waypoints="v"),
        F("d2b_renew", "d2b_pl", "retomar o ciclo", waypoints="loop"),
        F("d2b_c_to", "d2b_rec"),
        F("d2b_b_err", "d2b_rec"),
        F("d2b_rec", "d2b_gwrec"),
        F("d2b_gwrec", "d2b_pl", "sim", condition=True, waypoints="loop"),
        F("d2b_gwrec", "d2b_endfail", "não", condition=True),
        F("d2b_c_down", "d2b_endoff"),
        F("d2b_b_slow", "d2b_tel"),
        F("d2b_tel", "d2b_tel_end"),

        F("d2b_m_start", "d2b_m_build"),
        F("d2b_m_build", "d2b_m_end"),

        F("d2b_c_start", "d2b_c_gw"),
        F("d2b_c_gw", "d2b_c_hit", "sim", condition=True),
        F("d2b_c_gw", "d2b_c_miss", "não", condition=True, waypoints="v"),
        F("d2b_c_miss", "d2b_o_fetch"),
        F("d2b_o_fetch", "d2b_c_store"),
        F("d2b_c_store", "d2b_c_join"),
        F("d2b_c_hit", "d2b_c_join"),
        F("d2b_c_join", "d2b_c_end"),
    ],
    msgflows=[
        MsgFlow("d2b_pl", "d2b_m_start", "pedido de manifesto"),
        MsgFlow("d2b_m_end", "d2b_pl", "janela de segmentos"),
        MsgFlow("d2b_seg", "d2b_c_start", "pedido de segmento"),
        MsgFlow("d2b_c_end", "d2b_seg", "bytes do segmento"),
    ],
    dataflows=[
        DataFlow("d2b_seg", "d2b_d_seg", "out"),
        DataFlow("d2b_append", "d2b_d_seg", "in"),
        DataFlow("d2b_c_hit", "d2b_ds_cache", "in"),
        DataFlow("d2b_c_store", "d2b_ds_cache", "out"),
    ],
    notes=[
        T("d2b_n1",
          "Medição por amostragem a cada 2 s (EV-05): a cada volta entra exatamente 1 "
          "segmento novo, e a janela tem 16 segmentos (~32 s). O atraso entre o fim do "
          "segmento mais novo e o relógio do cliente ficou entre 1,46 s e 2,37 s.",
          "d2b_pl", L_CTRL, 1, 4.1),
        T("d2b_n2",
          "Medição (EV-04): 859.724 B em 0,266 s, ~26 Mbit/s contra 3,42 Mbit/s "
          "declarados para a faixa. Baixar leva ~13% da duração do segmento — a folga "
          "que sustenta o buffer.",
          "d2b_seg", L_CTRL, 3.4, 4.1),
        T("d2b_n3",
          "Buffer observado no player: 4,1 s a 5,0 s à frente do ponto exibido (EV-05). "
          "Somado ao atraso do manifesto, dá a ordem de 6 a 8 s entre o segmento existir "
          "e o espectador vê-lo.",
          "d2b_gwbuf", L_CTRL, 5.8, 4.1),
        T("d2b_n4",
          "O manifesto de mídia veio com cabeçalho de não-cache e marcado como privado "
          "(EV-03): ele é montado por sessão porque carrega as marcações de anúncio. "
          "Trade-off central: personalizar o manifesto impede cacheá-lo, e cada player "
          "volta à plataforma a cada ~2 s.",
          "d2b_m_build", "d2b_p_man", 2, 1),
        T("d2b_n5",
          "Os segmentos, ao contrário, são cacheáveis e foram servidos da borda com "
          "acerto de cache e idade de 2 s a 26 s (EV-04) — é a parte do tráfego que "
          "escala com a audiência sem tocar a origem.",
          "d2b_c_hit", L_EDGE, 6.4, 2.8),
        T("d2b_n6",
          "Descer a qualidade é ação preventiva; reencher o buffer já é a falha "
          "percebida. Todo o ramo superior existe para que este ramo inferior "
          "não seja alcançado.",
          "d2b_refill", L_CTRL, 8.2, 4.1),
    ],
)
