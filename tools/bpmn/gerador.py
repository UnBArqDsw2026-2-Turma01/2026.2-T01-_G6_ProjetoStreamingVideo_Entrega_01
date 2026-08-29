"""Gerador de arquivos BPMN 2.0 (semântica + DI) a partir de uma especificação declarativa.

Por que este gerador existe, em vez de desenhar tudo à mão no Camunda Modeler:
os seis diagramas da SubEquipe_01 compartilham raias, anotações de medição e
pontos de conexão entre si. Manter a coerência entre eles no editor gráfico é
trabalho manual repetido a cada revisão; aqui a especificação é texto versionado
e o layout é determinístico — regerar depois de uma correção custa um comando.

Os arquivos `.bpmn` gerados abrem normalmente no Camunda Modeler / bpmn.io, que
continua sendo a ferramenta oficial do projeto para ajuste fino e exportação.

Uso:
    python3 tools/bpmn/gerador.py            # gera todos os diagramas
    python3 tools/bpmn/gerador.py D2         # gera apenas um
"""

from __future__ import annotations

import html
import sys
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import quoteattr

# --------------------------------------------------------------------------- #
# Parâmetros de layout                                                          #
# --------------------------------------------------------------------------- #

POOL_HEADER_W = 30      # faixa vertical com o nome do pool
LANE_HEADER_W = 30      # faixa vertical com o nome da raia
COL_W = 200             # distância horizontal entre colunas lógicas
ROW_H = 120             # distância vertical entre linhas lógicas dentro da raia
PAD_LEFT = 70           # folga da primeira coluna
LANE_PAD_TOP = 72       # folga do topo da raia até a linha 0
POOL_GAP = 70           # espaço vertical entre pools
DIAGRAM_X = 160         # origem do desenho
DIAGRAM_Y = 80

SIZES = {
    "event": (36, 36),
    "gateway": (50, 50),
    "task": (140, 80),
    "subprocess": (175, 90),
    "data": (36, 50),
    "annotation": (230, 0),  # altura calculada a partir do texto
}

# tipo lógico -> (elemento BPMN, categoria de forma)
NODE_KIND = {
    "start": ("startEvent", "event"),
    "end": ("endEvent", "event"),
    "catch": ("intermediateCatchEvent", "event"),
    "throw": ("intermediateThrowEvent", "event"),
    "boundary": ("boundaryEvent", "event"),
    "task": ("task", "task"),
    "user": ("userTask", "task"),
    "service": ("serviceTask", "task"),
    "send": ("sendTask", "task"),
    "receive": ("receiveTask", "task"),
    "manual": ("manualTask", "task"),
    "rule": ("businessRuleTask", "task"),
    "script": ("scriptTask", "task"),
    "sub": ("subProcess", "subprocess"),
    "call": ("callActivity", "subprocess"),
    "xor": ("exclusiveGateway", "gateway"),
    "and": ("parallelGateway", "gateway"),
    "or": ("inclusiveGateway", "gateway"),
    "eventgw": ("eventBasedGateway", "gateway"),
    "data": ("dataObjectReference", "data"),
    "datastore": ("dataStoreReference", "data"),
}

# gatilho do evento -> (tag da definição, elemento-raiz que precisa existir)
EVENT_DEFS = {
    "message": ("messageEventDefinition", "message"),
    "timer": ("timerEventDefinition", None),
    "signal": ("signalEventDefinition", "signal"),
    "error": ("errorEventDefinition", "error"),
    "escalation": ("escalationEventDefinition", "escalation"),
    "terminate": ("terminateEventDefinition", None),
    "conditional": ("conditionalEventDefinition", None),
    "link": ("linkEventDefinition", None),
}


# --------------------------------------------------------------------------- #
# Modelo de especificação                                                       #
# --------------------------------------------------------------------------- #


@dataclass
class Node:
    id: str
    kind: str                    # chave de NODE_KIND
    name: str = ""
    lane: str | None = None      # id da raia (obrigatório se houver raias)
    col: float = 0
    row: float = 0
    trigger: str | None = None   # chave de EVENT_DEFS
    timer: str | None = None     # rótulo humano do timer (vira documentação)
    ref: str | None = None       # nome do sinal/mensagem/erro referenciado
    attached_to: str | None = None   # para boundary events
    interrupting: bool = True
    loop: str | None = None      # "standard" | "parallel" | "sequential"
    called: str | None = None    # id do processo chamado (callActivity)
    dy: int = 0                  # ajuste fino vertical, em pixels
    label_dy: int = 0            # ajuste fino do rótulo (evita sobreposição)


