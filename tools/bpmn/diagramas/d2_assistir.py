"""D2 — Assistir Transmissão ao Vivo (fluxo mínimo da SubEquipe_01).

Recorte: da abertura da página do canal até o encerramento da sessão de
reprodução. O ciclo de estado estacionário (baixar manifesto de mídia → baixar
segmento → alimentar o buffer) é um subprocesso recolhido, detalhado em D2b.
"""

from comum import Diagram, F, Lane, MsgFlow, N, Pool, T

L_USER, L_SPA, L_PLAYER = "d2_l_user", "d2_l_spa", "d2_l_player"
L_AUTH, L_WEAVER = "d2_l_auth", "d2_l_weaver"

D2 = Diagram(
    id="D2",
    name="Assistir Transmissão ao Vivo",
    arquivo="subequipe_01_bpmn-d2-assistir-transmissao.bpmn",
    descricao="Fluxo mínimo do foco: consumo de uma transmissão ao vivo pelo espectador.",
    pools=[
        Pool("d2_p_esp", "Espectador (cliente web)", "d2_proc_esp", [
            Lane(L_USER, "Espectador"),
            Lane(L_SPA, "Aplicação da página (SPA)"),
            Lane(L_PLAYER, "Player de vídeo (MSE + ABR)"),
        ]),
        Pool("d2_p_plat", "Plataforma de streaming", "d2_proc_plat", [
            Lane(L_AUTH, "Serviço de autorização de reprodução"),
            Lane(L_WEAVER, "Balanceador de manifesto"),
        ]),
    ],
    nodes=[
        # ---------------- Espectador ----------------
        N("d2_u_start", "start", "Espectador abre a página do canal", L_USER, 0, 0),
        N("d2_u_end", "end", "Sessão de reprodução encerrada", L_USER, 10, 0),

        N("d2_s_load", "service", "Carregar documento e aplicação da página", L_SPA, 1, 0),
        N("d2_s_par", "and", "Inicialização em paralelo", L_SPA, 2, 0),
        N("d2_s_meta", "service", "Consultar metadados do canal (consulta persistida)", L_SPA, 3, 0),
        N("d2_s_end_meta", "end", "Página do canal montada", L_SPA, 4, 0),
        N("d2_s_chat", "call", "Sincronizar chat e eventos em tempo real",
          L_SPA, 3, 1, called="d5_proc_cliente"),
        N("d2_s_end_chat", "end", "Canal de tempo real ativo", L_SPA, 4, 1),

        N("d2_pl_token", "service", "Obter token de reprodução do canal", L_PLAYER, 3, 0),
        N("d2_pl_gw_auth", "xor", "Reprodução autorizada?", L_PLAYER, 4, 0),
        N("d2_pl_block", "end", "Exibir motivo do bloqueio ao espectador", L_PLAYER, 4, 1),
        N("d2_pl_master", "service", "Obter manifesto mestre com a grade de qualidades",
          L_PLAYER, 5, 0),
        N("d2_pl_sel", "rule", "Escolher a qualidade inicial", L_PLAYER, 6, 0),
        N("d2_pl_loop", "call", "Ciclo de reprodução por segmento (ver D2b)",
          L_PLAYER, 7.6, 0, loop="standard", called="d2b_proc_player"),

        # eventos de borda do ciclo de reprodução
        N("d2_b_tok", "boundary", "A cada 18 min", L_PLAYER, 0, 0,
          trigger="timer", timer="R/PT18M", attached_to="d2_pl_loop", interrupting=False,
          label_dy=0),
        N("d2_b_down", "boundary", "Fim de transmissão anunciado", L_PLAYER, 0, 0,
          trigger="message", ref="Fim de transmissão anunciado", attached_to="d2_pl_loop",
          label_dy=46),
        N("d2_b_err", "boundary", "Falha de reprodução", L_PLAYER, 0, 0,
          trigger="error", ref="Falha de reprodução", attached_to="d2_pl_loop",
          label_dy=104),

        N("d2_pl_renew", "service", "Renovar token de reprodução", L_PLAYER, 8.8, 1),
        N("d2_pl_end_renew", "end", "Token renovado sem interromper o vídeo", L_PLAYER, 9.9, 1),
        N("d2_pl_offline", "task", "Exibir tela de canal fora do ar", L_PLAYER, 8.8, 2),
        N("d2_pl_end_off", "end", "Canal fora do ar", L_PLAYER, 9.9, 2),
        N("d2_pl_rec", "call", "Recuperar reprodução (ver D4)", L_PLAYER, 8.8, 3,
          called="d4_proc_player"),
        N("d2_pl_gw_rec", "xor", "Reprodução retomada?", L_PLAYER, 9.9, 3),
        N("d2_pl_fail", "end", "Encerrar com falha e reportar", L_PLAYER, 10.9, 3,
          trigger="escalation", ref="Reprodução não recuperada"),

        # ---------------- Plataforma ----------------
        N("d2_a_start", "start", "Pedido de token recebido", L_AUTH, 3, 0, trigger="message",
          ref="Pedido de token de reprodução"),
        N("d2_a_rule", "rule", "Avaliar direitos de reprodução do espectador", L_AUTH, 4, 0),
        N("d2_a_sign", "service", "Emitir token assinado com prazo de validade", L_AUTH, 5, 0),
        N("d2_a_end", "end", "Token devolvido ao player", L_AUTH, 6, 0, trigger="message",
          ref="Token de reprodução assinado"),

        N("d2_w_start", "start", "Pedido de manifesto mestre", L_WEAVER, 5, 0,
          trigger="message", ref="Pedido de manifesto mestre"),
        N("d2_w_val", "rule", "Validar assinatura e prazo do token", L_WEAVER, 6, 0),
        N("d2_w_sel", "service", "Selecionar cluster e nó de manifesto por geografia e carga",
          L_WEAVER, 7, 0),
        N("d2_w_build", "service", "Montar manifesto mestre só com as qualidades permitidas",
          L_WEAVER, 8, 0),
        N("d2_w_end", "end", "Manifesto mestre devolvido", L_WEAVER, 9, 0,
          trigger="message", ref="Manifesto mestre"),
    ],
    flows=[
        F("d2_u_start", "d2_s_load"),
        F("d2_s_load", "d2_s_par"),
        F("d2_s_par", "d2_s_meta"),
        F("d2_s_meta", "d2_s_end_meta"),
        F("d2_s_par", "d2_s_chat"),
        F("d2_s_chat", "d2_s_end_chat"),
        F("d2_s_par", "d2_pl_token"),

        F("d2_pl_token", "d2_pl_gw_auth"),
        F("d2_pl_gw_auth", "d2_pl_block", "não", condition=True),
        F("d2_pl_gw_auth", "d2_pl_master", "sim", condition=True),
        F("d2_pl_master", "d2_pl_sel"),
        F("d2_pl_sel", "d2_pl_loop"),
        F("d2_pl_loop", "d2_u_end", "espectador sai do canal"),

        F("d2_b_tok", "d2_pl_renew"),
        F("d2_pl_renew", "d2_pl_end_renew"),
        F("d2_b_down", "d2_pl_offline"),
        F("d2_pl_offline", "d2_pl_end_off"),
        F("d2_b_err", "d2_pl_rec"),
        F("d2_pl_rec", "d2_pl_gw_rec"),
        F("d2_pl_gw_rec", "d2_pl_loop", "sim — retomar o ciclo", condition=True,
          waypoints="loop"),
        F("d2_pl_gw_rec", "d2_pl_fail", "não", condition=True),

        F("d2_a_start", "d2_a_rule"),
        F("d2_a_rule", "d2_a_sign"),
        F("d2_a_sign", "d2_a_end"),

        F("d2_w_start", "d2_w_val"),
        F("d2_w_val", "d2_w_sel"),
        F("d2_w_sel", "d2_w_build"),
        F("d2_w_build", "d2_w_end"),
    ],
    msgflows=[
        MsgFlow("d2_pl_token", "d2_a_start", "pedido de token"),
        MsgFlow("d2_a_end", "d2_pl_token", "token + assinatura"),
        MsgFlow("d2_pl_master", "d2_w_start", "token + assinatura"),
        MsgFlow("d2_w_end", "d2_pl_master", "manifesto mestre"),
    ],
    notes=[
        T("d2_n1",
          "Medição (27/08/2026): TTFB de 253 ms. A resposta carrega as decisões de "
          "autorização — bloqueio geográfico, blackout, restrição de qualidade por "
          "assinatura e resolução máxima permitida. Evidência EV-01.",
          "d2_pl_token", L_PLAYER, 3, 4.3),
        T("d2_n2",
          "A autorização é anterior à entrega e independe da CDN: é aqui que a "
          "plataforma decide QUAIS qualidades o espectador poderá pedir. "
          "Sem token válido não há manifesto.",
          "d2_a_rule", L_AUTH, 4, 1),
        T("d2_n3",
          "Medição: TTFB de 250 ms; manifesto mestre com 6 qualidades "
          "(1080p60 fonte, 720p60, 480p, 360p, 160p e somente áudio). Evidência EV-02.",
          "d2_pl_master", L_PLAYER, 5.1, 4.3),
        T("d2_n4",
          "O nó de manifesto e a origem observados ficam em regiões diferentes, e o "
          "manifesto declara o país do espectador: a escolha do ponto de entrega é "
          "feita aqui, não no player. Evidência EV-02.",
          "d2_w_sel", L_WEAVER, 7, 1),
        T("d2_n5",
          "Este subprocesso concentra o custo de latência do fluxo e roda enquanto a "
          "transmissão durar. Detalhado em D2b; a decisão de qualidade dentro dele "
          "está em D3 e o tratamento de falha em D4.",
          "d2_pl_loop", L_PLAYER, 7.2, 4.3),
        T("d2_n6",
          "Validade do token medida: 1183 s (~20 min). A renovação é não interruptiva "
          "de propósito: interromper o ciclo para renovar credencial custaria "
          "rebuffering visível ao espectador.",
          "d2_pl_renew", L_PLAYER, 9.4, 4.3),
    ],
)
