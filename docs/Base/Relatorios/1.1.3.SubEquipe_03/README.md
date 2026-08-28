# 1.1.3. SubEquipe_03 — Relatório (Entrega 1 · Base)

> Este relatório cobre os **três focos** da Entrega 1. Nenhum tópico deve ser omitido.

## 1. Composição da Subequipe

| Membro | GitHub | Papel na subequipe |
| -- | -- | -- |
| Hugo Freitas Silva | [@HugoFreitass](https://github.com/HugoFreitass) | Líder |
| Philipe Amâncio Reis Caetano | [@Phill-Chill](https://github.com/Phill-Chill) | dev |
| Eduardo Lôbo Moreira | [@EduLoboM](https://github.com/EduLoboM) | dev |

## 2. Escopo Trabalhado

| Item | Definição | Justificativa |
| -- | -- | -- |
| **Artefato generalista escolhido** | **Rich Picture do Ecossistema de Transmissão ao Vivo** | Expressa a rede densa de múltiplos atores (Streamer, Viewer, Marketing, Devs Third-Party, Moderação), fluxos cruzados e tensões operacionais. |
| **Softgoal do SIG (NFR Framework)** | **Confiabilidade, Disponibilidade e Segurança no Ecossistema de Transmissão** | Resiliência sob picos de acesso, entrega contínua de streaming e moderação em tempo real de UGC. |
| **Fluxo modelado em BPMN** | **Chat ao Vivo em Tempo Real sob pico de audiência** | Comunicação bidirecional síncrona sob alta concorrência e moderação instantânea. |

> Sincronizar com as seções 5 e 6 do [Escopo do Produto](Projeto/EscopoProduto.md) para não haver sobreposição entre subequipes.

## 3. Índice do Relatório

| Foco | Página | Status |
| -- | -- | :--: |
| FOCO_01 | [Artefato Generalista](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md) | 🟢 |
| FOCO_01 | [SIG · NFR Framework](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md) | 🟢 |
| FOCO_02 | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) | 🟢 |
| FOCO_02 | [Modelagem BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) | 🟢 |
| FOCO_03 | [IA Generativa](Base/Relatorios/1.1.3.SubEquipe_03/5.IAGenerativa.md) | 🟢 |
| — | [Referências](Base/Relatorios/1.1.3.SubEquipe_03/6.Referencias.md) | 🟢 |

## 4. Metodologia da Subequipe

A SubEquipe_03 trabalhou em estreita colaboração síncrona e assíncrona, combinando sessões de ideação em quadros digitais (Miro e dsm3-goals) com discussões técnicas e revisões de pares. Todos os membros contribuíram ativamente na formulação de hipóteses de engenharia, fundamentação teórica em literatura acadêmica e validação dos artefatos produzidos. O processo geral do grupo segue as diretrizes descritas em [Metodologia & Processo](Projeto/Metodologia.md).

## 5. Rastreabilidade & Elos com Outros Artefatos (visão consolidada)

| Artefato desta subequipe | Origem / Insumo | Elo com | Observação |
| -- | -- | -- | -- |
| **Artefato Generalista (Rich Picture)** | Domínio de streaming ao vivo, UGC e plataformas de referência | [SIG (NFR)](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md), [BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) e [Escopo do Produto](Projeto/EscopoProduto.md) | Fornece os atores, dores/preocupações e fluxos sociotécnicos que originam os softgoals e os processos modelados. |
| **SIG (NFR Framework)** | Rich Picture e pesquisa de arquiteturas resilientes | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) e [BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) | Decompõe os atributos de qualidade e trade-offs a serem verificados no sistema real. |
| **Modelo BPMN** | Atores do Rich Picture e fluxo de chat/moderação sob concorrência | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) | Detalha a sequência temporal e pools/lanes de interação síncrona (13 pools integradas). |
| **IA Generativa (FOCO_03)** | Pesquisa terminológica, levantamento de padrões e debate de trade-offs | [Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md), [SIG (NFR)](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md) e [BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) | Apoio na estruturação conceitual sob estrita filtragem contra alucinações e governança metodológica. |

