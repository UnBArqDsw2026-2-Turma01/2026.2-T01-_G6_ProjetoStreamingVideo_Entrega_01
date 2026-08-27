# `tools/` — ferramentas do FOCO_02 (SubEquipe_01)

Código de apoio à Engenharia Reversa e à Modelagem BPMN. Não faz parte do produto: existe para que a coleta e os diagramas sejam **reprodutíveis** e para que uma correção não custe refazer trabalho manual.

Pré-requisitos: `python3` (só biblioteca padrão), `curl`, `chromium`, `node` e `npm`.

## Divisão em 4 blocos por NFR

A SubEquipe_01 dividiu o FOCO_02 (Engenharia Reversa + BPMN) em **4 blocos assíncronos**, um por membro, cada um lendo a mesma plataforma pela lente de um NFR diferente — a mesma ideia já usada no [SIG](../docs/Base/Relatorios/1.1.1.SubEquipe_01/2.NFRFramework.md#3-softgoal-escolhido-e-justificativa), agora aprofundada até o BPMN. Detalhe da divisão e do porquê em [3.EngenhariaReversa.md §0](../docs/Base/Relatorios/1.1.1.SubEquipe_01/3.EngenhariaReversa.md#0-divisão-do-foco-entre-os-4-membros).

Toda ferramenta abaixo é **compartilhada** pelos 4 blocos, mas cada bloco escreve na sua própria subpasta — nunca na de outro membro:

| Bloco (NFR) | Pasta de evidências | Prefixo de diagrama BPMN |
| -- | -- | -- |
| Performance/Latência | `docs/assets/engenharia-reversa/subequipe_01/performance-latencia/` | `D` (`D0`…`D5`, já publicados) |
| Usabilidade/Interatividade | `docs/assets/engenharia-reversa/subequipe_01/usabilidade-interatividade/` | `U` |
| Confiabilidade/Disponibilidade | `docs/assets/engenharia-reversa/subequipe_01/confiabilidade-disponibilidade/` | `C` |
| Segurança | `docs/assets/engenharia-reversa/subequipe_01/seguranca/` | `S` |

## `engenharia-reversa/` — coleta e anonimização das evidências

| Arquivo | O que faz |
| -- | -- |
| [`coletar.sh`](engenharia-reversa/coletar.sh) | Repete, fora do navegador, as requisições que o player faz sozinho ao abrir um canal ao vivo. Grava as capturas brutas e chama a anonimização. **A pasta de saída é obrigatória** — passe a subpasta do seu bloco (tabela acima) |
| [`montar_url.py`](engenharia-reversa/montar_url.py) | Monta a URL do manifesto mestre a partir do token de reprodução, como o player faz |
| [`medir_playlist.py`](engenharia-reversa/medir_playlist.py) | Amostra a janela ao vivo, calcula o atraso na borda e mede a entrega de um segmento |
| [`anonimizar.py`](engenharia-reversa/anonimizar.py) | Substitui identificadores por rótulos genéricos antes de versionar. Regras em [ANONIMIZACAO.md](../docs/assets/engenharia-reversa/subequipe_01/ANONIMIZACAO.md) — vale para os 4 blocos |
| [`figuras_devtools.py`](engenharia-reversa/figuras_devtools.py) · [`gerar_figuras.sh`](engenharia-reversa/gerar_figuras.sh) | Reconstrói os painéis do DevTools (Network/Console) do bloco **Performance/Latência** a partir das evidências já coletadas, em estilo fiel e anonimizado. **Gerado por IA generativa** nesta sessão — ver nota abaixo. Outro bloco que queira o mesmo tipo de figura copia este arquivo (não reaproveita em execução) e ajusta `BLOCO_NFR` e as cenas |
| `alvo.env.exemplo` | Modelo de configuração. Os endereços reais ficam em `alvo.env`, **fora do versionamento** (diretriz: não nomear a fonte de inspiração) — compartilhado pelos 4 blocos, pois é a mesma plataforma analisada |

```bash
cp tools/engenharia-reversa/alvo.env.exemplo tools/engenharia-reversa/alvo.env
```

Preencha os valores (o próprio arquivo diz onde ler cada um na aba Network) e rode, indicando a subpasta do **seu** bloco:

```bash
./tools/engenharia-reversa/coletar.sh <canal> docs/assets/engenharia-reversa/subequipe_01/<sua-subpasta>
```

> **Limites da coleta**: só requisições que a própria aplicação faz, sem sessão autenticada, sem contornar proteção, no volume de uma sessão humana. Vale para os 4 blocos. Ver [Engenharia Reversa §2.3](../docs/Base/Relatorios/1.1.1.SubEquipe_01/3.EngenhariaReversa.md#23-limites-adotados-na-coleta).

### Nota de autoria — `figuras_devtools.py` e `gerar_figuras.sh`

Estes dois arquivos foram **escritos por assistente de IA generativa** nesta sessão de trabalho, a pedido do membro responsável pelo bloco Performance/Latência. Dois motivos, os mesmos registrados em [FOCO_03](../docs/Base/Relatorios/1.1.1.SubEquipe_01/5.IAGenerativa.md):

1. **Não expor a plataforma analisada.** A diretriz proíbe capturas com a marca da fonte de inspiração (não-escopo FE06). Uma captura de tela real do DevTools mostraria o domínio da plataforma em cada requisição; o script reconstrói o mesmo painel, com o mesmo dado medido, mas anonimizado.
2. **Facilitar a análise e a revisão.** Refazer seis capturas de tela manualmente a cada ajuste de legenda ou de layout é retrabalho; regerar por código custa um comando.

Os **números, cabeçalhos e tópicos** desenhados nas figuras não foram inventados pela IA — vêm das evidências reais (EV-01 a EV-06 do bloco Performance/Latência), coletadas antes e à parte da geração das imagens. A IA escreveu o código que desenha; não escolheu o que aconteceu na coleta.

## `bpmn/` — geração e renderização dos diagramas

Os diagramas são descritos como especificação declarativa em Python; o gerador emite BPMN 2.0 com geometria, e a renderização usa a própria biblioteca do bpmn.io dentro de um Chromium headless. Os `.bpmn` resultantes abrem normalmente no **Camunda Modeler**, que continua sendo a ferramenta oficial do projeto para ajuste fino.

| Arquivo | O que faz |
| -- | -- |
| [`gerador.py`](bpmn/gerador.py) | Converte a especificação em BPMN 2.0 (semântica + diagrama). Compartilhado pelos 4 blocos — não tem nada específico de NFR |
| [`diagramas/`](bpmn/diagramas/) | Um módulo por diagrama. Bloco Performance/Latência: `D0`…`D5` (publicados). Cada novo bloco cria seus próprios módulos com o prefixo da tabela acima (ex.: `u0_algo.py` para Usabilidade) e os registra em `diagramas/__init__.py` |
| [`renderizar.sh`](bpmn/renderizar.sh) | Gera os PNG de pré-visualização a partir de **todos** os `.bpmn` em `docs/assets/bpmn/` — roda para os 4 blocos de uma vez, sem precisar de flag |
| [`medir_di.py`](bpmn/medir_di.py) · [`montar_pagina.py`](bpmn/montar_pagina.py) | Apoio à renderização |

```bash
python3 tools/bpmn/gerador.py && bash tools/bpmn/renderizar.sh
```

Para gerar um diagrama só: `python3 tools/bpmn/gerador.py D2b` (ou `U0`, `C0`, `S0`, conforme o bloco).

### Convenção de nomes para os novos blocos

Nenhuma pasta separada é necessária em `docs/assets/bpmn/` — é a mesma pasta de todas as subequipes do projeto, e o prefixo de arquivo já evita colisão:

```
subequipe_01_bpmn-<prefixo><n>-<nome-do-fluxo>.bpmn   ex.: subequipe_01_bpmn-u0-notificacao-canal-ao-vivo.bpmn
```

`<prefixo>` é a letra do bloco (tabela acima); `<n>` numera os diagramas dentro do bloco (`0`, `1`, `2`…), do mesmo jeito que Performance/Latência foi de `D0` a `D5`.

### Por que gerar em vez de desenhar

Os diagramas de um mesmo bloco compartilham raias, anotações de medição e pontos de conexão entre si. No editor gráfico, manter essa coerência é trabalho manual repetido a cada revisão; aqui a especificação é texto versionado e uma correção custa um comando. O preço está registrado no [senso crítico do bloco Performance/Latência](../docs/Base/Relatorios/1.1.1.SubEquipe_01/4.BPMN.md#7-senso-crítico): o layout é determinístico, não bonito — o polimento visual antes da apresentação é manual, no Camunda Modeler. Um novo bloco não é obrigado a gerar por código — desenhar direto no Camunda Modeler e versionar o `.bpmn` também é válido; a ferramenta existe para quem preferir o mesmo caminho já usado no primeiro bloco.

### Verificação

Os arquivos gerados são validados com `bpmn-moddle`, a mesma biblioteca que o Camunda Modeler usa para ler BPMN:

```bash
npx --yes -p bpmn-moddle node -e "const {BpmnModdle}=require('bpmn-moddle');const fs=require('fs');(async()=>{for(const f of fs.readdirSync('docs/assets/bpmn').filter(x=>x.endsWith('.bpmn'))){const {warnings}=await new BpmnModdle().fromXML(fs.readFileSync('docs/assets/bpmn/'+f,'utf8'));console.log(f,warnings.length,'avisos')}})()"
```

Resultado esperado: `0 avisos` em todos os arquivos, dos 4 blocos.

## Armadilha de shell nesta máquina

O shell não interativo pode carregar shims do `nvm` e quebrar `node`/`npm`. Os scripts já fazem `unset -f node npm npx; export PATH=/usr/bin:$PATH`; ao rodar comandos `node` à mão, faça o mesmo.
