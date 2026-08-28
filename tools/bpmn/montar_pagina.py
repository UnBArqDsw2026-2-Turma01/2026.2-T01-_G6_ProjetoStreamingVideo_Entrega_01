"""Monta a página HTML autocontida que o Chromium headless usa para renderizar
um diagrama com bpmn-js. Tudo é embutido no arquivo (CSS, biblioteca e XML)
para que a renderização não dependa de rede nem de servidor local.
"""

import json
import sys
from pathlib import Path

MODELO = """<!doctype html><html><head><meta charset="utf-8">
<style>{dcss}</style>
<style>{css}</style>
<style>
  html, body {{ margin: 0; background: #fff; }}
  #c {{ width: 100vw; height: 100vh; }}
  .djs-label, .djs-label tspan {{ font-family: Arial, Helvetica, sans-serif; }}
</style>
</head><body><div id="c"></div>
<script>{viewer}</script>
<script>
  const xml = {xml};
  const viewer = new BpmnJS({{ container: '#c' }});
  viewer.importXML(xml).then(() => {{
    viewer.get('canvas').zoom('fit-viewport', 'auto');
    document.body.setAttribute('data-pronto', '1');
  }}).catch(e => {{ document.body.textContent = 'ERRO: ' + e.message; }});
</script></body></html>"""


def main() -> None:
    bpmn, saida, viewer, css, dcss = (Path(a) for a in sys.argv[1:6])
    saida.write_text(
        MODELO.format(
            dcss=dcss.read_text(encoding="utf-8"),
            css=css.read_text(encoding="utf-8"),
            viewer=viewer.read_text(encoding="utf-8"),
            xml=json.dumps(bpmn.read_text(encoding="utf-8")),
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
