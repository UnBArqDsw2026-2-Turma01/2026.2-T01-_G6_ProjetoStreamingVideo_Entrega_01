"""D0 — Cadeia de Latência Fim a Fim (modelo integrador).

Este é o "diagrama maior" da SubEquipe_01: acompanha UM quadro de vídeo desde a
cena diante da câmera até a tela do espectador, e cada etapa longa é uma
atividade de chamada para o diagrama que a detalha. Serve como índice navegável
dos outros seis modelos e como lugar único onde o orçamento de latência medido
aparece etapa por etapa.
"""

from comum import Diagram, F, MsgFlow, N, Pool, T

D0 = Diagram(
    id="D0",
    name="Cadeia de Latência Fim a Fim",
    arquivo="subequipe_01_bpmn-d0-cadeia-latencia.bpmn",
    descricao="Modelo integrador: encadeia D1, D2, D2b, D3, D4 e D5.",
    pools=[
        Pool("d0_p_criador", "Criador de conteúdo", "d0_proc_criador"),
        Pool("d0_p_plat", "Plataforma de streaming", "d0_proc_plat"),
        Pool("d0_p_cdn", "Rede de distribuição (CDN)", "d0_proc_cdn"),
        Pool("d0_p_esp", "Espectador (cliente web)", "d0_proc_esp"),
    ],
    nodes=[
        # ---------------- Criador ----------------
        N("d0_a_start", "start", "A cena ocorre diante da câmera", "d0_p_criador", 0, 0),
        N("d0_a_enc", "call", "Iniciar e manter a transmissão (D1)", "d0_p_criador", 1, 0,
          called="d1_proc_criador"),
        N("d0_a_end", "end", "Fluxo entregue ao ponto de ingestão", "d0_p_criador", 2, 0,
          trigger="message", ref="Fluxo de ingestão"),

        # ---------------- Plataforma ----------------
        N("d0_b_start", "start", "Fluxo recebido na ingestão", "d0_p_plat", 2, 0,
          trigger="message", ref="Fluxo de ingestão"),
        N("d0_b_trans", "task", "Transcodificar a grade e empacotar em segmentos de ~2 s",
          "d0_p_plat", 3, 0),
        N("d0_b_pub", "task", "Publicar na origem e deslizar a janela do manifesto",
          "d0_p_plat", 4, 0),
        N("d0_b_sig", "throw", "Anunciar o canal como ao vivo", "d0_p_plat", 5, 0,
          trigger="signal", ref="Canal ao vivo"),
        N("d0_b_end", "end", "Segmento disponível na origem", "d0_p_plat", 6, 0,
          trigger="message", ref="Segmento disponível"),

        # ---------------- CDN ----------------
        N("d0_c_start", "start", "Segmento disponível na origem", "d0_p_cdn", 6, 0,
          trigger="message", ref="Segmento disponível"),
        N("d0_c_edge", "task", "Servir o segmento no PoP de borda mais próximo",
          "d0_p_cdn", 7, 0),
        N("d0_c_end", "end", "Segmento entregue à borda", "d0_p_cdn", 8, 0,
          trigger="message", ref="Segmento na borda"),

        # ---------------- Espectador ----------------
        N("d0_d_start", "start", "Canal anunciado ao vivo", "d0_p_esp", 5, 0,
          trigger="signal", ref="Canal ao vivo"),
        N("d0_d_play", "call", "Assistir transmissão ao vivo (D2)", "d0_p_esp", 6, 0,
          called="d2_proc_esp"),
        N("d0_d_par", "and", "Duas vias em paralelo", "d0_p_esp", 7, 0),
        N("d0_d_loop", "call", "Ciclo de reprodução por segmento (D2b)", "d0_p_esp", 8, 0,
          called="d2b_proc_player", loop="standard"),
        N("d0_d_rt", "call", "Sincronizar chat e eventos (D5)", "d0_p_esp", 8, 1,
          called="d5_proc_cliente"),
        N("d0_d_buf", "task", "Manter 4–5 s de buffer antes de exibir", "d0_p_esp", 9, 0),
        N("d0_d_join", "and", "Reunir", "d0_p_esp", 10, 0),
        N("d0_d_end", "end", "O espectador vê a cena", "d0_p_esp", 11, 0),
    ],
    flows=[
        F("d0_a_start", "d0_a_enc"),
        F("d0_a_enc", "d0_a_end"),

        F("d0_b_start", "d0_b_trans"),
        F("d0_b_trans", "d0_b_pub"),
        F("d0_b_pub", "d0_b_sig"),
        F("d0_b_sig", "d0_b_end"),

        F("d0_c_start", "d0_c_edge"),
        F("d0_c_edge", "d0_c_end"),

        F("d0_d_start", "d0_d_play"),
        F("d0_d_play", "d0_d_par"),
        F("d0_d_par", "d0_d_loop"),
        F("d0_d_par", "d0_d_rt"),
        F("d0_d_loop", "d0_d_buf"),
        F("d0_d_buf", "d0_d_join"),
        F("d0_d_rt", "d0_d_join"),
        F("d0_d_join", "d0_d_end"),
    ],
    msgflows=[
        MsgFlow("d0_a_end", "d0_b_start", "áudio e vídeo ao vivo"),
        MsgFlow("d0_b_end", "d0_c_start", "segmento publicado"),
        MsgFlow("d0_c_end", "d0_d_loop", "segmento de ~2 s"),
    ],
    notes=[
        T("d0_n1",
          "NÃO MEDIDO. Captura, codificação e ingestão não são observáveis por caixa-preta "
          "a partir do navegador de um espectador. Registrar isto é parte do resultado: "
          "o orçamento abaixo cobre apenas a metade observável da cadeia.",
          "d0_a_enc", "d0_p_criador", 1, 1),
        T("d0_n2",
          "NÃO MEDIDO diretamente. O que se observa é o efeito: segmentos de 2,000 s e "
          "uma grade de 6 qualidades saindo do outro lado (EV-02, EV-03). O tempo gasto "
          "aqui é inferido, não cronometrado.",
          "d0_b_trans", "d0_p_plat", 3, 1),
        T("d0_n3",
          "MEDIDO (EV-04): entrega da borda com acerto de cache, TTFB de 112 ms e "
          "859.724 B em 0,266 s. Idade do objeto na borda entre 2 s e 26 s.",
          "d0_c_edge", "d0_p_cdn", 7, 1),
        T("d0_n4",
          "MEDIDO (EV-05): entre o fim do segmento mais novo publicado e o relógio do "
          "cliente, de 1,46 s a 2,37 s. É a parcela de empacotamento + distribuição.",
          "d0_d_loop", "d0_p_esp", 5.9, 2.1),
        T("d0_n5",
          "MEDIDO (EV-05): 4,1 s a 5,0 s de buffer à frente do ponto exibido. É a maior "
          "parcela isolada da latência observável — e é escolha de projeto, não limite "
          "físico: encurtá-la troca atraso por risco de travamento (trade-off C01 do SIG).",
          "d0_d_buf", "d0_p_esp", 7.9, 2.1),
        T("d0_n6",
          "Esta via chega ANTES do vídeo: não passa pela CDN nem pelo buffer. A diferença "
          "entre os dois caminhos é a dessincronia que o espectador percebe entre o chat "
          "e a imagem. Detalhe em D5.",
          "d0_d_rt", "d0_p_esp", 9.9, 2.1),
        T("d0_n7",
          "Soma da parte observável: ~1,5 s a 2,4 s de manifesto + ~0,3 s de download + "
          "4,1 s a 5,0 s de buffer ≈ 6 s a 8 s entre o segmento existir e ser exibido. "
          "A parcela de captura, codificação e ingestão fica fora dessa conta.",
          "d0_d_end", "d0_p_esp", 12.2, 1.2),
    ],
)
