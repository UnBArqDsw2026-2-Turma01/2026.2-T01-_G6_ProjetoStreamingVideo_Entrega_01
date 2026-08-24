# G7_ProjetoStreamingVideo

**Código da Disciplina**: FGA0208<br>
**Número do Grupo**: 06<br>
**Entrega**: 01 — Desenho de Software (Base)<br>
**Período**: 2026.2 — Turma T01<br>

> ℹ️ **Nomenclatura do projeto**: a lista oficial de projetos (Diretrizes 2026.2 - T01) vincula o tema *Streaming de Vídeo* ao rótulo `G7_ProjetoStreamingVideo`. O repositório foi atualizado para esse rótulo. O **Número do Grupo** (06) é a numeração de matrícula da turma e não muda — ver [Escopo do Produto](Projeto/EscopoProduto.md).

## Alunos
| Matrícula | Aluno | GitHub | SubEquipe |
| -- | -- | -- | -- |
| 241039645 | Lucas Andrade Zanetti | [@Bappoz](https://github.com/Bappoz) | 01 (líder) |
| 241011018 | Davi Severiano Freitas | [@Davi-UnB](https://github.com/Davi-UnB) | 02 (líder) |
| 241025505 | Daniel de Oliveira Lira | [@Daniellira540](https://github.com/Daniellira540) | 02 |
| 241011466 | Mateus Rodrigues Barreto | [@Mateus0xC](https://github.com/Mateus0xC) | 02 |
| 241039073 | Heitor Macedo Ricardo | [@HeitorM50](https://github.com/HeitorM50) | 01 |
| 241011027 | Eduardo Lôbo Moreira | [@EduLoboM](https://github.com/EduLoboM) | 03 |
| 241041302 | Hugo Freitas Silva | [@HugoFreitass](https://github.com/HugoFreitass) | 03 (líder) |
| 241040350 | Philipe Amancio Reis Caetano | [@Phill-Chill](https://github.com/Phill-Chill) | 03 |
| 241040332 | Pedro Druck Montalvão Reis | [@pedruck](https://github.com/pedruck) | 01 |
| 231026545 | Pedro Henrique Freire Rodrigues | [@Pedro-Henrique3](https://github.com/Pedro-Henrique3) | 02 |
| 241031852 | Matheus Lemes Amaral | [@1emes](https://github.com/1emes) | 01 |

> Divisão completa, com papéis e matriz de participação por foco, em [Equipe & Subequipes](Projeto/Equipe.md).

## Sobre

O **G7_ProjetoStreamingVideo** aborda o domínio das **plataformas de streaming de vídeo**, sob as duas ênfases determinadas pela disciplina: **Transmissões ao Vivo** e **Conteúdo UGC** (*User-Generated Content*).

Como fonte de inspiração, a equipe elegeu uma plataforma consolidada de transmissões ao vivo organizada em **canais** — originada na comunidade de jogos eletrônicos e hoje ampliada para música, bate-papo, arte e eventos. Nela, qualquer usuário pode se tornar criador: transmite em tempo real, a audiência interage por um **chat público síncrono**, e o conteúdo transmitido é depois recortado, revisto e redistribuído pela própria comunidade.

A escolha se sustenta no fato de as duas ênfases coexistirem **no mesmo fluxo**: o conteúdo é ao vivo *e* é gerado pelo usuário, ao mesmo tempo. Isso concentra num único domínio tensões arquiteturais que rendem modelagem — latência contra qualidade de vídeo, audiência que varia em ordens de grandeza sem aviso, e moderação que precisa acontecer **enquanto** o conteúdo é produzido, sem o intervalo de revisão que plataformas sob demanda possuem.

> ⚠️ **Conforme as diretrizes da disciplina, o nome real da plataforma de inspiração não é citado em nenhum artefato deste repositório.** A referência é sempre feita por suas características, e o projeto é identificado apenas como `G7_ProjetoStreamingVideo`.

Escopo detalhado — aplicação de referência, público-alvo, funcionalidades e não-escopo — em [Escopo do Produto](Projeto/EscopoProduto.md).

## Entrega 1 — mapa rápido

| Foco | O que a diretriz exige | Onde documentar |
| -- | -- | -- |
| **FOCO_01** — Artefatos Generalistas & NFR Framework | 1 artefato generalista (Rich Picture **ou** Mapa Mental) + 1 SIG na notação do NFR Framework, **por subequipe** | `Base/Relatorios/<SubEquipe>/1.ArtefatoGeneralista.md` e `2.NFRFramework.md` |
| **FOCO_02** — Engenharia Reversa & Modelagem BPMN | Processo de Engenharia Reversa aplicado + 1 modelo BPMN do fluxo encontrado, **por subequipe** | `Base/Relatorios/<SubEquipe>/3.EngenhariaReversa.md` e `4.BPMN.md` |
| **FOCO_03** — IA Generativa | Ponto de vista de **cada membro** sobre lições aprendidas e uso de IA Generativa | `Base/Relatorios/<SubEquipe>/5.IAGenerativa.md` |
| **Transversal** | Participações com comprobatórios (links de commits) | [1.2. Participações](Base/1.2.ParticipacoesBase.md) |
| **Opcional** | Iniciativas extras | [1.3. Iniciativas Extras](Base/1.3.IniciativasExtras.md) |

Acompanhamento de pendências: [Checklist da Entrega 1](Projeto/ChecklistEntrega1.md).

## Screenshots da Primeira Entrega
<!-- PREENCHER: 2 ou mais screenshots dos artefatos produzidos na entrega (ex.: recorte do Rich Picture, recorte do SIG, recorte do BPMN). Imagens em docs/assets/. -->
_A preencher (mínimo 2 screenshots dos artefatos)._

## Há algo a ser executado?

( ) SIM

( **X** ) NÃO

A Entrega 1 (Base) é **documental**: os entregáveis são artefatos de modelagem publicados neste GitPages, sem código de aplicação. O único item executável é o próprio site da documentação, cujas instruções seguem abaixo.

### Executando o GitPages localmente

```shell
npm i docsify-cli -g
docsify serve ./docs
```

O site fica disponível em `http://localhost:3000`.

## Informações Complementares

- **Diretrizes da disciplina**: disponíveis no Aprender3.
- **Processo de trabalho da equipe**: [Metodologia & Processo](Projeto/Metodologia.md).
- **Rastros de reuniões**: [Atas de Reunião](Projeto/Atas/README.md).
- **Convenção de imagens e nomes de arquivo**: [Padrão de Assets](assets/README.md).

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 21/08/2026 | Estruturação inicial do GitPages para a Entrega 1 | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 22/08/2026 | Contextualização do projeto, divisão das subequipes e escopo de execução | [Equipe G7](Projeto/Equipe.md) | Lucas Andrade Zanetti |
| 1.2 | 23/08/2026 | Resolução da pendência de nomenclatura: rótulo do projeto atualizado para G7_ProjetoStreamingVideo, conforme lista oficial de projetos | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
