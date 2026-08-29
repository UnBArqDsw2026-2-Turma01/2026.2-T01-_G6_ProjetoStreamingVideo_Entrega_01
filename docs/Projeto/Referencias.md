# Referências do Projeto

Bibliografia consolidada do grupo, em notação **ABNT** com link direto, conforme as *Diretrizes Complementares* da disciplina ("Apresentar as referências consultadas, com links e/ou especificadas na notação ABNT").

**Legenda de status**: ✅ já consultada · 🔜 prevista, ainda não consultada

> ⚠️ **Nota sobre a citação da fonte de inspiração**
>
> A diretriz proíbe **usar o nome real da fonte de inspiração para nomear ou descrever o projeto** — por isso o projeto se chama `G6_ProjetoStreamingVideo` e todos os artefatos referem-se à plataforma por suas características.
>
> Referências bibliográficas, porém, **não podem ser adulteradas**: título, autoria e URL são reproduzidos exatamente como publicados, sob pena de a citação deixar de ser verificável. O nome comercial aparece portanto **apenas nas entradas bibliográficas abaixo**, nunca na modelagem, na nomenclatura ou na descrição do produto.

## 1. Fontes Técnicas sobre o Domínio (Streaming de Vídeo ao Vivo)

| # | Referência (ABNT) | Natureza da fonte | Status | Uso previsto |
| -- | -- | -- | -- | -- |
| R01 | TWITCH INTERACTIVE, INC. **Twitch Developer Documentation**. [S. l.]: Twitch Interactive, 2026. Disponível em: https://dev.twitch.tv/docs/. Acesso em: 22 ago. 2026. | **Primária e oficial** — documentação do próprio fornecedor | ✅ | Identificar as capacidades expostas da plataforma (API, EventSub, chat, embed, extensões) e delimitar o que é observável externamente |
| R02 | LOPES, Daniel; BAPTISTA, Diogo. **De que é feita?**. In: *Twitch a Microscópio*. [S. l.], [s. d.]. Disponível em: https://danielramoslopes8.wixsite.com/twitchmultimedia/tech. Acesso em: 22 ago. 2026. | **Secundária, não oficial** — trabalho acadêmico de terceiros | ✅ | Hipótese de arquitetura em duas camadas (ingestão e distribuição): encoder, PoP Ingest Proxy, Transcode/Transmux Worker, HLS, Protected Replication e Video Edge |
| R03 | LIVESTREAMNINJA. **Live Streaming Architecture**. [S. l.: s. n.], [s. d.]. 1 vídeo. Publicado pelo canal *livestreamninja*. Disponível em: https://www.youtube.com/watch?v=RvsaosnEHWc. Acesso em: 22 ago. 2026. | **Secundária, não revisada por pares** — conteúdo técnico de terceiros | 🔜 | Vocabulário e visão geral do pipeline de transmissão ao vivo |
| R04 | SINGH, Harshit. **Unveiling the Backbone of YouTube Live Streaming: A Deep Dive into YouTube's Architecture and Real-Time Video Processing**. DEV Community, 29 out. 2024. Disponível em: https://dev.to/wittedtech-by-harshit/unveiling-the-backbone-of-youtube-live-streaming-a-deep-dive-into-youtubes-architecture-and-real-time-video-processing-f6j. Acesso em: 22 ago. 2026. | **Secundária, não oficial** — artigo técnico de terceiros | 🔜 | Contraponto: como uma plataforma concorrente resolve o mesmo problema. Insumo para as [Iniciativas Extras](../Base/1.3.IniciativasExtras.md) |
| R05 | ANAND, Shashank. **How Live Video Streaming Works: A High-Level System Design Breakdown**. The Engineering Author, [s. d.]. Disponível em: https://theengineeringauthor.com/engineering-stories/live-video-streaming-solution. Acesso em: 22 ago. 2026. | **Secundária, agnóstica de plataforma** — artigo de design de sistemas | ✅ | Fundamentação conceitual neutra: captura e codificação (H.264/H.265), empacotamento em segmentos (HLS/MPEG-DASH), servidores de streaming e entrega por CDN. Citado em [Escopo do Produto](EscopoProduto.md#7-referências) |

### 1.1. Senso Crítico sobre as Fontes

Nenhuma das fontes acima, com exceção de **R01**, é oficial. Isso tem três consequências que a equipe assume explicitamente:

1. **R02 não é documentação da plataforma** — é um trabalho acadêmico produzido por dois estudantes. Descreve uma arquitetura *plausível e bem estruturada*, mas de segunda mão e sem data de publicação verificável. Serve como **hipótese de trabalho**, não como fato: qualquer elemento dela que entre num modelo BPMN ou num SIG precisa de corroboração por observação direta (Engenharia Reversa) ou por R01.
2. **R03, R04 e R05 descrevem o domínio, não a aplicação de referência** — R04 trata de outra plataforma e R05 é agnóstico. Fundamentam *como streaming ao vivo funciona em geral*, o que é legítimo para embasar decisões de modelagem, mas não substituem evidência sobre o sistema analisado.
3. **R01 delimita a superfície, não o interior** — a documentação de desenvolvedor descreve o que a plataforma expõe a terceiros, não como ela é implementada internamente. É a fonte mais confiável disponível, e ainda assim insuficiente para afirmar arquitetura interna.

