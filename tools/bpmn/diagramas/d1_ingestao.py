"""D1 — Iniciar e Configurar a Transmissão (ingestão).

Fluxo extra da SubEquipe_01. É a metade do pipeline que fica ANTES do
espectador: o que acontece aqui define o piso de latência que D2 e D2b
podem alcançar, por isso entra no mesmo conjunto de modelos.

Limite de observação: o criador e o ponto de ingestão não são observáveis
por caixa-preta a partir do navegador de um espectador. As atividades desta
raia vêm da documentação pública de configuração de transmissão e das
propriedades do que sai do outro lado (grade de qualidades, duração de
segmento e marcações do manifesto) — ver §6.3 da página de Engenharia Reversa.
"""

from comum import DataFlow, Diagram, F, Lane, MsgFlow, N, Pool, T

L_ING, L_TRANS, L_RT = "d1_l_ing", "d1_l_trans", "d1_l_rt"

D1 = Diagram(
    id="D1",
    name="Iniciar e Configurar a Transmissão",
    arquivo="subequipe_01_bpmn-d1-iniciar-transmissao.bpmn",
    descricao="Ingestão, transcodificação e empacotamento — a origem da latência.",
    pools=[
        Pool("d1_p_criador", "Criador de conteúdo", "d1_proc_criador"),
        Pool("d1_p_plat", "Plataforma de streaming", "d1_proc_plat", [
            Lane(L_ING, "Ponto de ingestão (PoP)"),
            Lane(L_TRANS, "Transcodificação e empacotamento"),
            Lane(L_RT, "Malha de tempo real"),
        ]),
    ],
    nodes=[
        # ---------------- Criador ----------------
        N("d1_c_start", "start", "Decide iniciar a transmissão", "d1_p_criador", 0, 0),
        N("d1_c_conf", "user", "Configurar o codificador: resolução, taxa de bits e "
          "intervalo de quadro-chave", "d1_p_criador", 1, 0),
        N("d1_c_key", "user", "Informar a chave de transmissão do canal", "d1_p_criador", 2, 0),
        N("d1_c_open", "send", "Abrir a conexão de ingestão", "d1_p_criador", 3, 0),
        N("d1_c_wait", "receive", "Aguardar a resposta do ponto de ingestão", "d1_p_criador", 4, 0),
        N("d1_c_gw", "xor", "Conexão aceita?", "d1_p_criador", 5, 0),
        N("d1_c_rej", "end", "Corrigir a configuração e tentar de novo", "d1_p_criador", 5, 1.4,
          trigger="error", ref="Ingestão recusada"),
        N("d1_c_push", "send", "Enviar áudio e vídeo continuamente", "d1_p_criador", 6, 0,
          loop="standard"),
        N("d1_b_drop", "boundary", "Queda da conexão", "d1_p_criador", 0, 0,
          trigger="error", ref="Queda da conexão de ingestão", attached_to="d1_c_push"),
        N("d1_c_recon", "service", "Reconectar ao ponto de ingestão", "d1_p_criador", 7.4, 1.5),
        N("d1_c_end", "end", "Transmissão encerrada pelo criador", "d1_p_criador", 8, 0),

        # ---------------- Ingestão ----------------
        N("d1_i_start", "start", "Conexão de ingestão recebida", L_ING, 3, 0,
          trigger="message", ref="Abertura de conexão de ingestão"),
        N("d1_i_val", "rule", "Validar a chave e a elegibilidade do canal", L_ING, 4, 0),
        N("d1_i_gw", "xor", "Chave válida?", L_ING, 5, 0),
        N("d1_i_rej", "end", "Recusar a conexão", L_ING, 5, 1.4, trigger="message",
          ref="Conexão de ingestão recusada"),
        N("d1_i_par", "and", "Aceitar e anunciar", L_ING, 6, 0),
        N("d1_i_acc", "throw", "Confirmar a ingestão ao criador", L_ING, 7, 0,
          trigger="message", ref="Conexão de ingestão aceita"),
        N("d1_i_recv", "receive", "Receber o fluxo contínuo do criador", L_ING, 8, 0,
          loop="standard"),

        # ---------------- Transcodificação ----------------
        N("d1_t_dec", "rule", "Decidir o modo: repassar a fonte ou recodificar", L_TRANS, 9, 0),
        N("d1_t_multi", "service", "Gerar cada qualidade da grade", L_TRANS, 10, 0,
          loop="parallel"),
        N("d1_t_pack", "service", "Empacotar em segmentos de ~2 s com marcação de tempo "
          "absoluta", L_TRANS, 11, 0),
        N("d1_t_ads", "service", "Inserir as marcações de anúncio na linha do tempo",
          L_TRANS, 12, 0),
        N("d1_t_pub", "service", "Publicar o segmento e deslizar a janela do manifesto",
          L_TRANS, 13, 0),
        N("d1_t_par", "and", "Publicar e sinalizar", L_TRANS, 14, 0),
        N("d1_t_gw", "xor", "Transmissão continua?", L_TRANS, 15, 0),
        N("d1_t_end", "end", "Janela de segmentos encerrada", L_TRANS, 16, 0),
        N("d1_d_seg", "data", "Segmento de ~2 s", L_TRANS, 13, 1),
        N("d1_ds_origin", "datastore", "Origem: janela deslizante de segmentos",
          L_TRANS, 14.2, 1),

        # ---------------- Malha de tempo real ----------------
        N("d1_rt_sig", "throw", "Anunciar o canal como ao vivo", L_RT, 15, 0,
          trigger="signal", ref="Canal ao vivo"),
        N("d1_rt_end", "end", "Anúncio publicado nos tópicos do canal", L_RT, 16, 0),
    ],
    flows=[
        F("d1_c_start", "d1_c_conf"),
        F("d1_c_conf", "d1_c_key"),
        F("d1_c_key", "d1_c_open"),
        F("d1_c_open", "d1_c_wait"),
        F("d1_c_wait", "d1_c_gw"),
        F("d1_c_gw", "d1_c_rej", "não", condition=True),
        F("d1_c_gw", "d1_c_push", "sim", condition=True),
        F("d1_c_push", "d1_c_end"),
        F("d1_b_drop", "d1_c_recon"),
        F("d1_c_recon", "d1_c_push", "retomar o envio", waypoints="loop"),

        F("d1_i_start", "d1_i_val"),
        F("d1_i_val", "d1_i_gw"),
        F("d1_i_gw", "d1_i_rej", "não", condition=True),
        F("d1_i_gw", "d1_i_par", "sim", condition=True),
        F("d1_i_par", "d1_i_acc"),
        F("d1_i_par", "d1_i_recv"),
        F("d1_i_acc", "d1_i_recv"),
        F("d1_i_recv", "d1_t_dec"),

        F("d1_t_dec", "d1_t_multi"),
        F("d1_t_multi", "d1_t_pack"),
        F("d1_t_pack", "d1_t_ads"),
        F("d1_t_ads", "d1_t_pub"),
        F("d1_t_pub", "d1_t_par"),
        F("d1_t_par", "d1_t_gw"),
        F("d1_t_par", "d1_rt_sig"),
        F("d1_t_gw", "d1_t_pack", "sim — próximo segmento", condition=True,
          waypoints="loop"),
        F("d1_t_gw", "d1_t_end", "não", condition=True),
        F("d1_rt_sig", "d1_rt_end"),
    ],
    msgflows=[
        MsgFlow("d1_c_open", "d1_i_start", "abertura + chave de transmissão"),
        MsgFlow("d1_i_acc", "d1_c_wait", "conexão aceita"),
        MsgFlow("d1_i_rej", "d1_c_wait", "conexão recusada"),
        MsgFlow("d1_c_push", "d1_i_recv", "fluxo contínuo de áudio e vídeo"),
    ],
    dataflows=[
        DataFlow("d1_t_pub", "d1_d_seg", "out"),
        DataFlow("d1_t_pub", "d1_ds_origin", "out"),
    ],
    notes=[
        T("d1_n1",
          "Repassar a fonte sem recodificar é o caminho de menor latência; recodificar "
          "a grade inteira acrescenta tempo de máquina antes de o primeiro segmento "
          "existir. É o primeiro trade-off do pipeline, e ele é invisível ao espectador.",
          "d1_t_dec", L_TRANS, 9, 2),
        T("d1_n2",
          "Grade observada na saída (EV-02): 1080p60 fonte ~6,5 Mbit/s; 720p60 "
          "~3,4; 480p ~1,4; 360p ~0,63; 160p ~0,23; somente áudio ~0,16.",
          "d1_t_multi", L_TRANS, 11, 2),
        T("d1_n3",
          "Duração de segmento observada: 2,000 s (EV-03). O intervalo de quadro-chave "
          "do codificador precisa dividir esse valor — se não dividir, o empacotador "
          "é obrigado a recodificar e a latência sobe.",
          "d1_t_pack", L_TRANS, 13, 2),
        T("d1_n4",
          "As marcações de anúncio observadas ficam na própria linha do tempo, com "
          "descontinuidade e um segmento curto de 0,235 s para alinhar a fronteira "
          "(EV-03). Isso obriga o manifesto de mídia a ser montado por sessão — e, "
          "por consequência, a não ser cacheável (ver D2b).",
          "d1_t_ads", L_TRANS, 15, 2),
        T("d1_n5",
          "Este sinal é o mesmo que D5 entrega aos espectadores pelo tópico de "
          "reprodução do canal, e é o gatilho de 'canal ao vivo' consumido em D0.",
          "d1_rt_sig", L_RT, 15, 1),
    ],
)
