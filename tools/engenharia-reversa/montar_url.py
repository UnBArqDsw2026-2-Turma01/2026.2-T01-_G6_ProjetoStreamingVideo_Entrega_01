"""Monta a URL do manifesto mestre a partir do token de reprodução.

O player faz exatamente isto: pega o par (valor, assinatura) devolvido pelo
serviço de autorização e o repassa como parâmetro de consulta ao balanceador de
manifesto. Reproduzir esse passo fora do navegador é o que permite ler o
manifesto mestre inteiro e cronometrar cada salto.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
from pathlib import Path

PARAMETROS_DO_PLAYER = {
    "allow_source": "true",
    "allow_audio_only": "true",
    "fast_bread": "true",           # sinaliza interesse em baixa latência
    "player_backend": "mediaplayer",
    "playlist_include_framerate": "true",
    "reassignments_supported": "true",   # aceita ser remanejado de nó
    "supported_codecs": "av1,h265,h264",
    "transcode_mode": "cbr_v1",
    "cdm": "wv",
}


def main() -> None:
    token_json, base_url, canal = sys.argv[1:4]
    dados = json.loads(Path(token_json).read_text(encoding="utf-8"))
    token = dados["data"]["streamPlaybackAccessToken"]
    valor = json.loads(token["value"])

    restante = valor["expires"] - int(time.time())
    print(f"validade do token: {restante} s", file=sys.stderr)

    consulta = dict(PARAMETROS_DO_PLAYER)
    consulta["sig"] = token["signature"]
    consulta["token"] = token["value"]
    consulta["p"] = str(int(time.time()))
    print(f"{base_url}/{canal}.m3u8?" + urllib.parse.urlencode(consulta))


if __name__ == "__main__":
    main()