> Consequência metodológica: os achados de arquitetura interna permanecem, nesta entrega, no nível de **inferência declarada como tal**, coerente com o recorte de não-escopo FE02 e FE03 registrado no [Escopo do Produto](EscopoProduto.md).

## 2. Fontes Metodológicas

| # | Referência (ABNT) | Status | Uso realizado / previsto |
| -- | -- | -- | -- |
| R06 | BECK, Kent *et al.* **Manifesto para o desenvolvimento ágil de software**. 2001. Disponível em: https://agilemanifesto.org/iso/ptbr/manifesto.html. Acesso em: 22 ago. 2026. | ✅ | Embasar a escolha por uma abordagem ágil adaptada, em vez de processo prescritivo. Citado em [Metodologia & Processo](Metodologia.md#11-por-que-esta-abordagem) |
| R07 | SCHWABER, Ken; SUTHERLAND, Jeff. **O Guia do Scrum**: o guia definitivo para o Scrum — as regras do jogo. [S. l.: s. n.], 2020. Disponível em: https://scrumguides.org/. Acesso em: 22 ago. 2026. | ✅ | Origem dos rituais adotados (abertura, revisão) e delimitação do que **não** foi adotado. Citado em [Metodologia & Processo](Metodologia.md#11-por-que-esta-abordagem) |
| R08 | BROOKS JR., Frederick P. **The Mythical Man-Month**: essays on software engineering. Anniversary ed. Boston: Addison-Wesley, 1995. | ✅ | Justificar a divisão em subequipes autônomas pelo custo de comunicação em equipes grandes. Citado em [Metodologia & Processo](Metodologia.md#11-por-que-esta-abordagem) |
| R09 | KNAPP, Jake; ZERATSKY, John; KOWITZ, Braden. **Sprint**: how to solve big problems and test new ideas in just five days. New York: Simon & Schuster, 2016. | ✅ | Fundamentar por que o *Design Sprint*, sugerido nas diretrizes, não se aplica ao recorte desta entrega. Citado em [Metodologia & Processo](Metodologia.md#11-por-que-esta-abordagem) |

## 3. Fontes por Artefato

> Referências específicas de cada artefato (NFR Framework, BPMN, Engenharia Reversa, Rich Picture) ficam na página **`6.Referencias.md`** de cada subequipe, junto do artefato que embasam. Esta página consolida as referências transversais e o direcionamento para os relatórios.

| Subequipe | Onde ficam as referências detalhadas | Focos cobertos |
| -- | -- | -- |
| **SubEquipe_01** | [1.1.1 · Referências](/Base/Relatorios/1.1.1.SubEquipe_01/6.Referencias.md) | Rich Picture (Checkland, Monk & Howard), NFR/Desempenho (Chung, Serrano, Pantos, Rescorla), BPMN (OMG, White & Miers), ER (Chikofsky, Pressman, RFC 8216, RFC 9111, W3C MSE, Bentaleb) |
| **SubEquipe_02** | [1.1.2 · Referências](/Base/Relatorios/1.1.2.SubEquipe_02/6.Referencias.md) | Rich Picture (Checkland, Open University), NFR/Confiabilidade (Chung, Serrano, Kleppmann, Stripe, Richardson, Bentaleb), BPMN (OMG), ER (Pressman, Chikofsky, RFC 8216) |
| **SubEquipe_03** | [1.1.3 · Referências](/Base/Relatorios/1.1.3.SubEquipe_03/6.Referencias.md) | Rich Picture (Checkland, Monk & Howard, LGPD, ECA), NFR/Segurança (Chung, Silva, Serrano, Kroop, Huang, RFC 6455 WebSocket, RFC 7519 JWT, RFC 9106 Argon2, OWASP), BPMN (OMG) |

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| :--: | :--: | -- | -- | -- |
| 1.0 | 22/08/2026 | Consolidação das referências técnicas e metodológicas, com classificação de natureza da fonte e senso crítico | [Equipe G6](Equipe.md) | Lucas Andrade Zanetti |
| 1.1 | 23/08/2026 | Atualização do rótulo do projeto para G6_ProjetoStreamingVideo | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.2 | 28/08/2026 | Atualização do status de consulta das fontes técnicas e metodológicas (R05 a R09) e mapeamento cruzado com os relatórios das subequipes | Davi Severiano Freitas | Pedro Henrique Freire Rodrigues |