## 6. Senso Crítico (visão consolidada)

A combinação do Rich Picture (visão sistêmica qualitativa e holística) com o NFR Framework (análise semi-formal de metas de qualidade e trade-offs) forneceu uma base sólida para antecipar conflitos arquiteturais críticos antes da modelagem procedural e da engenharia reversa. O grupo priorizou a clareza de escopo, a conformidade regulatória (LGPD/ECA/DMCA) e a viabilidade técnica de transmissões ao vivo sob alta demanda.

## 7. Versionamentos & Participações

> Quadro oficial consolidado em [1.2. Participações](Base/1.2.ParticipacoesBase.md); aqui fica o registro detalhado da subequipe, com data e link de comprobatório.

| Membro | Foco / Atividade | Data | Comprobatório |
| -- | -- | :--: | -- |
| Eduardo Lôbo Moreira | **FOCO_01**: Rich Picture (infra/CDN/viewer), SSM e NFR (operacionalizações e trade-offs).<br>**FOCO_02**: Engenharia Reversa (tráfego de mídia HLS, CDNs) e revisão do BPMN.<br>**FOCO_03**: Lições aprendidas, senso crítico de normas IETF (RFC 9106, 6455, 8216bis) e governança de IA. | 28/08/2026 | [Histórico Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) · [Histórico BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md#histórico-de-versões) · [Ponto de Vista IA](Base/Relatorios/1.1.3.SubEquipe_03/5.IAGenerativa.md#eduardo-lôbo-moreira) |
| Hugo Freitas Silva | **FOCO_01**: Rich Picture (streamer/governança/DMCA), requisitos NFR e análise de senso crítico.<br>**FOCO_02**: Modelagem BPMN completa (13 pools, diagramas de sequência), visualizador interativo bpmn-js e fundamentação teórica.<br>**FOCO_03**: Lições aprendidas, senso crítico de hipóteses vs fatos e revisão visual. | 28/08/2026 | [Histórico Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) · [Histórico BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md#histórico-de-versões) · [Ponto de Vista IA](Base/Relatorios/1.1.3.SubEquipe_03/5.IAGenerativa.md#hugo-freitas-silva) |
| Philipe Amâncio Reis Caetano | **FOCO_01**: Rich Picture (chat/marketing/devs), grafo dsm3-goals e rastreabilidade.<br>**FOCO_02**: Engenharia Reversa (GraphQL Persisted Queries, WebSockets PubSub, Ad Targeting CSAI) e modelagem lógica de dados.<br>**FOCO_03**: Lições aprendidas, senso crítico de APIs de tempo real vs polling e decodificação assistida. | 28/08/2026 | [Histórico Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) · [Histórico BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md#histórico-de-versões) · [Ponto de Vista IA](Base/Relatorios/1.1.3.SubEquipe_03/5.IAGenerativa.md#philipe-amâncio-reis-caetano) |

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| :--: | :--: | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do relatório da SubEquipe_03 | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 24/08/2026 | Definição do fluxo BPMN e registro das participações no FOCO_01 (NFR Framework) | Eduardo Lôbo Moreira | Equipe G6 |
| 1.2 | 26/08/2026 | Atualização do status do Artefato Generalista (Rich Picture), consolidação de rastreabilidade, referências e participações de todos os membros | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |
| 1.3 | 27/08/2026 | Correção das rotas e links internos para total compatibilidade com Docsify | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |
| 1.4 | 27/08/2026 | Atualização do status do FOCO_03 (IA Generativa) e integração de rastreabilidade | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |
| 1.5 | 28/08/2026 | Conclusão integral de todos os entregáveis da SubEquipe_03 (FOCO_01, FOCO_02 e FOCO_03), atualização de status no índice para 🟢 e consolidação de participações | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |


