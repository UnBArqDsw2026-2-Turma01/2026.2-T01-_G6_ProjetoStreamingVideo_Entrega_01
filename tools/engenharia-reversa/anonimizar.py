"""Anonimiza as capturas brutas da engenharia reversa antes de versioná-las.

A diretriz da disciplina proíbe nomear a fonte de inspiração (não-escopo FE06
do Escopo do Produto). As evidências, porém, precisam continuar verificáveis:
a estrutura das requisições, os cabeçalhos, as tags dos manifestos e os números
medidos são o conteúdo técnico e permanecem intactos.

O que este script faz é uma substituição *documentada e reprodutível*: cada
regra abaixo aparece na tabela de ANONIMIZACAO.md. Nada é reescrito à mão, para
que qualquer membro consiga refazer a mesma anonimização sobre uma nova captura.

Uso:
    python3 tools/engenharia-reversa/anonimizar.py entrada.json saida.json
    cat captura.txt | python3 tools/engenharia-reversa/anonimizar.py > saida.txt
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Marcas identificadoras -> substituto genérico.
#
# NENHUMA marca aparece neste arquivo: elas chegam por variável de ambiente,
# carregadas de `alvo.env` (fora do versionamento). Manter o nome da plataforma
# aqui dentro contrariaria a mesma diretriz que este script existe para cumprir.
#
# A busca é por substring e sem diferenciar maiúsculas: as marcas aparecem
# coladas em identificadores internos (ex.: "cdn_prod_regiao_marca"), onde um
# limite de palavra falharia.
MARCAS = [
    ("RE_MARCA_PLATAFORMA", "<plataforma>"),
    ("RE_MARCA_CDN_PLATAFORMA", "<cdn-plataforma>"),
    ("RE_MARCA_CDN_TERCEIRA", "<cdn-terceira>"),
    ("RE_MARCA_PROVEDOR", "<provedor>"),
    ("RE_MARCA_DOMINIO_ALTERNATIVO", "<dominio-alternativo>"),
    ("RE_MARCA_NO_ALTERNATIVO", "<no-alternativo>"),
    ("RE_CANAL_A", "<canal-A>"),
    ("RE_CANAL_B", "<canal-B>"),
    ("RE_ID_CANAL_A", "<id-canal-A>"),
    ("RE_ID_CANAL_B", "<id-canal-B>"),
    ("RE_CLIENT_ID", "<client-id-publico-do-cliente-web>"),
]

IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
IPV6 = re.compile(r"\b(?:[0-9a-fA-F]{1,4}:){3,7}[0-9a-fA-F]{1,4}\b")
# blobs longos: tokens assinados e URLs de segmento com credencial embutida.
# São cortados curtos o bastante para não sobrar conteúdo decodificável.
BLOB = re.compile(r"[A-Za-z0-9_\-]{80,}")
PREFIXO_BLOB = 12


def anonimizar(texto: str, ambiente: dict[str, str] | None = None) -> str:
    ambiente = ambiente if ambiente is not None else dict(os.environ)
    faltando = [v for v, _ in MARCAS if not ambiente.get(v)]
    if len(faltando) == len(MARCAS):
        raise SystemExit(
            "nenhuma marca definida no ambiente: carregue alvo.env antes "
            "(`set -a; . tools/engenharia-reversa/alvo.env; set +a`)"
        )
    for var, substituto in MARCAS:
        valor = ambiente.get(var)
        if valor:
            texto = re.sub(re.escape(valor), substituto, texto, flags=re.IGNORECASE)
    texto = IPV6.sub("<ip-redigido>", texto)
    texto = IPV4.sub("<ip-redigido>", texto)
    texto = BLOB.sub(
        lambda m: f"{m.group(0)[:PREFIXO_BLOB]}…[TRUNCADO: {len(m.group(0))} caracteres]",
        texto,
    )
    return texto


def main() -> None:
    if len(sys.argv) >= 3:
        entrada, saida = Path(sys.argv[1]), Path(sys.argv[2])
        saida.write_text(
            anonimizar(entrada.read_text(encoding="utf-8")), encoding="utf-8"
        )
        print(f"{entrada.name} -> {saida}")
    else:
        sys.stdout.write(anonimizar(sys.stdin.read()))


if __name__ == "__main__":
    main()