@dataclass
class Flow:
    src: str
    dst: str
    name: str = ""
    default: bool = False
    condition: bool = False      # desenha o losango de condição na origem
    waypoints: str = "auto"      # "auto" | "h" (cotovelo horizontal) | "v"


@dataclass
class MsgFlow:
    src: str
    dst: str
    name: str = ""


@dataclass
class DataFlow:
    """Associação entre uma atividade e um objeto/armazenamento de dados."""
    task: str
    data: str
    direcao: str = "out"         # "in" (lê) | "out" (escreve)


@dataclass
class Note:
    id: str
    text: str
    attach: str                  # id do nó anotado
    lane: str | None = None
    col: float = 0
    row: float = 0


@dataclass
class Lane:
    id: str
    name: str


@dataclass
class Pool:
    id: str
    name: str
    process: str
    lanes: list[Lane] = field(default_factory=list)


@dataclass
class Diagram:
    id: str
    name: str
    arquivo: str
    pools: list[Pool]
    nodes: list[Node]
    flows: list[Flow] = field(default_factory=list)
    msgflows: list[MsgFlow] = field(default_factory=list)
    dataflows: list[DataFlow] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    descricao: str = ""


# --------------------------------------------------------------------------- #
# Cálculo de geometria                                                          #
# --------------------------------------------------------------------------- #


def _shape_size(node: Node) -> tuple[int, int]:
    _, cat = NODE_KIND[node.kind]
    return SIZES[cat]


def _wrap(text: str, largura: int = 34) -> list[str]:
    linhas, atual = [], ""
    for palavra in text.split():
        if len(atual) + len(palavra) + 1 > largura:
            linhas.append(atual)
            atual = palavra
        else:
            atual = f"{atual} {palavra}".strip()
    if atual:
        linhas.append(atual)
    return linhas or [""]


def calcular_geometria(d: Diagram) -> dict:
    """Devolve {id_do_elemento: (x, y, w, h)} para pools, raias, nós e anotações."""
    geo: dict[str, tuple[float, float, float, float]] = {}
    por_lane: dict[str, list] = {}

    itens = list(d.nodes) + list(d.notes)
    for it in itens:
        if isinstance(it, Node) and it.attached_to:
            continue  # boundary é posicionado depois, sobre a atividade hospedeira
        por_lane.setdefault(it.lane, []).append(it)

    # largura do desenho: maior coluna ocupada em qualquer raia
    max_col = 0.0
    for it in itens:
        if isinstance(it, Node) and it.attached_to:
            continue
        max_col = max(max_col, it.col)
    largura_util = PAD_LEFT + max_col * COL_W + SIZES["task"][0] + 80
    pool_w = POOL_HEADER_W + LANE_HEADER_W + largura_util

    y = DIAGRAM_Y
    for pool in d.pools:
        # pool sem raias: os nós declaram lane = id do próprio pool
        lanes = pool.lanes or [Lane(pool.id, "")]
        pool_h = 0
        alturas: list[float] = []
        for lane in lanes:
            itens_lane = por_lane.get(lane.id, [])
            max_row = max((i.row for i in itens_lane), default=0)
            extra = 0
            for it in itens_lane:
                if isinstance(it, Note):
                    extra = max(extra, 0)
            h = LANE_PAD_TOP * 2 + max_row * ROW_H + extra
            alturas.append(max(h, 140))
            pool_h += alturas[-1]

        geo[pool.id] = (DIAGRAM_X, y, pool_w, pool_h)
        ly = y
        for lane, h in zip(lanes, alturas):
            if pool.lanes:
                geo[lane.id] = (DIAGRAM_X + POOL_HEADER_W, ly,
                                pool_w - POOL_HEADER_W, h)
            for it in por_lane.get(lane.id, []):
                cx = DIAGRAM_X + POOL_HEADER_W + LANE_HEADER_W + PAD_LEFT + it.col * COL_W
                cy = ly + LANE_PAD_TOP + it.row * ROW_H
                if isinstance(it, Note):
                    linhas = _wrap(it.text)
                    w, h_n = SIZES["annotation"][0], 18 + 14 * len(linhas)
                    geo[it.id] = (cx - w / 2, cy - h_n / 2, w, h_n)
                else:
                    w, h_n = _shape_size(it)
                    geo[it.id] = (cx - w / 2, cy - h_n / 2 + it.dy, w, h_n)
            ly += h
        y += pool_h + POOL_GAP

    # eventos de borda: canto inferior direito da atividade hospedeira
    for n in d.nodes:
        if not n.attached_to:
            continue
        hx, hy, hw, hh = geo[n.attached_to]
        w, h = _shape_size(n)
        idx = [x for x in d.nodes if x.attached_to == n.attached_to].index(n)
        geo[n.id] = (hx + hw - 36 - idx * 58, hy + hh - h / 2, w, h)

    return geo


