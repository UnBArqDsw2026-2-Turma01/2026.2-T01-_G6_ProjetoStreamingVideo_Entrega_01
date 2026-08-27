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
| Artefato generalista escolhido (Rich Picture **ou** Mapa Mental) | Rich Picture | Descreve melhor, de forma visual, os atores e fluxos da arquitetura levantada ([Ata S1_01, D02](../../../Projeto/Atas/Atas_Sg1/ata-S1-01-2026-08-23.md#decisões)) |
| Softgoal do SIG (NFR Framework) | Performance / Latência | Streaming ao vivo tolera pouco atraso; é a ênfase "Transmissões ao Vivo" do tema traduzida em NFR ([Escopo do Produto §6](../../../Projeto/EscopoProduto.md#_6-requisitos-não-funcionais-candidatos-insumo-para-os-sigs)) |
| Fluxo modelado em BPMN | Assistir Transmissão ao Vivo (mínimo) · Início da Transmissão (extra) · Adaptação de Qualidade/ABR (extra) · Ciclo de Reprodução por Segmento, Recuperação de Falha e Tempo Real (extras adicionais) | Ponto onde a latência/buffering do "ao vivo" é mais sensível ao usuário ([Escopo do Produto §5](../../../Projeto/EscopoProduto.md#_5-fluxos-selecionados-para-engenharia-reversa--bpmn)) |

> Sincronizar com as seções 5 e 6 do [Escopo do Produto](../../../Projeto/EscopoProduto.md) para não haver sobreposição entre subequipes.

## 3. Índice do Relatório

| Foco | Página | Status |
| -- | -- | -- |
| FOCO_01 | [Artefato Generalista](1.ArtefatoGeneralista.md) | ✅ |
| FOCO_01 | [SIG · NFR Framework](2.NFRFramework.md) | ✅|
| FOCO_02 | [Engenharia Reversa](3.EngenhariaReversa.md) | 🟨 v1 · pendente revisão |
| FOCO_02 | [Modelagem BPMN](4.BPMN.md) | 🟨 v1 · pendente revisão |
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
| Cadência de reuniões da subequipe | Semanal, às **quartas-feiras à noite** ([Ata S1_01, D03](../../../Projeto/Atas/Atas_Sg1/ata-S1-01-2026-08-23.md#decisões)) |
| Divisão de tarefas | Rich Picture e levantamento de NFRs construídos **em conjunto** pela subequipe, sem divisão individual nesta fase; a divisão fica reservada para a etapa final de documentação ([Ata S1_01, D04](../../../Projeto/Atas/Atas_Sg1/ata-S1-01-2026-08-23.md#decisões)) |
| Registro de reuniões | Gravação em vídeo + ata publicada em [Atas de Reunião](../../../Projeto/Atas/README.md) |
| Ferramenta de modelagem colaborativa | Quadro **Miro**, com edição simultânea pelos quatro membros ([Ata S1_02, D01](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md#decisões)) |
| Critério de revisão interna | Revisão em voz alta durante a própria sessão: quem propõe um elemento justifica, e o grupo aceita, renomeia ou descarta antes de seguir |

### Sessões de trabalho realizadas

| # | Data | Duração | Objetivo | Resultado | Registro |
| -- | -- | -- | -- | -- | -- |
| 01 | 23/08/2026 | ~10 min | Confirmar softgoal e fluxos; escolher o artefato generalista; definir cadência | Rich Picture escolhido; softgoal e 3 fluxos confirmados | [Ata S1_01](../../../Projeto/Atas/Atas_Sg1/ata-S1-01-2026-08-23.md) · [Vídeo](https://www.youtube.com/watch?v=iyWpaxbuiow) |
| 02 | 25/08/2026 | ~1h20 | Construir o artefato generalista | **Rich Picture v1 concluído** e publicado | [Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md) · [Vídeo](https://www.youtube.com/watch?v=7sRz8l8YtqU) |
| 03 | 26/08/2026 | ~1h23 | Construir o SIG (NFR Framework): um ramo por pessoa presente (Desempenho, Segurança, Confiabilidade, Usabilidade) | **SIG v1 concluído** e publicado; Pedro Druck ausente, revisão posterior encaminhada | [Ata S1_03](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md) · [Vídeo](https://www.youtube.com/watch?v=n36T4kpz-Bk) |
| 04 | 27/08/2026 | ~1h | Executar o FOCO_02: engenharia reversa por caixa-preta no nível de protocolo e modelagem BPMN | **6 evidências** coletadas e anonimizadas, 14 regras inferidas, **7 diagramas BPMN** encadeados publicados; duas hipóteses do FOCO_01 refutadas | [Eng. Reversa](3.EngenhariaReversa.md) · [BPMN](4.BPMN.md) · _ata pendente_ |

Restante do processo específico de cada foco (ferramentas do BPMN, critérios de revisão) a preencher conforme o trabalho avançar.

## 5. Rastreabilidade & Elos com Outros Artefatos (visão consolidada)

| Artefato desta subequipe | Origem / insumo | Elo com | Observação |
| -- | -- | -- | -- |
| [Rich Picture v1](1.ArtefatoGeneralista.md) | Conhecimento prévio dos membros + pesquisa em documentação pública, consolidados na sessão de 25/08 ([Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md)) | [SIG](2.NFRFramework.md) · [BPMN](4.BPMN.md) · [Engenharia Reversa](3.EngenhariaReversa.md) | A cadeia ingestão → transcodificação → empacotamento → CDN → player é o insumo do SIG; os atores viram lanes no BPMN; os protocolos e componentes citados são hipóteses a verificar no FOCO_02 |
| [SIG (NFR)](2.NFRFramework.md) | Cadeia de latência identificada no Rich Picture | [Rich Picture](1.ArtefatoGeneralista.md) · [BPMN](4.BPMN.md) | 🟨 v1 concluído (26/08) — pendente revisão de Pedro Druck |
| [Engenharia Reversa](3.EngenhariaReversa.md) | Hipóteses do Rich Picture (§3.1) + coleta própria de 27/08 (EV-01 a EV-06) | [Rich Picture](1.ArtefatoGeneralista.md) · [SIG](2.NFRFramework.md) · [BPMN](4.BPMN.md) | 🟨 v1 — **confirma** H02–H05, **refuta** H03b (LL-HLS) e H04b (cacheabilidade). Correção do SIG (O04) pendente |
| [Modelo BPMN](4.BPMN.md) | Achados §6 da Engenharia Reversa; atores e fluxos do Rich Picture; fluxos definidos no [Escopo §5](../../../Projeto/EscopoProduto.md#_5-fluxos-selecionados-para-engenharia-reversa--bpmn) | [Rich Picture](1.ArtefatoGeneralista.md) · [SIG](2.NFRFramework.md) · [Engenharia Reversa](3.EngenhariaReversa.md) | 🟨 v1 — 7 diagramas encadeados; **quantifica** o trade-off C01 do SIG |

## 6. Senso Crítico (visão consolidada)

O senso crítico de cada foco está na página dele ([Rich Picture](1.ArtefatoGeneralista.md) · [SIG §7](2.NFRFramework.md#_7-senso-crítico) · [Eng. Reversa §8](3.EngenhariaReversa.md#_8-senso-crítico) · [BPMN §7](4.BPMN.md#_7-senso-crítico)). O que atravessa os quatro:

- **A ordem dos artefatos expôs o custo de desenhar antes de observar.** Rich Picture e SIG foram construídos a partir de conhecimento prévio; a engenharia reversa veio depois e **derrubou duas hipóteses** que já tinham virado nó de SIG (LL-HLS e cacheabilidade do manifesto). O grupo optou por registrar a contradição e corrigir o artefato anterior, em vez de reescrever o histórico — a divergência entre artefatos, quando documentada, é resultado; quando escondida, é erro de rastreabilidade.
- **O softgoal escolhido cobrou um método específico.** Latência não é observável por roteiro de cliques. Ter fixado Performance/Latência no FOCO_01 obrigou o FOCO_02 a descer ao nível de protocolo, e é isso que separa este conjunto de um BPMN de telas.
- **Metade da cadeia continua invisível.** Ingestão e transcodificação não são observáveis por caixa-preta de espectador. Os modelos dizem isso explicitamente, com anotações "NÃO MEDIDO", em vez de estimar.
- **A participação foi desigual entre focos.** O FOCO_01 foi construído em conjunto; o FOCO_02 foi executado por um membro com apoio de IA generativa. A revisão pelos demais é pendência anterior à entrega, e não formalidade: o valor do trabalho depende de mais de um par de olhos sobre a classificação de confiança dos achados.

## 7. Versionamentos & Participações

> Quadro oficial consolidado em [1.2. Participações](../../1.2.ParticipacoesBase.md). Aqui fica o registro detalhado da subequipe, com data e link de commit.

| Membro | Contribuição | Data | Comprobatório (commit/PR) |
| -- | -- | -- | -- |
| Lucas Andrade Zanetti | FOCO_01 · Rich Picture: condução da sessão, mapeamento do pipeline de mídia, legenda de fluxos por cor e recorte do artefato; export, versionamento da imagem e redação da página do foco | 25/08/2026 | [Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#_7-participantes--comprobatórios) |
| Pedro Druck Montalvão Reis | FOCO_01 · Rich Picture: camadas de infraestrutura (servidor de origem, CDN, edge caching, APIs, Auth) e extensões/desenvolvedores externos | 25/08/2026 | [Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#_7-participantes--comprobatórios) |
| Matheus Lemes Amaral | FOCO_01 · Rich Picture: padronização da notação (verbos, tipografia, cores, agrupamentos), desdobramento VOD/Clips e recorte da monetização externa | 25/08/2026 | [Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#_7-participantes--comprobatórios) |
| Heitor Macedo Ricardo | FOCO_01 · Rich Picture: camada de chat/moderação (chat, moderadores, AutoMod, Pub/Sub), camada de monetização, correção terminológica do encoder e revisão de layout/recorte | 25/08/2026 | [Ata S1_02](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md) · [Gravação](https://www.youtube.com/watch?v=7sRz8l8YtqU) · [FOCO_01 §7](1.ArtefatoGeneralista.md#_7-participantes--comprobatórios) |
| Lucas Andrade Zanetti | FOCO_01 · SIG (NFR Framework): condução da sessão, construção do ramo Desempenho/Baixa Latência (ingestão, transcodificação, LL-HLS/WebRTC/CDN própria/peering/origin shield, buffer/ABR), explicação do padrão Pub/Sub, redação da ata e da página do foco | 26/08/2026 | [Ata S1_03](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md) · [Gravação](https://www.youtube.com/watch?v=n36T4kpz-Bk) · [FOCO_01 · NFR §8](2.NFRFramework.md#_8-participantes--comprobatórios) |
| Heitor Macedo Ricardo | FOCO_01 · SIG (NFR Framework): revisão da notação do NFR Framework para o grupo, construção do ramo Segurança, apoio no ramo Usabilidade, condução da integração espacial dos quatro ramos | 26/08/2026 | [Ata S1_03](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md) · [Gravação](https://www.youtube.com/watch?v=n36T4kpz-Bk) · [FOCO_01 · NFR §8](2.NFRFramework.md#_8-participantes--comprobatórios) |
| Matheus Lemes Amaral | FOCO_01 · SIG (NFR Framework): construção dos ramos Confiabilidade (degradação graciosa, microsserviços replicados, tolerância a falha de PoP) e Usabilidade/Interatividade, reclassificação da contribuição da degradação graciosa de HELP para MAKE | 26/08/2026 | [Ata S1_03](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md) · [Gravação](https://www.youtube.com/watch?v=n36T4kpz-Bk) · [FOCO_01 · NFR §8](2.NFRFramework.md#_8-participantes--comprobatórios) |

| Lucas Andrade Zanetti | FOCO_02 · Engenharia Reversa e BPMN: definição do recorte e do protocolo de coleta, execução das 13 etapas, ferramentas de coleta/anonimização/geração, especificação dos 7 diagramas e redação das duas páginas do foco | 27/08/2026 | [FOCO_02 · Eng. Reversa §9](3.EngenhariaReversa.md#_9-participantes--comprobatórios) · [FOCO_02 · BPMN §8](4.BPMN.md#_8-participantes--comprobatórios) |

> ⚠️ **O FOCO_02 ainda não tem revisão de segundo membro.** As linhas de Heitor, Matheus e Pedro Druck nas páginas de [Engenharia Reversa](3.EngenhariaReversa.md#_9-participantes--comprobatórios) e [BPMN](4.BPMN.md#_8-participantes--comprobatórios) estão abertas e precisam ser preenchidas antes da entrega.

> **Pedro Druck Montalvão Reis não participou da sessão do SIG (26/08/2026)** e não consta nas linhas acima referentes a este artefato; permanece registrado nas linhas do Rich Picture (25/08/2026) e fica designado para revisar o SIG publicado ([Ata S1_03 §10](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md#_10-ausência-de-pedro-druck-e-encaminhamento)).

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do relatório da SubEquipe_01 | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 23/08/2026 | Composição da subequipe, escopo trabalhado (Rich Picture, softgoal e fluxos) e metodologia da subequipe, a partir da Ata S1_01 | [SubEquipe_01](../../../Projeto/Atas/Atas_Sg1/ata-S1-01-2026-08-23.md) | Lucas Andrade Zanetti |
| 1.2 | 25/08/2026 | Registro das sessões de trabalho, ferramenta de modelagem, rastreabilidade consolidada e participações do FOCO_01 após a conclusão do Rich Picture v1 | [SubEquipe_01](../../../Projeto/Atas/Atas_Sg1/ata-S1-02-2026-08-25.md#participantes) | Lucas Andrade Zanetti |
| 1.4 | 27/08/2026 | Registro da quarta sessão de trabalho (FOCO_02): engenharia reversa v1 com 6 evidências, 7 diagramas BPMN encadeados, rastreabilidade atualizada, senso crítico consolidado e participações do FOCO_02 | Lucas Andrade Zanetti | _(pendente)_ |
| 1.3 | 26/08/2026 | Registro da terceira sessão de trabalho (SIG v1), rastreabilidade e participações do FOCO_01 após a conclusão do SIG; Pedro Druck ausente nesta sessão | [SubEquipe_01](../../../Projeto/Atas/Atas_Sg1/ata-S1-03-2026-08-26.md#participantes) | Lucas Andrade Zanetti |
