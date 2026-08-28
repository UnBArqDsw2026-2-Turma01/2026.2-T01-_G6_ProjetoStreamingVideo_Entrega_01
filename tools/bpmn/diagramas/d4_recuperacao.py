"""D4 — Recuperar a Reprodução após Falha.

Chamado por D2 (evento de borda de erro no ciclo) e por D2b (falha ao baixar
segmento ou ausência de segmento novo). Reúne os três modos de falha que a
exploração conseguiu evidenciar do lado do cliente.
"""

from comum import Diagram, F, Lane, N, Pool, T

L_DIAG, L_ACAO = "d4_l_diag", "d4_l_acao"

D4 = Diagram(
    id="D4",
    name="Recuperar a Reprodução após Falha",
    arquivo="subequipe_01_bpmn-d4-recuperacao.bpmn",
    descricao="Tratamento de esgotamento de buffer, token vencido e nó indisponível.",
    pools=[
        Pool("d4_p_player", "Player — recuperação de reprodução", "d4_proc_player", [
            Lane(L_DIAG, "Diagnóstico"),
            Lane(L_ACAO, "Ação corretiva"),
        ]),
    ],
    nodes=[
        N("d4_start", "start", "Falha de reprodução detectada", L_DIAG, 0, 0),
        N("d4_diag", "rule", "Classificar o modo de falha", L_DIAG, 1, 0),
        N("d4_gw", "or", "Quais modos de falha se aplicam?", L_DIAG, 2, 0),
        N("d4_backoff", "catch", "Esperar com recuo exponencial", L_DIAG, 2, 2,
          trigger="timer", timer="R3/PT1S"),

        N("d4_buf", "task", "Pausar e reencher o buffer", L_ACAO, 3, 0),
        N("d4_low", "service", "Descer para a faixa mais baixa disponível", L_ACAO, 4, 0),
        N("d4_tok", "service", "Renovar o token de reprodução", L_ACAO, 3, 1),
        N("d4_master", "service", "Reobter o manifesto mestre", L_ACAO, 4, 1),
        N("d4_node", "service", "Pedir reatribuição de nó ao balanceador", L_ACAO, 3, 2),
        N("d4_alt", "service", "Usar a URL alternativa declarada no manifesto",
          L_ACAO, 4, 2),
        N("d4_join", "or", "Aguardar as correções disparadas", L_ACAO, 5, 0),
        N("d4_retry", "service", "Retomar o download na borda da janela", L_ACAO, 6, 0),
        N("d4_gw2", "xor", "Reprodução retomada?", L_ACAO, 7, 0),
        N("d4_ok", "end", "Reprodução retomada", L_ACAO, 8, 0),
        N("d4_gw3", "xor", "Ainda há tentativas?", L_ACAO, 8, 1),
        N("d4_degrade", "service", "Cair para somente áudio", L_ACAO, 9, 1),
        N("d4_esc", "end", "Falha reportada ao espectador", L_ACAO, 10, 1,
          trigger="escalation", ref="Reprodução não recuperada"),
    ],
    flows=[
        F("d4_start", "d4_diag"),
        F("d4_diag", "d4_gw"),
        F("d4_gw", "d4_buf", "buffer esgotado", condition=True),
        F("d4_gw", "d4_tok", "token vencido ou recusado", condition=True),
        F("d4_gw", "d4_node", "nó ou PoP indisponível", condition=True),
        F("d4_buf", "d4_low"),
        F("d4_tok", "d4_master"),
        F("d4_node", "d4_alt"),
        F("d4_low", "d4_join"),
        F("d4_master", "d4_join"),
        F("d4_alt", "d4_join"),
        F("d4_join", "d4_retry"),
        F("d4_retry", "d4_gw2"),
        F("d4_gw2", "d4_ok", "sim", condition=True),
        F("d4_gw2", "d4_gw3", "não", condition=True),
        F("d4_gw3", "d4_backoff", "sim", condition=True),
        F("d4_backoff", "d4_diag", "nova tentativa", waypoints="loop"),
        F("d4_gw3", "d4_degrade", "não", condition=True),
        F("d4_degrade", "d4_esc"),
    ],
    notes=[
        T("d4_n1",
          "Reencher o buffer é a única ação desta página que o espectador enxerga: é o "
          "'travando'. Os outros dois ramos existem para agir antes que ele perceba.",
          "d4_buf", L_ACAO, 3, 3),
        T("d4_n2",
          "Prazo do token medido em 1183 s, ~20 min (EV-01). Numa transmissão de várias "
          "horas o vencimento é certo, não excepcional — por isso D2 renova por evento "
          "de borda não interruptivo, e este ramo é só a rede de segurança.",
          "d4_tok", L_ACAO, 5.2, 3),
        T("d4_n3",
          "Dois mecanismos de contorno foram observados sem acesso ao código (EV-02): o "
          "pedido ao balanceador declara suporte a reatribuição, e o manifesto mestre "
          "carrega URLs alternativas de segmento em outro domínio.",
          "d4_node", L_ACAO, 7.4, 3),
        T("d4_n4",
          "Cair para somente áudio é degradação graciosa: a faixa de ~0,16 Mbit/s da "
          "grade (EV-02) permite manter a transmissão viva com quase qualquer rede. "
          "Liga ao operacionalizador O15 do SIG.",
          "d4_degrade", L_ACAO, 9.6, 3),
        T("d4_n5",
          "Gateway INCLUSIVO, não exclusivo: uma queda de nó produz ao mesmo tempo "
          "erro de download e buffer drenando, e as correções não se excluem — dá "
          "para renovar o token E trocar de nó. O exclusivo forçaria escolher um "
          "ramo e perderia o caso mais comum.",
          "d4_gw", L_DIAG, 1.4, 3),
    ],
)