def waypoints(geo: dict, f: Flow, nodes: dict[str, Node]) -> list[tuple[float, float]]:
    sx, sy, sw, sh = geo[f.src]
    tx, ty, tw, th = geo[f.dst]
    scx, scy = sx + sw / 2, sy + sh / 2
    tcx, tcy = tx + tw / 2, ty + th / 2

    origem_boundary = nodes.get(f.src) and nodes[f.src].attached_to

    if origem_boundary:
        # sai por baixo do evento de borda e desce até a altura do destino
        p0 = (scx, sy + sh)
        if abs(tcx - scx) < 8:
            return [p0, (tcx, ty)]
        if abs(tcy - scy) < 6:
            return [p0, (scx, tcy), (tx, tcy)]
        return [p0, (scx, tcy), (tx if tcx > scx else tx + tw, tcy)]

    if f.waypoints == "loop":
        # retorno para trás: desce, atravessa por baixo e entra pela base do alvo
        canal = max(sy + sh, ty + th) + 45
        return [(scx, sy + sh), (scx, canal), (tcx, canal), (tcx, ty + th)]

    if abs(scy - tcy) < 6:                       # mesma linha
        if tcx > scx:
            return [(sx + sw, scy), (tx, tcy)]
        return [(sx, scy), (tx + tw, tcy)]

    if abs(scx - tcx) < 6:                       # mesma coluna
        if tcy > scy:
            return [(scx, sy + sh), (tcx, ty)]
        return [(scx, sy), (tcx, ty + th)]

    if f.waypoints == "v" or tcx <= scx:         # cotovelo vertical primeiro
        y_saida = sy + sh if tcy > scy else sy
        return [(scx, y_saida), (scx, tcy), (tx + tw if tcx < scx else tx, tcy)]

    meio = (sx + sw + tx) / 2                    # cotovelo horizontal
    return [(sx + sw, scy), (meio, scy), (meio, tcy), (tx, tcy)]


def waypoints_msg(geo: dict, mf: MsgFlow) -> list[tuple[float, float]]:
    sx, sy, sw, sh = geo[mf.src]
    tx, ty, tw, th = geo[mf.dst]
    scx, tcx = sx + sw / 2, tx + tw / 2
    if ty > sy:                                  # destino abaixo
        return [(scx, sy + sh), (scx, ty - 0), (tcx, ty)] if abs(scx - tcx) > 6 \
            else [(scx, sy + sh), (tcx, ty)]
    return [(scx, sy), (scx, ty + th)] if abs(scx - tcx) < 6 \
        else [(scx, sy), (scx, ty + th), (tcx, ty + th)]


# --------------------------------------------------------------------------- #
# Serialização                                                                  #
# --------------------------------------------------------------------------- #


def _a(v: str) -> str:
    return quoteattr(v)


def _esc(v: str) -> str:
    return html.escape(v, quote=False)


