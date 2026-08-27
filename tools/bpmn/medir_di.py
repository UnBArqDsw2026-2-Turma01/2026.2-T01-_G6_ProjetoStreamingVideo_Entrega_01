"""Mede a caixa envolvente do diagrama declarada no DI de um arquivo .bpmn.

Imprime "largura altura" em pixels, para dimensionar a janela do navegador
usada em `renderizar.sh`.
"""

import re
import sys
from pathlib import Path

MARGEM = 140


def medir(caminho: Path) -> tuple[int, int]:
    xml = caminho.read_text(encoding="utf-8")
    xs: list[int] = []
    ys: list[int] = []
    for m in re.finditer(r'x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"', xml):
        x, y, w, h = map(int, m.groups())
        xs += [x, x + w]
        ys += [y, y + h]
    for m in re.finditer(r'waypoint x="(-?\d+)" y="(-?\d+)"', xml):
        x, y = map(int, m.groups())
        xs.append(x)
        ys.append(y)
    if not xs:
        raise SystemExit(f"nenhuma forma com coordenadas em {caminho}")
    return max(xs) - min(xs) + MARGEM, max(ys) - min(ys) + MARGEM


if __name__ == "__main__":
    largura, altura = medir(Path(sys.argv[1]))
    print(largura, altura)
