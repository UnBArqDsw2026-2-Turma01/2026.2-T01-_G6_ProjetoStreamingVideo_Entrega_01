"""Gera as figuras do processo de engenharia reversa em estilo DevTools.

Por que reconstrução, e não captura crua de tela: a diretriz da disciplina
proíbe expor o nome da fonte de inspiração (não-escopo FE06). Uma captura do
DevTools sobre o site real mostraria a marca em cada domínio. Estas figuras
reproduzem *fielmente* o que o DevTools mostrou, mas a partir dos dados já
coletados e anonimizados (EV-01 a EV-06): os números, cabeçalhos, tags e
tópicos são os reais; apenas os identificadores da plataforma foram trocados
pelos mesmos rótulos de docs/assets/engenharia-reversa/subequipe_01/ANONIMIZACAO.md.

O contorno do waterfall é esquemático (as janelas de início relativas de cada
requisição não foram cronometradas); a coluna "Time" traz os valores medidos.

NOTA DE AUTORIA: este script e o wrapper `gerar_figuras.sh` foram escritos por
assistente de IA generativa nesta sessão, a pedido do membro responsável, com
dois objetivos declarados: (1) evitar publicar captura real da plataforma
analisada — a reconstrução permite ilustrar o processo sem expor a marca,
cumprindo o não-escopo FE06; e (2) baratear a produção de material visual do
processo, já que refazer seis capturas manualmente a cada revisão de layout
seria o mesmo retrabalho que já motivou gerar os diagramas BPMN por código
(ver tools/bpmn/README ou o próprio gerador). O uso está registrado em
docs/Base/Relatorios/1.1.1.SubEquipe_01/5.IAGenerativa.md — os NÚMEROS
desenhados aqui são sempre os medidos em EV-01 a EV-06, nunca inventados pela IA.

Uso:
    python3 tools/engenharia-reversa/figuras_devtools.py
    # ou, com o wrapper:
    ./tools/engenharia-reversa/gerar_figuras.sh
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
# Bloco desta figura dentro da divisão em 4 NFRs da SubEquipe_01 (ver
# 3.EngenhariaReversa.md §0). Um novo bloco (Usabilidade, Confiabilidade,
# Segurança) não deve escrever aqui: copie este arquivo, troque BLOCO_NFR e as
# cenas em FIGURAS, e gere na sua própria subpasta.
BLOCO_NFR = "performance-latencia"
DESTINO = RAIZ / "docs" / "assets" / "engenharia-reversa" / "subequipe_01" / BLOCO_NFR
LARGURA = 1180

# Paleta aproximada do tema escuro do Chrome DevTools.
CSS = """
* { box-sizing: border-box; }
body { margin: 0; font: 12px/1.5 'Segoe UI', Roboto, Arial, sans-serif;
       background: #202124; color: #e8eaed; }
.jan { border: 1px solid #000; }
.barra { display: flex; align-items: center; gap: 14px; padding: 6px 12px;
         background: #292a2d; border-bottom: 1px solid #3c4043; color: #9aa0a6; }
.barra .aba { color: #e8eaed; }
.barra .aba.on { color: #8ab4f8; border-bottom: 2px solid #8ab4f8; padding-bottom: 5px; }
.chk::before { content: '\\2713 '; color: #8ab4f8; }
.legenda { padding: 10px 14px; background: #17181a; border-top: 1px solid #3c4043;
           color: #bdc1c6; font-size: 12.5px; }
.legenda b { color: #fdd663; }
.tag { display: inline-block; padding: 1px 7px; border-radius: 9px; font-size: 11px;
       font-weight: 600; }
.tag.d2 { background: #1a3a5c; color: #8ab4f8; }
.tag.d2b { background: #16403a; color: #81c995; }
.tag.d3 { background: #4a3a12; color: #fdd663; }
.tag.d5 { background: #3d2a4d; color: #c58af9; }
.tag.d0 { background: #4a2020; color: #f28b82; }
.tag.d1 { background: #2b2b2b; color: #cfcfcf; }
table.net { width: 100%; border-collapse: collapse; }
table.net th { text-align: left; font-weight: 600; color: #9aa0a6; padding: 5px 10px;
               border-bottom: 1px solid #3c4043; background: #292a2d; font-size: 11px; }
table.net td { padding: 5px 10px; border-bottom: 1px solid #2a2b2e; white-space: nowrap;
               overflow: hidden; text-overflow: ellipsis; }
table.net tr:hover td { background: #28292c; }
.name { color: #8ab4f8; }
.dom { color: #9aa0a6; }
.st200 { color: #81c995; } .st101 { color: #c58af9; }
.mePOST { color: #fdd663; } .meGET { color: #81c995; }
.wf { position: relative; height: 12px; background: #202124; border-radius: 2px; }
.wf i { position: absolute; top: 1px; height: 10px; border-radius: 2px; }
.wf .ttfb { background: #5f6368; } .wf .dl { background: #8ab4f8; }
.wf .ws { background: #c58af9; opacity: .6; }
.pane { display: grid; grid-template-columns: 1fr 1.25fr; }
.pane > div { padding: 12px 14px; }
.pane .req { border-right: 1px solid #3c4043; background: #1c1d1f; }
.h { color: #9aa0a6; text-transform: uppercase; font-size: 10.5px; letter-spacing: .04em;
     margin: 12px 0 4px; }
.h:first-child { margin-top: 0; }
.kv { font-family: 'Cascadia Code', Consolas, monospace; font-size: 12px; }
.kv .k { color: #8ab4f8; } .kv .v { color: #e8eaed; }
pre { margin: 0; font-family: 'Cascadia Code', Consolas, monospace; font-size: 12px;
      line-height: 1.55; white-space: pre-wrap; word-break: break-word; }
.j-key { color: #8ab4f8; } .j-str { color: #f28b82; } .j-num { color: #aecbfa; }
.j-bool { color: #fdd663; } .hl { background: #3a2f00; border-radius: 2px; padding: 0 2px;
         outline: 1px solid #6b5900; }
.hl2 { background: #082a12; border-radius: 2px; padding: 0 2px; outline: 1px solid #1f5c34; }
.cons { padding: 4px 0; background: #202124; }
.cons .l { padding: 4px 14px; border-bottom: 1px solid #2a2b2e; font-family: 'Cascadia Code',
           Consolas, monospace; }
.cons .obj { color: #aecbfa; } .cons .gray { color: #9aa0a6; } .cons .grn { color: #81c995; }
.cons .warn { color: #fdd663; }
.badge { display:inline-block; min-width: 18px; text-align:center; padding: 0 5px;
         border-radius: 4px; background:#3c4043; color:#e8eaed; font-size:11px; }
.medpanel { padding: 12px 14px; background:#17181a; }
.medpanel .row { display:flex; justify-content:space-between; padding: 4px 0;
                 border-bottom:1px dashed #3c4043; }
.medpanel .row b { color:#8ab4f8; } .medpanel .big { color:#f28b82; font-weight:700; }
"""


def _wf(ttfb_px: int, dl_px: int, left: int = 0) -> str:
    return (f'<div class="wf"><i class="ttfb" style="left:{left}px;width:{ttfb_px}px"></i>'
            f'<i class="dl" style="left:{left + ttfb_px}px;width:{dl_px}px"></i></div>')


def _pagina(titulo: str, corpo: str) -> str:
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<style>{CSS}</style></head><body>{corpo}</body></html>')


# --------------------------------------------------------------------------- #
# Figura 1 — Network: as quatro origens                                         #
# --------------------------------------------------------------------------- #

def fig1() -> tuple[str, int]:
    linhas = [
        # nome, método, status, tipo, domínio, tamanho, ttfb_px, dl_px, left, cls_status
        ("&lt;canal-A&gt;", "GET", "200", "document", "www.&lt;plataforma&gt;.tv",
         "206&nbsp;kB", 10, 26, 0, "st200", "meGET"),
        ("gql · PlaybackAccessToken", "POST", "200", "fetch", "gql.&lt;plataforma&gt;.tv",
         "1.3&nbsp;kB", 52, 3, 40, "st200", "mePOST"),
        ("gql · metadados do canal", "POST", "200", "fetch", "gql.&lt;plataforma&gt;.tv",
         "3.6&nbsp;kB", 54, 4, 44, "st200", "mePOST"),
        ("&lt;canal-A&gt;.m3u8", "GET", "200", "m3u8", "usher.&lt;cdn-plataforma&gt;.net",
         "9.7&nbsp;kB", 51, 2, 100, "st200", "meGET"),
        ("index-…-.m3u8", "GET", "200", "m3u8", "sae12.playlist.&lt;cdn-plataforma&gt;.net",
         "15&nbsp;kB", 27, 2, 156, "st200", "meGET"),
        ("720p60/…-.ts", "GET", "200", "media", "…&lt;cdn-terceira&gt;.hls.&lt;cdn-plataforma&gt;.net",
         "840&nbsp;kB", 22, 32, 188, "st200", "meGET"),
        ("v1 · hermes", "GET", "101", "websocket", "hermes.&lt;plataforma&gt;.tv",
         "—", 0, 0, 120, "st101", "meGET"),
    ]
    tr = []
    for nome, me, st, tp, dom, sz, ttfb, dl, left, scls, mcls in linhas:
        if st == "101":
            wf = f'<div class="wf"><i class="ws" style="left:{left}px;width:200px"></i></div>'
        else:
            wf = _wf(ttfb, dl, left)
        tr.append(
            f'<tr><td class="name">{nome}</td><td class="{mcls}">{me}</td>'
            f'<td class="{scls}">{st}</td><td>{tp}</td><td class="dom">{dom}</td>'
            f'<td style="text-align:right">{sz}</td><td style="width:280px">{wf}</td></tr>')
    corpo = f"""
    <div class="jan">
      <div class="barra">
        <span class="aba on">Network</span><span class="aba">Console</span>
        <span class="aba">Performance</span>
        <span style="margin-left:auto"></span>
        <span class="chk">Preserve log</span><span class="chk">Disable cache</span>
        <span>Fetch/XHR · JS · CSS · Img · Media · WS</span>
      </div>
      <table class="net">
        <tr><th style="width:230px">Name</th><th style="width:52px">Method</th>
        <th style="width:52px">Status</th><th style="width:78px">Type</th>
        <th>Domain</th><th style="width:70px;text-align:right">Size</th>
        <th style="width:280px">Waterfall</th></tr>
        {''.join(tr)}
      </table>
      <div class="legenda">
        <b>Passo 2 — mapear os atores.</b> Com a página do canal aberta e o vídeo tocando, a aba
        Network revela <b>quatro origens de rede distintas</b> mais uma conexão persistente:
        documento, API (gql), balanceador de manifesto (usher), serviço de manifesto de mídia
        (playlist) e CDN de segmentos — e o WebSocket (hermes). Cada origem que decide sozinha
        vira um <i>pool</i> ou raia em
        &nbsp;<span class="tag d2">D2</span> <span class="tag d2b">D2b</span>
        <span class="tag d5">D5</span>.
      </div>
    </div>"""
    return corpo, 360


# --------------------------------------------------------------------------- #
# Figura 2 — PlaybackAccessToken: a decisão de autorização                       #
# --------------------------------------------------------------------------- #

def fig2() -> tuple[str, int]:
    resp = """{
  "data": { "streamPlaybackAccessToken": {
    "value": "{
      <span class="j-key">\\"authorization\\"</span>: { <span class="j-key">\\"forbidden\\"</span>: <span class="hl2 j-bool">false</span>, <span class="j-key">\\"reason\\"</span>: <span class="j-str">\\"\\"</span> },
      <span class="j-key">\\"blackout_enabled\\"</span>: <span class="j-bool">false</span>, <span class="j-key">\\"geoblock_reason\\"</span>: <span class="j-str">\\"\\"</span>,
      <span class="j-key">\\"expires\\"</span>: <span class="hl j-num">1787840676</span>,
      <span class="j-key">\\"user_ip\\"</span>: <span class="j-str">\\"&lt;ip-redigido&gt;\\"</span>, <span class="j-key">\\"user_id\\"</span>: <span class="j-bool">null</span>,
      <span class="j-key">\\"server_ads\\"</span>: <span class="j-bool">true</span>, <span class="j-key">\\"show_ads\\"</span>: <span class="j-bool">true</span>,
      <span class="j-key">\\"maximum_resolution\\"</span>: <span class="hl j-str">\\"FULL_HD\\"</span>,
      <span class="j-key">\\"maximum_resolution_reasons\\"</span>: {
        <span class="j-key">\\"QUAD_HD\\"</span>: [<span class="j-str">\\"AUTHZ_NOT_LOGGED_IN\\"</span>],
        <span class="j-key">\\"ULTRA_HD\\"</span>: [<span class="j-str">\\"AUTHZ_NOT_LOGGED_IN\\"</span>] }
    }",
    "signature": <span class="j-str">\\"266146…[TRUNCADO]\\"</span> } } }"""
    corpo = f"""
    <div class="jan">
      <div class="barra">
        <span class="aba on">Network</span>
        <span>Headers</span><span style="color:#8ab4f8">Response</span><span>Timing</span>
        <span style="margin-left:auto">gql · PlaybackAccessToken · <span class="st200">200 OK</span></span>
      </div>
      <div class="pane">
        <div class="req">
          <div class="h">Request</div>
          <div class="kv"><span class="k">POST</span> <span class="v">https://gql.&lt;plataforma&gt;.tv/gql</span></div>
          <div class="h">Request headers</div>
          <div class="kv"><span class="k">Client-Id:</span> <span class="v">&lt;client-id-publico-do-cliente-web&gt;</span></div>
          <div class="kv"><span class="k">Content-Type:</span> <span class="v">text/plain;charset=UTF-8</span></div>
          <div class="h">Payload (consulta persistida)</div>
          <div class="kv"><span class="k">operationName:</span> <span class="v">PlaybackAccessToken</span></div>
          <div class="kv"><span class="k">variables.login:</span> <span class="v">&lt;canal-A&gt;</span></div>
          <div class="kv"><span class="k">persistedQuery.sha256Hash:</span> <span class="v">ed230a…</span></div>
          <div class="h">Timing</div>
          <div class="kv"><span class="k">TTFB:</span> <span class="v">253 ms</span> · <span class="k">total:</span> <span class="v">253 ms</span></div>
        </div>
        <div>
          <div class="h">Response</div>
          <pre>{resp}</pre>
        </div>
      </div>
      <div class="legenda">
        <b>Passo 3 — isolar a decisão de autorização.</b> A resposta não traz vídeo: traz a
        <b>decisão</b>. Realçado: <code>maximum_resolution: "FULL_HD"</code> com o motivo
        <code>AUTHZ_NOT_LOGGED_IN</code> (o teto de qualidade é função do estado da conta — RN02);
        e <code>expires</code>, do qual se calcula a validade medida de <b>1183&nbsp;s</b> (RN03).
        Vira em <span class="tag d2">D2</span> a raia <i>Serviço de autorização</i>, o gateway
        “Reprodução autorizada?” e o evento de borda de renovação de token.
      </div>
    </div>"""
    return corpo, 470


# --------------------------------------------------------------------------- #
# Figura 3 — Manifesto mestre: a grade de qualidades                            #
# --------------------------------------------------------------------------- #

def fig3() -> tuple[str, int]:
    m3u8 = """#EXTM3U
<span class="gray">#EXT-X-&lt;plataforma&gt;-INFO:</span>NODE=<span class="j-str">"…elastic-weaver.<span class="hl">sae12</span>"</span>,<span class="hl">USER-COUNTRY="BR"</span>,<span class="hl">MANIFEST-CLUSTER="sae12"</span>,<span class="hl">ORIGIN="sae11"</span>,…

<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">6465525</span>,RESOLUTION=<span class="j-num">1920x1080</span>,CODECS="avc1.64002A,mp4a.40.2",FRAME-RATE=<span class="j-num">60.000</span>,VIDEO="chunked"      <span class="grn">← 1080p60 (source)</span>
https://sae12.playlist.&lt;cdn-plataforma&gt;.net/v1/playlist/CpcF…-.m3u8
<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">3422999</span>,RESOLUTION=<span class="j-num">1280x720</span>,FRAME-RATE=<span class="j-num">60.000</span>,VIDEO="720p60"
<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">1427999</span>,RESOLUTION=<span class="j-num">852x480</span>,FRAME-RATE=<span class="j-num">30.000</span>,VIDEO="480p30"
<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">630000</span>,RESOLUTION=<span class="j-num">640x360</span>,FRAME-RATE=<span class="j-num">30.000</span>,VIDEO="360p30"
<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">230000</span>,RESOLUTION=<span class="j-num">284x160</span>,FRAME-RATE=<span class="j-num">30.000</span>,VIDEO="160p30"
<span class="gray">#EXT-X-STREAM-INF:</span>BANDWIDTH=<span class="j-num">160000</span>,CODECS="mp4a.40.2",VIDEO="audio_only"                 <span class="grn">← somente áudio (~0,16 Mbit/s)</span>"""
    corpo = f"""
    <div class="jan">
      <div class="barra">
        <span class="aba on">Network</span><span>Headers</span>
        <span style="color:#8ab4f8">Response</span>
        <span style="margin-left:auto">&lt;canal-A&gt;.m3u8 · usher · <span class="st200">200 OK</span>
        · content-type: application/vnd.apple.mpegurl</span>
      </div>
      <div style="padding:12px 14px;background:#1c1d1f"><pre>{m3u8}</pre></div>
      <div class="legenda">
        <b>Passos 5–6 — o token vira manifesto, e o manifesto revela a grade.</b> O balanceador
        (usher) valida a assinatura e devolve <b>6 qualidades</b> (RN06) e um bloco de metadados
        que denuncia a geografia: <code>ORIGIN=sae11</code>, <code>MANIFEST-CLUSTER=sae12</code>,
        <code>USER-COUNTRY=BR</code> — a escolha do ponto de entrega é do servidor (RN05). Vira em
        <span class="tag d2">D2</span> a raia <i>Balanceador de manifesto</i> e alimenta as
        entradas do ABR em <span class="tag d3">D3</span>.
      </div>
    </div>"""
    return corpo, 356


# --------------------------------------------------------------------------- #
# Figura 4 — A janela ao vivo: medindo a latência                               #
# --------------------------------------------------------------------------- #

def fig4() -> tuple[str, int]:
    polls = []
    base_left = 0
    for i, (t, atraso) in enumerate([("14:07:22", "1.46"), ("14:07:24", "1.83"),
                                     ("14:07:26", "1.95"), ("14:07:28", "2.09"),
                                     ("14:07:30", "2.23"), ("14:07:32", "2.37")]):
        left = i * 82
        polls.append(
            f'<tr><td class="name">index-…-.m3u8</td><td class="meGET">GET</td>'
            f'<td class="st200">200</td><td class="dom">…playlist.&lt;cdn-plataforma&gt;.net</td>'
            f'<td style="text-align:right">15&nbsp;kB</td>'
            f'<td style="width:520px"><div class="wf">'
            f'<i class="ttfb" style="left:{left}px;width:14px"></i>'
            f'<i class="dl" style="left:{left + 14}px;width:3px"></i></div></td>'
            f'<td class="gray">último seg. {t} · atraso {atraso}s</td></tr>')
    seg_row = (
        '<tr><td class="name">720p60/…-.ts</td><td class="meGET">GET</td>'
        '<td class="st200">200</td><td class="dom">…&lt;cdn-terceira&gt;.hls…</td>'
        '<td style="text-align:right">840&nbsp;kB</td>'
        '<td><div class="wf"><i class="ttfb" style="left:26px;width:22px"></i>'
        '<i class="dl" style="left:48px;width:36px"></i></div></td>'
        '<td class="grn">X-Cache: Hit · Age: 2</td></tr>')
    corpo = f"""
    <div class="jan">
      <div class="barra">
        <span class="aba on">Network</span>
        <span>filtro: <span style="color:#e8eaed">.m3u8</span></span>
        <span style="margin-left:auto">6 leituras a cada ~2 s · 1 segmento novo por leitura</span>
      </div>
      <table class="net">
        <tr><th style="width:150px">Name</th><th style="width:50px">Method</th>
        <th style="width:50px">Status</th><th>Domain</th>
        <th style="width:64px;text-align:right">Size</th>
        <th style="width:200px">Waterfall</th><th style="width:210px">Observação</th></tr>
        {''.join(polls)}{seg_row}
      </table>
      <div class="medpanel">
        <div class="row"><b>Janela do manifesto</b><span>16 segmentos × 2,000 s = <b>32 s</b> de DVR</span></div>
        <div class="row"><b>Atraso na borda (fim do último seg. → relógio)</b><span class="big">1,46 s – 2,37 s</span></div>
        <div class="row"><b>Download do segmento</b><span>859.724 B em 0,266 s (~26 Mbit/s · faixa: 3,42)</span></div>
        <div class="row"><b>Buffer do player (fig. 6)</b><span class="big">4,1 s – 5,0 s</span></div>
        <div class="row"><b>Soma da parte observável</b><span class="big">≈ 6 s – 8 s</span></div>
      </div>
      <div class="legenda">
        <b>Passos 7–9 — onde o tempo é gasto.</b> Cada leitura do manifesto traz exatamente 1
        segmento novo (RN07); o segmento vem de cache de borda com TTFB de 112 ms (RN08). O
        orçamento acima é o coração do <span class="tag d0">D0</span> e o motivo de existir o
        detalhamento em <span class="tag d2b">D2b</span>.
      </div>
    </div>"""
    return corpo, 545


# --------------------------------------------------------------------------- #
# Figura 5 — Console: a camada de tempo real (WebSocket)                         #
# --------------------------------------------------------------------------- #

def fig5() -> tuple[str, int]:
    topicos = ["stream-chat-room-v1.&lt;id-canal-B&gt;", "video-playback-by-id.&lt;id-canal-B&gt;",
               "community-points-channel-v1.&lt;id-canal-B&gt;", "predictions-channel-v1.&lt;id-canal-B&gt;",
               "raid.&lt;id-canal-B&gt;", "broadcast-settings-update.&lt;id-canal-B&gt;",
               "ads.&lt;id-canal-B&gt;", "hype-train-events-v2.&lt;id-canal-B&gt;"]
    top_html = "".join(f'<div class="l gray">  subscribe → {t}</div>' for t in topicos)
    corpo = f"""
    <div class="jan">
      <div class="barra">
        <span class="aba">Network</span><span class="aba on">Console</span>
        <span style="margin-left:auto">Filter: <span style="color:#e8eaed">__re.ws</span></span>
      </div>
      <div class="cons">
        <div class="l grn">&gt; instrumentação de WebSocket instalada (envelope sobre window.WebSocket)</div>
        <div class="l"><span class="obj">1</span> <span class="gray">conexão aberta:</span> wss://hermes.&lt;plataforma&gt;.tv/v1?clientId=&lt;client-id…&gt;</div>
        <div class="l"><span class="gray">← welcome</span> <span class="obj">{{ keepaliveSec: <span class="warn">15</span>, recoveryUrl: "wss://hermes.&lt;plataforma&gt;.tv/a/v1?…" }}</span></div>
        <div class="l"><span class="gray">← keepalive</span> {{ type: "keepalive", timestamp: "2026-08-27T14:08:10.884Z" }}</div>
        {top_html}
        <div class="l warn">↺ troca de canal (mesma conexão): 38 unsubscribe · 36 subscribe · 0 nova conexão</div>
      </div>
      <div class="legenda">
        <b>Passo 11 — instrumentar o tempo real.</b> Um envelope em torno de <code>WebSocket</code>
        no console mostra <b>uma única conexão</b> multiplexando 36 tópicos (RN11), com a URL de
        recuperação entregue já na saudação. Vira o <i>pool</i> de <span class="tag d5">D5</span>,
        com o padrão publicar/assinar e a reconexão por evento de temporizador de 15 s.
      </div>
    </div>"""
    return corpo, 470


# --------------------------------------------------------------------------- #
# Figura 6 — Console: estado do player (MSE)                                     #
# --------------------------------------------------------------------------- #

def fig6() -> tuple[str, int]:
    corpo = """
    <div class="jan">
      <div class="barra">
        <span class="aba">Network</span><span class="aba on">Console</span>
        <span style="margin-left:auto">document.querySelector('video')</span>
      </div>
      <div class="cons">
        <div class="l grn">&gt; sessão A (&lt;canal-A&gt;)</div>
        <div class="l"><span class="obj">{ readyState: <span class="j-num">4</span>, videoWidth: <span class="j-num">1280</span>, videoHeight: <span class="j-num">720</span>,</span></div>
        <div class="l"><span class="obj">&nbsp;&nbsp;currentTime: <span class="j-num">280.95</span>, bufferAhead: <span class="warn">4.11</span> /* segundos à frente */,</span></div>
        <div class="l"><span class="obj">&nbsp;&nbsp;droppedVideoFrames: <span class="j-num">0</span>, totalVideoFrames: <span class="j-num">16792</span>,</span></div>
        <div class="l"><span class="obj">&nbsp;&nbsp;src: <span class="j-str">"blob:https://www.&lt;plataforma&gt;.tv/3fe2b0b3-…"</span> /* Media Source Extensions */ }</span></div>
        <div class="l gray">// segunda leitura da mesma sessão: bufferAhead 5.02</div>
        <div class="l grn">&gt; sessão B (&lt;canal-B&gt;), mesma janela de exibição 700×394 CSS</div>
        <div class="l"><span class="obj">{ videoWidth: <span class="j-num">1920</span>, videoHeight: <span class="j-num">1080</span> } </span><span class="warn">// resolução ≠ com o mesmo tamanho de tela</span></div>
      </div>
      <div class="legenda">
        <b>Passo 10 — o estado do player.</b> O buffer medido (4,1–5,0 s à frente) é a maior
        parcela isolada da latência, e a fonte <code>blob:</code> confirma reprodução por MSE. Que
        a sessão A tenha estabilizado em 720p e a B em 1080p com a <b>mesma</b> janela de exibição
        mostra que a regra do ABR é caixa-preta (FE03): vira em <span class="tag d3">D3</span> as
        três entradas observáveis da decisão, não a decisão em si.
      </div>
    </div>"""
    return corpo, 380


FIGURAS = {
    "fig-devtools-01-network-origens": fig1,
    "fig-devtools-02-token-autorizacao": fig2,
    "fig-devtools-03-manifesto-grade": fig3,
    "fig-devtools-04-latencia-janela": fig4,
    "fig-devtools-05-console-websocket": fig5,
    "fig-devtools-06-console-player": fig6,
}


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for nome, construir in FIGURAS.items():
            corpo, altura = construir()
            html_path = Path(tmp) / f"{nome}.html"
            html_path.write_text(_pagina(nome, corpo), encoding="utf-8")
            png = DESTINO / f"{nome}.png"
            subprocess.run(
                ["chromium", "--headless", "--disable-gpu", "--hide-scrollbars",
                 "--no-sandbox", "--force-device-scale-factor=2",
                 "--virtual-time-budget=4000",
                 f"--window-size={LARGURA},{altura}",
                 f"--screenshot={png}", f"file://{html_path}"],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{png.relative_to(RAIZ)}  {LARGURA}x{altura} css @2x")


if __name__ == "__main__":
    main()