def gerar_xml(d: Diagram) -> str:
    geo = calcular_geometria(d)
    nodes = {n.id: n for n in d.nodes}
    entradas: dict[str, list[str]] = {}
    saidas: dict[str, list[str]] = {}
    for i, f in enumerate(d.flows):
        fid = f"fl_{i}"
        saidas.setdefault(f.src, []).append(fid)
        entradas.setdefault(f.dst, []).append(fid)

    # elementos-raiz referenciados por eventos
    sinais, mensagens, erros, escalas = {}, {}, {}, {}
    for n in d.nodes:
        if not n.trigger:
            continue
        _, raiz = EVENT_DEFS[n.trigger]
        rotulo = n.ref or n.name
        alvo = {"signal": sinais, "message": mensagens,
                "error": erros, "escalation": escalas}.get(raiz)
        if alvo is not None:
            alvo.setdefault(rotulo, f"{raiz}_{len(alvo)}")

    out: list[str] = []
    add = out.append
    add('<?xml version="1.0" encoding="UTF-8"?>')
    add('<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"'
        ' xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"'
        ' xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"'
        ' xmlns:di="http://www.omg.org/spec/DD/20100524/DI"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        f' id="Definitions_{d.id}" targetNamespace="http://unb.fga/G6_ProjetoStreamingVideo"'
        ' exporter="G6 SubEquipe_01 - tools/bpmn/gerador.py" exporterVersion="1.0">')

    for nome, sid in sinais.items():
        add(f'  <bpmn:signal id="{sid}" name={_a(nome)} />')
    for nome, mid in mensagens.items():
        add(f'  <bpmn:message id="{mid}" name={_a(nome)} />')
    for nome, eid in erros.items():
        add(f'  <bpmn:error id="{eid}" name={_a(nome)} errorCode={_a(nome)} />')
    for nome, eid in escalas.items():
        add(f'  <bpmn:escalation id="{eid}" name={_a(nome)} escalationCode={_a(nome)} />')
    for n in d.nodes:
        if n.kind == "datastore":
            add(f'  <bpmn:dataStore id="{n.id}_store" name={_a(n.name)} />')

    # ---- colaboração -------------------------------------------------------
    add(f'  <bpmn:collaboration id="Collab_{d.id}">')
    for p in d.pools:
        add(f'    <bpmn:participant id="{p.id}" name={_a(p.name)} processRef="{p.process}" />')
    for i, mf in enumerate(d.msgflows):
        add(f'    <bpmn:messageFlow id="mf_{i}" name={_a(mf.name)}'
            f' sourceRef="{mf.src}" targetRef="{mf.dst}" />')
    add('  </bpmn:collaboration>')

    # ---- processos ---------------------------------------------------------
    for p in d.pools:
        nos = [n for n in d.nodes if _pool_de(d, n.lane) is p]
        notas = [t for t in d.notes if _pool_de(d, t.lane) is p]
        add(f'  <bpmn:process id="{p.process}" isExecutable="false">')
        if p.lanes:
            add(f'    <bpmn:laneSet id="ls_{p.id}">')
            for lane in p.lanes:
                add(f'      <bpmn:lane id="{lane.id}" name={_a(lane.name)}>')
                for n in nos:
                    if n.lane == lane.id or (n.attached_to and
                                             nodes[n.attached_to].lane == lane.id):
                        add(f'        <bpmn:flowNodeRef>{n.id}</bpmn:flowNodeRef>')
                add('      </bpmn:lane>')
            add('    </bpmn:laneSet>')

        assoc_por_tarefa: dict[str, list[DataFlow]] = {}
        for df in d.dataflows:
            assoc_por_tarefa.setdefault(df.task, []).append(df)
        for n in nos:
            add(_no_xml(n, entradas, saidas, sinais, mensagens, erros, escalas,
                        assoc_por_tarefa.get(n.id, [])))

        for i, f in enumerate(d.flows):
            if nodes[f.src].id not in {x.id for x in nos}:
                continue
            attrs = f'id="fl_{i}" sourceRef="{f.src}" targetRef="{f.dst}"'
            if f.name:
                attrs += f" name={_a(f.name)}"
            if f.condition:
                add(f'    <bpmn:sequenceFlow {attrs}>')
                add('      <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">'
                    f'{_esc(f.name or "condição")}</bpmn:conditionExpression>')
                add('    </bpmn:sequenceFlow>')
            else:
                add(f'    <bpmn:sequenceFlow {attrs} />')

        for t in notas:
            add(f'    <bpmn:textAnnotation id="{t.id}">')
            add(f'      <bpmn:text>{_esc(t.text)}</bpmn:text>')
            add('    </bpmn:textAnnotation>')
            add(f'    <bpmn:association id="as_{t.id}" sourceRef="{t.attach}"'
                f' targetRef="{t.id}" associationDirection="None" />')
        add('  </bpmn:process>')

    # ---- diagrama ----------------------------------------------------------
    add('  <bpmndi:BPMNDiagram id="Diagram_1">')
    add(f'    <bpmndi:BPMNPlane id="Plane_1" bpmnElement="Collab_{d.id}">')
    for p in d.pools:
        add(_shape(p.id, geo[p.id], horizontal=True))
        for lane in p.lanes:
            add(_shape(lane.id, geo[lane.id], horizontal=True))
    for n in d.nodes:
        marcador = ' isMarkerVisible="true"' if n.kind == "xor" else ""
        add(_shape(n.id, geo[n.id], extra=marcador,
                   label=_label_bounds(n, geo[n.id])))
    for t in d.notes:
        add(_shape(t.id, geo[t.id]))
        add(_edge(f"as_{t.id}", [_ponto_borda(geo[t.attach], geo[t.id]),
                                 _ponto_borda(geo[t.id], geo[t.attach])]))
    for i, f in enumerate(d.flows):
        add(_edge(f"fl_{i}", waypoints(geo, f, nodes), rotulo=f.name,
                  geo_src=geo[f.src]))
    for i, mf in enumerate(d.msgflows):
        add(_edge(f"mf_{i}", waypoints_msg(geo, mf), rotulo=mf.name,
                  geo_src=geo[mf.src]))
    contagem: dict[str, int] = {}
    for df in d.dataflows:
        j = contagem.get(df.task, 0)
        contagem[df.task] = j + 1
        eid = (f"dia_{df.task}_{j}" if df.direcao == "in" else f"doa_{df.task}_{j}")
        a, b = (geo[df.data], geo[df.task]) if df.direcao == "in" \
            else (geo[df.task], geo[df.data])
        add(_edge(eid, [_ponto_borda(a, b), _ponto_borda(b, a)]))
    add('    </bpmndi:BPMNPlane>')
    add('  </bpmndi:BPMNDiagram>')
    add('</bpmn:definitions>')
    return "\n".join(out) + "\n"


