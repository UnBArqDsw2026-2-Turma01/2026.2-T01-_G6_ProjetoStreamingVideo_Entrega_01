"""D5 — Sincronizar Chat e Eventos em Tempo Real.

Chamado por D2 em paralelo com o player. Está no conjunto porque é a SEGUNDA
via de latência do fluxo: ela não passa pela CDN nem pelo buffer, chega antes
do vídeo, e é exatamente essa diferença que o espectador percebe como
dessincronia entre o chat e a imagem.
"""

from comum import Diagram, F, Lane, MsgFlow, N, Pool, T

L_CLI, L_RT = "d5_l_cli", "d5_l_rt"

D5 = Diagram(
    id="D5",
    name="Sincronizar Chat e Eventos em Tempo Real",
    arquivo="subequipe_01_bpmn-d5-tempo-real.bpmn",
    descricao="Conexão persistente multiplexada por tópicos (padrão publicar/assinar).",
    pools=[
        Pool("d5_p_cliente", "Cliente web — camada de tempo real", "d5_proc_cliente", [
            Lane(L_CLI, "Conexão e assinaturas"),
        ]),
        Pool("d5_p_rt", "Plataforma — malha de tempo real (publicar/assinar)",
             "d5_proc_rt", [
                 Lane(L_RT, "Distribuição de eventos"),
             ]),
    ],
    nodes=[
        # ---------------- Cliente ----------------
        N("d5_start", "start", "Página do canal montada", L_CLI, 0, 0, trigger="message",
          ref="Página do canal montada"),
        N("d5_open", "send", "Abrir uma única conexão persistente multiplexada",
          L_CLI, 1, 0),
        N("d5_wel", "receive", "Receber a saudação com o intervalo de keepalive e a URL "
          "de recuperação", L_CLI, 2, 0),
        N("d5_sub", "send", "Assinar os tópicos do canal", L_CLI, 3, 0, loop="parallel"),
        N("d5_gwe", "eventgw", "Aguardar o próximo evento", L_CLI, 4, 0),
        N("d5_c_notif", "catch", "Notificação de tópico", L_CLI, 5, 0, trigger="message",
          ref="Notificação de tópico"),
        N("d5_c_ka", "catch", "Sem keepalive por 15 s", L_CLI, 5, 1, trigger="timer",
          timer="PT15S"),
        N("d5_c_nav", "catch", "Espectador troca de canal", L_CLI, 5, 2,
          trigger="message", ref="Troca de canal"),
        N("d5_c_close", "catch", "Espectador sai da página", L_CLI, 5, 3,
          trigger="message", ref="Saída da página"),
        N("d5_apply", "service", "Aplicar o evento na interface", L_CLI, 6, 0),
        N("d5_recover", "service", "Reconectar pela URL de recuperação", L_CLI, 6, 1),
        N("d5_resub", "send", "Cancelar as assinaturas e assinar as do novo canal",
          L_CLI, 6, 2),
        N("d5_end", "end", "Conexão encerrada", L_CLI, 6, 3, trigger="terminate"),

        # ---------------- Plataforma ----------------
        N("d5_s_start", "start", "Conexão recebida", L_RT, 1, 0, trigger="message",
          ref="Abertura de conexão de tempo real"),
        N("d5_s_wel", "send", "Enviar a saudação e os parâmetros da sessão", L_RT, 2, 0),
        N("d5_s_reg", "receive", "Registrar as assinaturas de tópico da conexão",
          L_RT, 3, 0),
        N("d5_s_gw", "eventgw", "Aguardar", L_RT, 4, 0),
        N("d5_s_evt", "catch", "Evento publicado em tópico assinado", L_RT, 5, 0,
          trigger="conditional"),
        N("d5_s_ka", "catch", "A cada 15 s", L_RT, 5, 1, trigger="timer",
          timer="R/PT15S"),
        N("d5_s_close", "catch", "Conexão fechada pelo cliente", L_RT, 5, 2,
          trigger="message", ref="Fechamento de conexão"),
        N("d5_s_fan", "send", "Distribuir o evento a todas as conexões assinantes",
          L_RT, 6, 0),
        N("d5_s_send_ka", "send", "Enviar keepalive", L_RT, 6, 1),
        N("d5_s_end", "end", "Assinaturas liberadas", L_RT, 6, 2),
    ],
    flows=[
        F("d5_start", "d5_open"),
        F("d5_open", "d5_wel"),
        F("d5_wel", "d5_sub"),
        F("d5_sub", "d5_gwe"),
        F("d5_gwe", "d5_c_notif"),
        F("d5_gwe", "d5_c_ka"),
        F("d5_gwe", "d5_c_nav"),
        F("d5_gwe", "d5_c_close"),
        F("d5_c_notif", "d5_apply"),
        F("d5_apply", "d5_gwe", "voltar a aguardar", waypoints="loop"),
        F("d5_c_ka", "d5_recover"),
        F("d5_recover", "d5_wel", "retomar a sessão", waypoints="loop"),
        F("d5_c_nav", "d5_resub"),
        F("d5_resub", "d5_gwe", "voltar a aguardar", waypoints="loop"),
        F("d5_c_close", "d5_end"),

        F("d5_s_start", "d5_s_wel"),
        F("d5_s_wel", "d5_s_reg"),
        F("d5_s_reg", "d5_s_gw"),
        F("d5_s_gw", "d5_s_evt"),
        F("d5_s_gw", "d5_s_ka"),
        F("d5_s_gw", "d5_s_close"),
        F("d5_s_evt", "d5_s_fan"),
        F("d5_s_fan", "d5_s_gw", "voltar a aguardar", waypoints="loop"),
        F("d5_s_ka", "d5_s_send_ka"),
        F("d5_s_send_ka", "d5_s_gw", "voltar a aguardar", waypoints="loop"),
        F("d5_s_close", "d5_s_end"),
    ],
    msgflows=[
        MsgFlow("d5_open", "d5_s_start", "abertura da conexão"),
        MsgFlow("d5_s_wel", "d5_wel", "saudação da sessão"),
        MsgFlow("d5_sub", "d5_s_reg", "assinaturas de tópico"),
        MsgFlow("d5_resub", "d5_s_reg", "cancelamentos + novas assinaturas"),
        MsgFlow("d5_s_fan", "d5_c_notif", "evento do tópico"),
        MsgFlow("d5_s_send_ka", "d5_c_notif", "keepalive"),
        MsgFlow("d5_c_close", "d5_s_close", "fechamento"),
    ],
    notes=[
        T("d5_n1",
          "Uma única conexão carrega todos os tópicos do canal (EV-06): 36 assinaturas "
          "foram emitidas em uma só troca de canal e nenhuma segunda conexão foi aberta. "
          "É o padrão publicar/assinar do SIG (O18) visto de fora.",
          "d5_open", L_CLI, 1, 4),
        T("d5_n2",
          "A saudação observada já traz o intervalo de keepalive (15 s) e uma URL de "
          "recuperação pronta: o caminho de reconexão é entregue ANTES de a falha "
          "acontecer. Evidência EV-06.",
          "d5_wel", L_CLI, 3, 4),
        T("d5_n3",
          "Esta via não passa pela CDN nem pelo buffer do player. O evento de chat chega "
          "antes do vídeo correspondente — a dessincronia percebida entre chat e imagem "
          "é o preço de otimizar as duas vias em separado. É o elo mais direto entre o "
          "softgoal de latência e o que o espectador sente.",
          "d5_apply", L_CLI, 5.4, 4),
        T("d5_n4",
          "Na troca de canal foram observados 38 cancelamentos e 36 novas assinaturas "
          "na mesma conexão (EV-06): trocar de canal custa assinatura, não conexão — "
          "poupa o handshake e o TLS a cada navegação.",
          "d5_resub", L_CLI, 7.6, 4),
        T("d5_n5",
          "Uma publicação alcança N assinantes sem N chamadas do cliente: é o fanout que "
          "sustenta chat sob pico de audiência (recorte da SubEquipe_02).",
          "d5_s_fan", L_RT, 6, 3),
    ],
)
