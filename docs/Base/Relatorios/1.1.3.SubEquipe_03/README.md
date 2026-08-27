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
| FOCO_02 | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) | ⬜ |
| FOCO_02 | [Modelagem BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) | ⬜ |
| FOCO_03 | [IA Generativa](Base/Relatorios/1.1.3.SubEquipe_03/5.IAGenerativa.md) | ⬜ |
| — | [Referências](Base/Relatorios/1.1.3.SubEquipe_03/6.Referencias.md) | 🟢 |

## 4. Metodologia da Subequipe

A SubEquipe_03 trabalhou em estreita colaboração síncrona e assíncrona, combinando sessões de ideação em quadros digitais (Miro e dsm3-goals) com discussões técnicas e revisões de pares. Todos os membros contribuíram ativamente na formulação de hipóteses de engenharia, fundamentação teórica em literatura acadêmica e validação dos artefatos produzidos. O processo geral do grupo segue as diretrizes descritas em [Metodologia & Processo](Projeto/Metodologia.md).

## 5. Rastreabilidade & Elos com Outros Artefatos (visão consolidada)

| Artefato desta subequipe | Origem / Insumo | Elo com | Observação |
| -- | -- | -- | -- |
| **Artefato Generalista (Rich Picture)** | Domínio de streaming ao vivo, UGC e plataformas de referência (Twitch/YouTube/Kick) | [SIG (NFR)](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md), [BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) e [Escopo do Produto](Projeto/EscopoProduto.md) | Fornece os atores, dores/preocupações e fluxos sociotécnicos que originam os softgoals e os processos modelados. |
| **SIG (NFR Framework)** | Rich Picture e pesquisa de arquiteturas resilientes | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) e [BPMN](Base/Relatorios/1.1.3.SubEquipe_03/4.BPMN.md) | Decompõe os atributos de qualidade e trade-offs a serem verificados no sistema real. |
| **Modelo BPMN** | Atores do Rich Picture e fluxo de chat/moderação sob concorrência | [Engenharia Reversa](Base/Relatorios/1.1.3.SubEquipe_03/3.EngenhariaReversa.md) | Detalha a sequência temporal e pools/lanes de interação síncrona. |

## 6. Senso Crítico (visão consolidada)

A combinação do Rich Picture (visão sistêmica qualitativa e holística) com o NFR Framework (análise semi-formal de metas de qualidade e trade-offs) forneceu uma base sólida para antecipar conflitos arquiteturais críticos antes da modelagem procedural e da engenharia reversa. O grupo priorizou a clareza de escopo, a conformidade regulatória (LGPD/ECA/DMCA) e a viabilidade técnica de transmissões ao vivo sob alta demanda.

## 7. Versionamentos & Participações

> Quadro oficial consolidado em [1.2. Participações](Base/1.2.ParticipacoesBase.md). Aqui fica o registro detalhado da subequipe, com data e link de comprobatório.

| Membro | Foco / Atividade | Data | Comprobatório |
| -- | -- | :--: | -- |
| Eduardo Lôbo Moreira | Pesquisa de arquiteturas de referência, elaboração do Rich Picture (infra/CDN/viewer), fundamentação teórica em SSM e NFR, modelagem de operacionalizações e trade-offs | 26/08/2026 | [Histórico de Versões do Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico do NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) |
| Hugo Freitas Silva | Pesquisa de streaming ao vivo, modelagem do Rich Picture (streamer/governança/DMCA), definição dos requisitos de Confiabilidade/Disponibilidade e análise de senso crítico | 26/08/2026 | [Histórico de Versões do Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico do NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) |
| Philipe Amâncio Reis Caetano | Pesquisa de moderação e chat em tempo real, modelagem do Rich Picture (chat/marketing/devs), estruturação do grafo no dsm3-goals e mapeamento de rastreabilidade | 26/08/2026 | [Histórico de Versões do Rich Picture](Base/Relatorios/1.1.3.SubEquipe_03/1.ArtefatoGeneralista.md#histórico-de-versões) · [Histórico do NFR](Base/Relatorios/1.1.3.SubEquipe_03/2.NFRFramework.md#histórico-de-versões) |

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| :--: | :--: | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do relatório da SubEquipe_03 | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 24/08/2026 | Definição do fluxo BPMN e registro das participações no FOCO_01 (NFR Framework) | Eduardo Lôbo Moreira | Equipe G6 |
| 1.2 | 26/08/2026 | Atualização do status do Artefato Generalista (Rich Picture), consolidação de rastreabilidade, referências e participações de todos os membros | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |
| 1.3 | 27/08/2026 | Correção das rotas e links internos para total compatibilidade com Docsify | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G6 |