def _pool_de(d: Diagram, lane_id: str | None) -> Pool | None:
    for p in d.pools:
        if not p.lanes and lane_id == p.id:
            return p
        for lane in p.lanes:
            if lane.id == lane_id:
                return p
    # nó de borda herda a raia da atividade hospedeira; resolvido pelo chamador
    return d.pools[0] if d.pools else None


def _no_xml(n: Node, entradas, saidas, sinais, mensagens, erros, escalas,
            assoc: list["DataFlow"] | None = None) -> str:
    tag, _ = NODE_KIND[n.kind]
    attrs = f'id="{n.id}"'
    if n.name:
        attrs += f" name={_a(n.name)}"
    if n.kind == "boundary":
        attrs += f' attachedToRef="{n.attached_to}"'
        if not n.interrupting:
            attrs += ' cancelActivity="false"'
    if n.kind in ("catch", "throw") and not n.interrupting:
        pass
    if n.kind == "call" and n.called:
        attrs += f' calledElement="{n.called}"'
    if n.kind == "sub":
        attrs += ' triggeredByEvent="false"'
    if n.kind == "data":
        attrs += f' dataObjectRef="{n.id}_obj"'
    if n.kind == "datastore":
        attrs += f' dataStoreRef="{n.id}_store"'

    linhas = [f"    <bpmn:{tag} {attrs}>"]
    if n.kind not in ("data", "datastore"):
        for fid in entradas.get(n.id, []):
            linhas.append(f"      <bpmn:incoming>{fid}</bpmn:incoming>")
        for fid in saidas.get(n.id, []):
            linhas.append(f"      <bpmn:outgoing>{fid}</bpmn:outgoing>")
    if n.loop == "standard":
        linhas.append('      <bpmn:standardLoopCharacteristics />')
    elif n.loop in ("parallel", "sequential"):
        seq = "true" if n.loop == "sequential" else "false"
        linhas.append(f'      <bpmn:multiInstanceLoopCharacteristics isSequential="{seq}" />')
    if n.trigger:
        deftag, raiz = EVENT_DEFS[n.trigger]
        ref = ""
        rotulo = n.ref or n.name
        if raiz == "signal":
            ref = f' signalRef="{sinais[rotulo]}"'
        elif raiz == "message":
            ref = f' messageRef="{mensagens[rotulo]}"'
        elif raiz == "error":
            ref = f' errorRef="{erros[rotulo]}"'
        elif raiz == "escalation":
            ref = f' escalationRef="{escalas[rotulo]}"'
        if n.trigger == "timer" and n.timer:
            linhas.append(f'      <bpmn:{deftag} id="{n.id}_def">')
            linhas.append('        <bpmn:timeCycle xsi:type="bpmn:tFormalExpression">'
                          f"{_esc(n.timer)}</bpmn:timeCycle>")
            linhas.append(f'      </bpmn:{deftag}>')
        else:
            linhas.append(f'      <bpmn:{deftag} id="{n.id}_def"{ref} />')
    for i, df in enumerate(assoc or []):
        if df.direcao == "in":
            linhas.append(f'      <bpmn:dataInputAssociation id="dia_{n.id}_{i}">')
            linhas.append(f"        <bpmn:sourceRef>{df.data}</bpmn:sourceRef>")
            linhas.append("      </bpmn:dataInputAssociation>")
        else:
            linhas.append(f'      <bpmn:dataOutputAssociation id="doa_{n.id}_{i}">')
            linhas.append(f"        <bpmn:targetRef>{df.data}</bpmn:targetRef>")
            linhas.append("      </bpmn:dataOutputAssociation>")
    linhas.append(f"    </bpmn:{tag}>")
    if n.kind == "data":
        linhas.append(f'    <bpmn:dataObject id="{n.id}_obj" />')
    return "\n".join(linhas)


