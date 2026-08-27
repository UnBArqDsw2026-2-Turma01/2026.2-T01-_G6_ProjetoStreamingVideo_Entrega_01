"""Mede a janela do manifesto de mídia e a entrega de um segmento.

Três medições, todas a partir do que o próprio player já busca:

1. **Atraso na borda da janela** — diferença entre o relógio do cliente e o fim
   do segmento mais novo anunciado. É a parcela de empacotamento + distribuição
   da latência ao vivo, e a única observável de fora sem instrumentar o player.
2. **Avanço da janela** — quantos segmentos novos entram por volta de consulta.
   Confirma (ou desmente) que o período de atualização é a duração do segmento.
3. **Entrega do segmento** — tempo, tamanho e cabeçalhos de cache do objeto que
   de fato carrega o vídeo.

Uso: medir_playlist.py <manifesto-mestre.m3u8> <diretorio-de-saida> [voltas]
"""

from __future__ import annotations

import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CABECALHOS_DE_INTERESSE = (
    "content-type", "cache-control", "age", "x-cache", "x-amz-cf-pop",
    "x-amz-cf-id", "date", "server", "via",
)
AGENTE = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) engenharia-reversa-academica"}


def baixar(url: str) -> tuple[bytes, dict[str, str], float]:
    inicio = time.perf_counter()
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE)) as r:
        corpo = r.read()
        return corpo, dict(r.headers), time.perf_counter() - inicio


def variantes(mestre: str) -> dict[str, str]:
    """Mapeia grupo de qualidade -> URL do manifesto de mídia."""
    linhas = mestre.splitlines()
    saida: dict[str, str] = {}
    for i, linha in enumerate(linhas):
        if linha.startswith("#EXT-X-STREAM-INF"):
            grupo = re.search(r'VIDEO="([^"]+)"', linha)
            if grupo:
                saida[grupo.group(1)] = linhas[i + 1]
    return saida


def fim_do_ultimo_segmento(playlist: str) -> float | None:
    marcas = re.findall(r"#EXT-X-PROGRAM-DATE-TIME:(\S+)", playlist)
    duracoes = [float(x) for x in re.findall(r"#EXTINF:([\d.]+)", playlist)]
    if not marcas or not duracoes:
        return None
    inicio = datetime.strptime(marcas[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
    return inicio.replace(tzinfo=timezone.utc).timestamp() + duracoes[-1]


def main() -> None:
    mestre_arq, destino = Path(sys.argv[1]), Path(sys.argv[2])
    voltas = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    mestre = mestre_arq.read_text(encoding="utf-8")
    grupos = variantes(mestre)
    escolhido = next((g for g in ("720p60", "chunked") if g in grupos), None)
    if escolhido is None:
        raise SystemExit(f"nenhuma variante conhecida em {mestre_arq}: {list(grupos)}")
    url = grupos[escolhido]

    relatorio: list[str] = [f"variante medida: {escolhido}", ""]
    corpo, _, _ = baixar(url)
    (destino / "ev03-manifesto-de-midia.m3u8").write_bytes(corpo)

    relatorio.append("volta | rtt_ms | segmentos_na_janela | ultimo_inicio | atraso_s | anuncio")
    anterior: list[str] = []
    for i in range(voltas):
        corpo, _, rtt = baixar(url)
        agora = time.time()
        texto = corpo.decode()
        marcas = re.findall(r"#EXT-X-PROGRAM-DATE-TIME:(\S+)", texto)
        fim = fim_do_ultimo_segmento(texto)
        atraso = f"{agora - fim:.2f}" if fim else "n/d"
        novos = len([m for m in marcas if m not in anterior]) if anterior else 0
        anuncio = "sim" if "stitched-ad" in texto else "nao"
        relatorio.append(
            f"{i:5d} | {rtt * 1000:6.0f} | {len(marcas):19d} | {marcas[-1]} | "
            f"{atraso:>8} | {anuncio}   (novos desde a volta anterior: {novos})"
        )
        anterior = marcas
        if i < voltas - 1:
            time.sleep(2)

    segmentos = [x for x in texto.splitlines() if x.startswith("http")]
    if segmentos:
        dados, cabecalhos, dur = baixar(segmentos[-1])
        relatorio += [
            "",
            "entrega do último segmento da janela:",
            f"  bytes: {len(dados)}",
            f"  tempo: {dur:.3f} s  ({len(dados) * 8 / dur / 1e6:.2f} Mbit/s)",
        ]
        for chave, valor in cabecalhos.items():
            if chave.lower() in CABECALHOS_DE_INTERESSE:
                relatorio.append(f"  {chave}: {valor}")

    saida = destino / "ev05-medicoes-de-latencia.txt"
    saida.write_text("\n".join(relatorio) + "\n", encoding="utf-8")
    print("\n".join(relatorio))


if __name__ == "__main__":
    main()
