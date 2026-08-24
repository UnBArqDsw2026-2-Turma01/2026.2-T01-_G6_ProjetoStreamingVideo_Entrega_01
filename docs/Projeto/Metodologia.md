# Metodologia & Processo de Trabalho

> A diretriz cobra **Metodologia** em cada relatório de subequipe e valoriza, para menções superiores, "rastros claros para o trabalho em equipe (ex. vídeos das reuniões e atas bem elaboradas), evidenciando práticas metodológicas (ex. reuniões periódicas das metodologias ágeis; checklists; debates)".
>
> Esta página descreve o processo **do grupo todo**. Cada subequipe complementa com a metodologia específica de cada foco, no seu relatório.

## 1. Abordagem Adotada

| Item | Definição |
| -- | -- |
| Abordagem/metodologia | **Processo ágil incremental, com *timebox* externo e execução paralela em subequipes**, sincronizada em marcos. Inspirado no Scrum quanto aos rituais e ao papel de liderança distribuída, sem adotar o framework completo. |
| Justificativa (com referência) | Ver [§1.1](#11-por-que-esta-abordagem) abaixo. Fontes: [R06, R07, R08 e R09](Referencias.md#2-fontes-metodológicas) |
| Cadência de reuniões | Reunião **geral** na abertura e no fechamento de cada entrega; cada subequipe define sua própria cadência interna (decisão D10 da [Ata 01](Atas/ata-01-2026-08-22.md)) |
| Canal de comunicação | Teams e WhatsApp — comunidade no WhatsApp com grupo geral e um grupo por subequipe (decisão D09 da [Ata 01](Atas/ata-01-2026-08-22.md)) |
| Ferramenta de gestão de tarefas | Teams, com o [Checklist da Entrega 1](ChecklistEntrega1.md) versionado no GitPages como quadro de acompanhamento visível a todos |

### 1.1. Por que esta abordagem

**O que caracteriza o processo adotado**

| Elemento | Como se manifesta aqui |
| -- | -- |
| *Timebox* fixo e externo | O prazo da entrega é dado pela disciplina e não é negociável. O escopo é a única variável de ajuste — daí a distinção explícita entre entrega mínima e iniciativas extras. |
| Incremento por entrega | Cada módulo da disciplina (Base → Modelagem → Padrões → DAS) é um incremento sobre o mesmo produto, e não um trabalho isolado. O que é decidido agora (escopo, recortes) é insumo dos módulos seguintes. |
| Execução paralela com sincronização em marcos | As três subequipes trabalham simultaneamente sobre recortes distintos e se sincronizam na abertura e no fechamento, não continuamente. |
| Revisão por pares | Todo material entra na `main` por Pull Request, com revisor — o que torna a revisão um ritual do processo, não uma etapa final. |
| Rastro como parte do processo | Atas, gravações e histórico de versões são produzidos durante o trabalho, não reconstruídos no fim. |

**Por que não uma coordenação central única**

A equipe tem 11 membros. Coordenar todos em um único fluxo de decisão faria o custo de comunicação crescer de forma quadrática em relação ao número de pessoas — o argumento clássico de Brooks (R08) sobre por que adicionar pessoas a um trabalho atrasado o atrasa ainda mais. A divisão em três subequipes com liderança própria e autonomia de cadência reduz esse custo: a coordenação global acontece só nos marcos, e a coordenação fina fica dentro de grupos de 3 a 4 pessoas.

Isso também é o que sustenta a decisão de **não centralizar a liderança** ([Ata 01, D05](Atas/ata-01-2026-08-22.md)): o representante geral é ponto de contato formal exigido pelas diretrizes, não gargalo de decisão.

**Por que Scrum como inspiração, e não como framework**

Do Scrum (R07) foram aproveitados os rituais de abertura e revisão, a liderança distribuída e o artefato de acompanhamento visível. **Não** foram adotados: papéis formais de *Product Owner* e *Scrum Master*, *sprints* de duração própria (o ciclo é ditado pelo calendário da disciplina) e reuniões diárias — que não fazem sentido para uma equipe que não trabalha em dedicação integral. Adotar o vocabulário sem as condições que o sustentam produziria cerimônia sem benefício, o que contraria o próprio Manifesto Ágil (R06) ao privilegiar processo sobre interação.

**Por que não Design Sprint**

As diretrizes sugerem o *Design Sprint* (R09) como opção para esta primeira etapa. A equipe avaliou e **não adotou**, por incompatibilidade de propósito: o Design Sprint é um processo de cinco dias, com equipe dedicada e co-localizada, voltado a **conceber e validar uma solução nova** por meio de prototipação e teste com usuários. A Entrega 1 é o oposto disso — parte de um sistema **já existente** e faz o caminho de volta, recuperando fluxo e requisitos por Engenharia Reversa. Não há solução a prototipar nem hipótese de produto a validar com usuários nesta etapa.

> ⚠️ Como a sugestão partiu da professora, convém **explicitar essa justificativa na apresentação**, e não apenas deixá-la documentada — a recusa fundamentada de uma sugestão é senso crítico; a recusa silenciosa parece desatenção.

## 2. Ferramentas

| Finalidade | Ferramenta | Observações |
| -- | -- | -- |
| Artefato generalista (Rich Picture / Mapa Mental) | _a definir_ | |
| SIG / NFR Framework | _a definir_ | |
| Modelagem BPMN | Camunda | | |
| Documentação (GitPages) | Docsify | Site em `docs/`    |
| Versionamento | Git + GitHub | |
| Reuniões / gravações | Teams | |

## 3. Fluxo de Versionamento

- **Branches**: `main` protegida; trabalho em `docs/<assunto>` ou `feat/<assunto>`.
- **Commits**: Conventional Commits (`docs:`, `feat:`, `fix:`), assunto no imperativo.
- **Pull Requests**: obrigatório para entrar em `main`, com pelo menos 1 revisor da mesma ou de outra subequipe.
- **Rastro para a entrega**: o link do commit/PR é o **comprobatório** exigido no quadro de participações.


> ⚠️ **Diretriz OBS GERAL_01**: não serão aceitas postagens (commits e melhorias na wiki) **fora do prazo** da entrega. O repositório é fechado para modificações após o prazo.

## 4. Rituais e Registros

| Ritual | Frequência | Registro/comprobatório |
| -- | -- | -- |
| Reunião geral do grupo | Início e Fim de cada Entrega | [Atas](Atas/README.md) |
| Reunião por subequipe | Semanal | [Atas](Atas/README.md) |
| Revisão cruzada de artefatos | A cada 2 semanas | PRs no GitHub |

## 5. Definition of Done da Entrega 1

Um artefato só é considerado pronto quando:

- [ ] Está publicado no GitPages, na página correta da subequipe;
- [ ] Tem imagem legível versionada em `docs/assets/` (não apenas link externo);
- [ ] Tem seção de **descrição/leitura** explicando o que o modelo comunica;
- [ ] Tem seção de **rastreabilidade & elos** com outros artefatos;
- [ ] Tem seção de **senso crítico** (limitações, decisões, alternativas descartadas);
- [ ] Tem **referências** com link e/ou em ABNT;
- [ ] Tem **histórico de versões** preenchido;
- [ ] Tem os **participantes** identificados, com link de commit.

## 6. Referências da Metodologia

Consolidadas em [Referências do Projeto §2](Referencias.md#2-fontes-metodológicas): Manifesto Ágil (R06), Guia do Scrum (R07), Brooks (R08) e Knapp *et al.* (R09).

> **Pendência honesta**: as quatro fontes acima embasam conceitualmente o processo descrito nesta página, mas ainda constam como 🔜 *previstas* — precisam ser efetivamente lidas pelos responsáveis antes da entrega, para que a citação corresponda a consulta real.

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do documento de metodologia | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 22/08/2026 | Definição da abordagem metodológica, justificativa fundamentada e registro das decisões de processo da Reunião Geral 01 | Equipe G6 | Lucas Andrade Zanetti |
| 1.2 | 24/08/2026 | Correção ortográfica e remoção de comentários residuais | Eduardo Lôbo Moreira | Equipe G6 |
