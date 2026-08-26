# 1.1.1. SubEquipe_01 — Relatório (Entrega 1 · Base)

> Este relatório cobre os **três focos** da Entrega 1. Nenhum tópico deve ser omitido.

## 1. Composição da Subequipe

| Membro | GitHub | Papel na subequipe |
| -- | -- | -- |
| Lucas Andrade Zanetti | [@Bappoz](https://github.com/Bappoz) | Líder |
| Heitor Macedo Ricardo | [@HeitorM50](https://github.com/HeitorM50) | dev |
| Matheus Lemes Amaral | [@1emes](https://github.com/1emes) | dev |
| Pedro Druck Montalvão Reis | [@pedruck](https://github.com/pedruck) | dev |

## 2. Escopo Trabalhado

| Item | Definição | Justificativa |
| -- | -- | -- |
| Artefato generalista escolhido (Rich Picture **ou** Mapa Mental) | Rich Picture | Descreve melhor, de forma visual, os atores e fluxos da arquitetura levantada ([Ata 02, D02](../../../Projeto/Atas/ata-S1-01-2026-08-23.md#decisões)) |
| Softgoal do SIG (NFR Framework) | Performance / Latência | Streaming ao vivo tolera pouco atraso; é a ênfase "Transmissões ao Vivo" do tema traduzida em NFR ([Escopo do Produto §6](../../../Projeto/EscopoProduto.md#6-requisitos-não-funcionais-candidatos-insumo-para-os-sigs)) |
| Fluxo modelado em BPMN | Assistir Transmissão ao Vivo (mínimo) · Início/Configuração da Transmissão (extra) · Troca de Qualidade Adaptativa/ABR (extra) | Ponto onde a latência/buffering do "ao vivo" é mais sensível ao usuário ([Escopo do Produto §5](../../../Projeto/EscopoProduto.md#5-fluxos-selecionados-para-engenharia-reversa--bpmn)) |

> Sincronizar com as seções 5 e 6 do [Escopo do Produto](../../../Projeto/EscopoProduto.md) para não haver sobreposição entre subequipes.

## 3. Índice do Relatório

| Foco | Página | Status |
| -- | -- | -- |
| FOCO_01 | [Artefato Generalista](1.ArtefatoGeneralista.md) | 🟨 v1 publicada (25/08) |
| FOCO_01 | [SIG · NFR Framework](2.NFRFramework.md) | ⬜ |
| FOCO_02 | [Engenharia Reversa](3.EngenhariaReversa.md) | ⬜ |
| FOCO_02 | [Modelagem BPMN](4.BPMN.md) | ⬜ |
| FOCO_03 | [IA Generativa](5.IAGenerativa.md) | ⬜ |
| — | [Referências](6.Referencias.md) | ⬜ |

## 4. Metodologia da Subequipe

<!--
PREENCHER. Como o trabalho da subequipe ocorreu: divisão de tarefas, reuniões, ferramentas,
critérios de revisão interna. Vídeos e atas ajudam aqui (diretriz).
A metodologia específica de cada foco fica na página do respectivo foco.
-->

Processo geral do grupo em [Metodologia & Processo](../../../Projeto/Metodologia.md).

| Item | Definição |
| -- | -- |
| Cadência de reuniões da subequipe | Semanal, às **quartas-feiras à noite** ([Ata 02, D03](../../../Projeto/Atas/ata-S1-01-2026-08-23.md#decisões)) |
| Divisão de tarefas | Rich Picture e levantamento de NFRs construídos **em conjunto** pela subequipe, sem divisão individual nesta fase; a divisão fica reservada para a etapa final de documentação ([Ata 02, D04](../../../Projeto/Atas/ata-S1-01-2026-08-23.md#decisões)) |
| Registro de reuniões | Gravação em vídeo + ata publicada em [Atas de Reunião](../../../Projeto/Atas/README.md) |
| Ferramenta de modelagem colaborativa | Quadro **Miro**, com edição simultânea pelos quatro membros ([Ata 03, D01](../../../Projeto/Atas/ata-S1-02-2026-08-25.md#decisões)) |
| Critério de revisão interna | Revisão em voz alta durante a própria sessão: quem propõe um elemento justifica, e o grupo aceita, renomeia ou descarta antes de seguir |

### Sessões de trabalho realizadas

| # | Data | Duração | Objetivo | Resultado | Registro |
| -- | -- | -- | -- | -- | -- |
| 01 | 23/08/2026 | ~10 min | Confirmar softgoal e fluxos; escolher o artefato generalista; definir cadência | Rich Picture escolhido; softgoal e 3 fluxos confirmados | [Ata 02](../../../Projeto/Atas/ata-S1-01-2026-08-23.md) · [Vídeo](https://www.youtube.com/watch?v=iyWpaxbuiow) |
| 02 | 25/08/2026 | ~1h20 | Construir o artefato generalista | **Rich Picture v1 concluído** e publicado | [Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md) · [Vídeo](https://www.youtube.com/watch?v=7sRz8l8YtqU) |

Restante do processo específico de cada foco (ferramentas do SIG e do BPMN, critérios de revisão) a preencher conforme o trabalho avançar.

## 5. Rastreabilidade & Elos com Outros Artefatos (visão consolidada)

| Artefato desta subequipe | Origem / insumo | Elo com | Observação |
| -- | -- | -- | -- |
| [Rich Picture v1](1.ArtefatoGeneralista.md) | Conhecimento prévio dos membros + pesquisa em documentação pública, consolidados na sessão de 25/08 ([Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md)) | [SIG](2.NFRFramework.md) · [BPMN](4.BPMN.md) · [Engenharia Reversa](3.EngenhariaReversa.md) | A cadeia ingestão → transcodificação → empacotamento → CDN → player é o insumo do SIG; os atores viram lanes no BPMN; os protocolos e componentes citados são hipóteses a verificar no FOCO_02 |
| [SIG (NFR)](2.NFRFramework.md) | Cadeia de latência identificada no Rich Picture | [Rich Picture](1.ArtefatoGeneralista.md) · [BPMN](4.BPMN.md) | ⬜ não iniciado |
| [Modelo BPMN](4.BPMN.md) | Atores e fluxos do Rich Picture; fluxos definidos no [Escopo §5](../../../Projeto/EscopoProduto.md#5-fluxos-selecionados-para-engenharia-reversa--bpmn) | [Rich Picture](1.ArtefatoGeneralista.md) · [Engenharia Reversa](3.EngenhariaReversa.md) | ⬜ não iniciado |

## 6. Senso Crítico (visão consolidada)

<!--
PREENCHER. O que funcionou, o que não funcionou, quais decisões foram revistas, quais
limitações permanecem. Senso crítico é item explicitamente cobrado na diretriz.
-->
_A preencher._

## 7. Versionamentos & Participações

> Quadro oficial consolidado em [1.2. Participações](../../1.2.ParticipacoesBase.md). Aqui fica o registro detalhado da subequipe, com data e link de commit.

| Membro | Contribuição | Data | Comprobatório (commit/PR) |
| -- | -- | -- | -- |
| Lucas Andrade Zanetti | FOCO_01 · Rich Picture: condução da sessão, mapeamento do pipeline de mídia, legenda de fluxos por cor e recorte do artefato; export, versionamento da imagem e redação da página do foco | 25/08/2026 | [Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#7-participantes--comprobatórios) |
| Pedro Druck Montalvão Reis | FOCO_01 · Rich Picture: camadas de infraestrutura (servidor de origem, CDN, edge caching, APIs, Auth) e extensões/desenvolvedores externos | 25/08/2026 | [Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#7-participantes--comprobatórios) |
| Matheus Lemes Amaral | FOCO_01 · Rich Picture: padronização da notação (verbos, tipografia, cores, agrupamentos), desdobramento VOD/Clips e recorte da monetização externa | 25/08/2026 | [Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#7-participantes--comprobatórios) |
| Heitor Macedo Ricardo | FOCO_01 · Rich Picture: camada de chat/moderação (chat, moderadores, AutoMod, Pub/Sub), camada de monetização, correção terminológica do encoder e revisão de layout/recorte | 25/08/2026 | [Ata 03](../../../Projeto/Atas/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#7-participantes--comprobatórios) |

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do relatório da SubEquipe_01 | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 23/08/2026 | Composição da subequipe, escopo trabalhado (Rich Picture, softgoal e fluxos) e metodologia da subequipe, a partir da Ata 02 | [SubEquipe_01](../../../Projeto/Atas/ata-S1-01-2026-08-23.md) | Lucas Andrade Zanetti |
| 1.2 | 25/08/2026 | Registro das sessões de trabalho, ferramenta de modelagem, rastreabilidade consolidada e participações do FOCO_01 após a conclusão do Rich Picture v1 | [SubEquipe_01](../../../Projeto/Atas/ata-S1-02-2026-08-25.md#participantes) | Lucas Andrade Zanetti |
