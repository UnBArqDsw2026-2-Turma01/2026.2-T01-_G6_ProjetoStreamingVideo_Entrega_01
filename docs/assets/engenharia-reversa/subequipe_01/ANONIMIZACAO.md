# Anonimização das Evidências — SubEquipe_01

O [Escopo do Produto](../../../Projeto/EscopoProduto.md#_7-fora-de-escopo) fixa, no não-escopo **FE06**, que o nome real e a identidade visual da plataforma de referência não entram na documentação. As evidências deste foco são capturas de rede e de manifestos, e capturas de rede carregam nomes de domínio.

Havia duas saídas ruins e uma boa:

| Alternativa | Por que foi descartada |
| -- | -- |
| Publicar as capturas como vieram | Viola a diretriz de forma direta. |
| Descrever as evidências em prosa, sem anexar arquivo | Tira a verificabilidade: nenhum leitor consegue conferir o que foi medido. Sem isso, "medimos 2,37 s" é indistinguível de "achamos que dá uns 2 s". |
| **Substituição automática e documentada** | Preserva a estrutura técnica inteira — cabeçalhos, tags, parâmetros, tempos e tamanhos — e troca só os identificadores. É o que está publicado aqui. |

A substituição é feita por [`tools/engenharia-reversa/anonimizar.py`](https://github.com/UnBArqDsw2026-2-Turma01/2026.2-T01-_G6_ProjetoStreamingVideo_Entrega_01/blob/main/tools/engenharia-reversa/anonimizar.py), nunca à mão. A regra é código versionado: qualquer membro reaplica sobre uma captura nova e obtém o mesmo resultado, e a professora pode auditar o que foi trocado.

> **O script também não nomeia a plataforma.** As marcas a substituir chegam por variável de ambiente, de um arquivo de configuração que fica fora do versionamento. Deixar o nome dentro do próprio anonimizador contrariaria a diretriz que ele existe para cumprir. Sem essas variáveis, o script recusa a executar em vez de gravar uma evidência mal anonimizada.

## Tabela de substituição

| O que aparecia | O que foi publicado | Por quê |
| -- | -- | -- |
| Marca da plataforma, em qualquer posição | `<plataforma>` | FE06 |
| Domínio da CDN própria da plataforma | `<cdn-plataforma>` | FE06 |
| Nome da CDN de terceiro | `<cdn-terceira>` | FE06 (identificaria a plataforma pelo fornecedor) |
| Nome do provedor de nuvem / de anúncios | `<provedor>` | FE06 |
| Domínio alternativo de segmentos | `<dominio-alternativo>.net` | FE06 |
| Nome dos dois canais observados | `<canal-A>`, `<canal-B>` | Dado de pessoa real, alheio ao objeto de estudo |
| Identificador numérico dos canais | `<id-canal-A>`, `<id-canal-B>` | Idem |
| Endereços IP (v4 e v6) | `<ip-redigido>` | O IP do espectador aparece dentro do token e do manifesto — é dado de quem executou a coleta |
| Identificador público do cliente web | `<client-id-publico-do-cliente-web>` | Não é segredo (vai em texto claro em toda requisição do navegador), mas identificaria a plataforma |
| Cadeias longas: token assinado, assinatura, URLs de segmento | 12 primeiros caracteres + `…[TRUNCADO: N caracteres]` | São credenciais de sessão com validade curta. O prefixo curto mostra o formato sem deixar conteúdo decodificável |

## O que foi mantido de propósito

Tudo o que sustenta uma afirmação técnica do relatório:

- **Tags e cabeçalhos** (`#EXT-X-…`, `X-Cache`, `Age`, `Cache-Control`, `X-Amz-Cf-Pop`) — são a prova do mecanismo;
- **Números** — durações de segmento, larguras de banda declaradas, tempos medidos, tamanhos em bytes, contagens de tópicos;
- **Códigos de região e de ponto de presença** (`sae11`, `sae12`, `GIG52-P2`) — são identificadores geográficos genéricos, e é justamente deles que sai o achado de que o nó de manifesto, a origem e a borda ficam em lugares diferentes;
- **Identificadores de sessão** (`SERVING-ID`, `VIDEO-SESSION-ID`, `BROADCAST-ID`) — sustentam o achado de que o manifesto de mídia é montado por sessão, e expiraram no mesmo dia da coleta.

## Capturas brutas

As capturas originais **não** são versionadas (`.gitignore`: `docs/assets/engenharia-reversa/*/bruto/`). Ficam com quem executou a coleta e podem ser reapresentadas à professora sob demanda, se a verificação exigir.

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 27/08/2026 | Definição do procedimento de anonimização e da tabela de substituição | Lucas Andrade Zanetti | _(pendente)_ |