def _shape(eid: str, bounds, horizontal=False, extra="", label=None) -> str:
    x, y, w, h = bounds
    hz = ' isHorizontal="true"' if horizontal else ""
    s = [f'      <bpmndi:BPMNShape id="{eid}_di" bpmnElement="{eid}"{hz}{extra}>',
         f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" />']
    if label:
        lx, ly, lw, lh = label
        s.append('        <bpmndi:BPMNLabel>')
        s.append(f'          <dc:Bounds x="{lx:.0f}" y="{ly:.0f}"'
                 f' width="{lw:.0f}" height="{lh:.0f}" />')
        s.append('        </bpmndi:BPMNLabel>')
    s.append('      </bpmndi:BPMNShape>')
    return "\n".join(s)


def _label_bounds(n: Node, bounds):
    """Rótulo abaixo de eventos e gateways; dentro da forma para atividades."""
    _, cat = NODE_KIND[n.kind]
    if cat not in ("event", "gateway", "data") or not n.name:
        return None
    x, y, w, h = bounds
    linhas = _wrap(n.name, 20)
    lw, lh = 110, 14 * len(linhas)
    if cat == "gateway":                      # acima: libera espaço para os
        return (x + w / 2 - lw / 2, y - lh - 8, lw, lh)   # rótulos "sim"/"não"
    return (x + w / 2 - lw / 2, y + h + 6 + n.label_dy, lw, lh)


def _ponto_borda(a, b):
    """Ponto da borda de `a` mais próximo do centro de `b`."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    acx, acy = ax + aw / 2, ay + ah / 2
    bcx, bcy = bx + bw / 2, by + bh / 2
    if abs(bcx - acx) > abs(bcy - acy):
        return (ax + aw if bcx > acx else ax, acy)
    return (acx, ay + ah if bcy > acy else ay)


def _edge(eid: str, pts, rotulo: str = "", geo_src=None) -> str:
    s = [f'      <bpmndi:BPMNEdge id="{eid}_di" bpmnElement="{eid}">']
    for x, y in pts:
        s.append(f'        <di:waypoint x="{x:.0f}" y="{y:.0f}" />')
    if rotulo:
        x0, y0 = pts[0]
        x1, y1 = pts[1] if len(pts) > 1 else pts[0]
        if abs(x0 - x1) < 6:                  # trecho vertical
            lx, ly = x0 + 8, y0 + 8
        else:
            lx, ly = (x0 + x1) / 2 - 40, (y0 + y1) / 2 - 24
        s.append('        <bpmndi:BPMNLabel>')
        s.append(f'          <dc:Bounds x="{lx:.0f}" y="{ly:.0f}" width="90" height="18" />')
        s.append('        </bpmndi:BPMNLabel>')
    s.append('      </bpmndi:BPMNEdge>')
    return "\n".join(s)


# --------------------------------------------------------------------------- #
# Execução                                                                      #
# --------------------------------------------------------------------------- #


def escrever(d: Diagram, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    caminho = destino / d.arquivo
    caminho.write_text(gerar_xml(d), encoding="utf-8")
    return caminho


def main() -> None:
    from diagramas import TODOS  # noqa: PLC0415  (import tardio: specs opcionais)

    raiz = Path(__file__).resolve().parents[2]
    destino = raiz / "docs" / "assets" / "bpmn"
    alvo = sys.argv[1] if len(sys.argv) > 1 else None
    for d in TODOS:
        if alvo and d.id != alvo:
            continue
        caminho = escrever(d, destino)
        n_nos = len(d.nodes)
        print(f"{d.id:>3}  {caminho.relative_to(raiz)}  "
              f"({n_nos} nós, {len(d.flows)} fluxos, "
              f"{len(d.msgflows)} fluxos de mensagem, {len(d.notes)} anotações)")


if __name__ == "__main__":
    # reimporta como módulo para que `gerador.Node` seja a mesma classe usada
    # pelas especificações (evita duas cópias: __main__.Node e gerador.Node)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import gerador

    gerador.main()
