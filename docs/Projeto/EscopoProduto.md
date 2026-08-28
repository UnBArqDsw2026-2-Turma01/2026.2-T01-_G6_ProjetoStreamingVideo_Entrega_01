# Escopo do Produto — G7_ProjetoStreamingVideo

> **Tema oficial**: Streaming de Vídeo, com ênfase em **Transmissões ao Vivo** e **Conteúdo UGC** (*User-Generated Content*), baseado em qualquer streaming de vídeo para inspiração, podendo ser em versão site, desktop ou aplicativo móvel.
>
> **Restrição da diretriz**: **não usar o nome real da fonte de inspiração**. Referenciar sempre como *"aplicação de referência"* ou *"plataforma inspiradora"*.

Esta página é a **fonte única de verdade do escopo**. Todos os artefatos das subequipes (Rich Picture / Mapa Mental, SIG, BPMN) devem rastrear para os itens definidos aqui.

## 1. Identidade do Projeto

| Campo | Valor |
| -- | -- |
| Nome do projeto | `G7_ProjetoStreamingVideo` |
| Plataforma-alvo (site / desktop / mobile) | **Site (aplicação web)** — versão de navegador da aplicação de referência |
| Aplicação de referência (descrição, sem nome real) | Plataforma consolidada de **transmissões ao vivo organizadas em canais**, originada na comunidade de jogos eletrônicos e hoje ampliada para música, bate-papo, arte e eventos. Qualquer usuário pode se tornar criador: transmite em tempo real, a audiência interage por um **chat público síncrono**, e o conteúdo transmitido pode ser recortado em trechos curtos e revisto sob demanda após a transmissão. A receita combina inscrições recorrentes em canais, doações via moeda virtual e publicidade. |
| Justificativa da escolha da referência | É uma das poucas plataformas em que as **duas ênfases exigidas pela disciplina coexistem no mesmo fluxo**: o conteúdo é ao vivo *e* é gerado pelo usuário, simultaneamente. Isso concentra, num único domínio, tensões arquiteturais ricas para modelagem — latência versus qualidade de vídeo, escala de audiência imprevisível, e moderação de conteúdo que precisa acontecer **enquanto** o conteúdo é produzido, sem o intervalo de revisão que plataformas sob demanda possuem. A versão web foi escolhida por ser acessível a todos os membros sem instalação, favorecendo a Engenharia Reversa distribuída entre 11 pessoas. |

## 2. Ênfases Obrigatórias do Tema

| Ênfase | O que significa para o nosso recorte | Onde isso aparece nos artefatos |
| -- | -- | -- |
| Transmissões ao Vivo | O conteúdo é consumido **enquanto é produzido**: não há etapa de processamento prévio, revisão ou publicação. Isso impõe restrições que não existem em vídeo sob demanda — o atraso entre criador e espectador é percebido diretamente na interação por chat, a audiência de um canal varia em ordens de grandeza sem aviso, e uma falha não pode ser corrigida por nova tentativa: a transmissão perdida é perdida. | A mapear por cada subequipe (ver §5 e §6) |
| Conteúdo UGC (User-Generated Content) | A plataforma **não produz o conteúdo**: ela oferece a infraestrutura para que usuários o produzam, e o próprio público o reprocessa (recortes, compartilhamento, comentários). Isso desloca responsabilidades para a plataforma — verificação de identidade e elegibilidade do criador, moderação em tempo real do que é transmitido e do que é escrito no chat, tratamento de direitos autorais de terceiros embutidos na transmissão, e repasse financeiro a criadores. | A mapear por cada subequipe (ver §5 e §6) |

> As ênfases do tema devem ser **visíveis** nos artefatos. Ex.: um SIG de *Desempenho* ou *Disponibilidade* faz sentido direto com "ao vivo"; um SIG de *Moderação/Segurança de Conteúdo* faz sentido direto com "UGC".

## 3. Público-Alvo

| Perfil | Descrição | Necessidades principais | Fonte do levantamento |
| -- | -- | -- | -- |
| **Criador de conteúdo** | Usuário que transmite ao vivo em seu próprio canal, de forma amadora ou profissional. Vai do iniciante sem audiência ao criador com contrato e equipe de apoio. | Transmitir com qualidade e estabilidade; acompanhar e interagir com a audiência durante a live; construir audiência recorrente; monetizar o canal; delegar moderação | Levantamento inicial da equipe — **a validar e detalhar na Engenharia Reversa** |
| **Espectador** | Usuário que consome transmissões, com ou sem conta. O espectador anônimo assiste; o autenticado interage, segue e se inscreve em canais. | Descobrir conteúdo relevante; assistir sem travamentos; participar do chat; ser avisado quando um canal segue entra ao vivo; rever o que perdeu | Levantamento inicial da equipe — **a validar e detalhar na Engenharia Reversa** |
| **Moderador de canal** | Espectador de confiança a quem o criador delega poderes sobre o chat do seu canal. Não é funcionário da plataforma. | Agir sobre mensagens e usuários em tempo real; aplicar as regras definidas pelo criador; ter ferramentas que funcionem sob alto volume de mensagens | Levantamento inicial da equipe — **a validar e detalhar na Engenharia Reversa** |
| **Equipe de confiança da plataforma** | Perfil interno responsável pelas políticas de conteúdo, atuando acima dos canais individuais. | Aplicar políticas de forma consistente; responder a denúncias; suspender contas e conteúdo; auditar decisões | Levantamento inicial da equipe — **a validar e detalhar na Engenharia Reversa** |

## 4. Principais Funcionalidades Levantadas

> **Levantamento preliminar**, feito por observação superficial da aplicação de referência, apenas para dar ponto de partida às subequipes e evitar sobreposição na divisão dos fluxos. **Não substitui a Engenharia Reversa**: cada funcionalidade só entra como achado depois de investigada e evidenciada na página do foco correspondente. As colunas *Subequipe responsável* e *Artefato(s)* são preenchidas quando a divisão de §5 for fechada.

| # | Funcionalidade | Ênfase relacionada | Subequipe responsável | Artefato(s) |
| -- | -- | -- | -- | -- |
| F01 | Autenticação e gestão de conta | Ambas | | |
| F02 | Configuração e transmissão ao vivo de um canal | Transmissões ao Vivo | | |
| F03 | Consumo de transmissão ao vivo pelo espectador | Transmissões ao Vivo | | |
| F04 | Chat público síncrono do canal | Ambas | | |
| F05 | Descoberta de conteúdo (busca, categorias, canais ao vivo) | UGC | | |
| F06 | Relação com o canal (seguir e inscrever-se) | UGC | | |
| F07 | Notificação de canal ao vivo | Transmissões ao Vivo | | |
| F08 | Recorte de trechos e revisão sob demanda após a transmissão | UGC | | |
| F09 | Moderação de chat e de conteúdo | UGC | | |
| F10 | Monetização (inscrições, moeda virtual, publicidade) | UGC | | |

## 5. Fluxos Selecionados para Engenharia Reversa & BPMN

> A diretriz exige **pelo menos um** fluxo distinto por subequipe. Para não ficar só na Menção Mínima, cada subequipe modela **3 fluxos**, todos ligados ao seu softgoal (seção 6): o primeiro é a entrega mínima, os outros dois são iniciativa extra e entram também em [1.3. Iniciativas Extras](../Base/1.3.IniciativasExtras.md). Evitar sobreposição entre subequipes — registrar a divisão aqui **antes** de começar a modelar.

| Subequipe | Papel | Fluxo escolhido | Justificativa da escolha | Status |
| -- | -- | -- | -- | -- |
| SubEquipe_01 | Mínimo | Assistir Transmissão ao Vivo (player + ingestão + sincronização do chat) | Ponto onde a latência/buffering do "ao vivo" é mais sensível ao usuário | 🟨 modelado (D2) |
| SubEquipe_01 | Extra | Início e Configuração da Transmissão (setup de bitrate/qualidade, handshake com servidor de ingestão) | Desempenho da ingestão é pré-condição para o fluxo de assistir | 🟨 modelado (D1) |
| SubEquipe_01 | Extra | Troca de Qualidade Adaptativa (ABR) durante a exibição | Evidencia desempenho sob variação de rede, critério central de Performance/Latência | 🟨 modelado (D3) |
| SubEquipe_01 | Extra | Ciclo de Reprodução por Segmento, Recuperação de Falha e Sincronização de Tempo Real | Surgiram da própria engenharia reversa: concentram o custo de latência e o tratamento de falha do fluxo mínimo | 🟨 modelados (D2b, D4, D5) |
| SubEquipe_02 | Mínimo | Chat ao Vivo em Tempo Real sob pico de audiência | Disponibilidade sob carga é o teste de estresse mais direto do "ao vivo" | ⬜ |
| SubEquipe_02 | Extra | Doações/Monetização durante a live (pagamento, confirmação, notificação) | Confiabilidade transacional — falha aqui tem custo direto ao usuário | ⬜ |
| SubEquipe_02 | Extra | Recuperação de Falha de Transmissão (reconexão do streamer, failover de ingestão) | Cenário clássico de resiliência/disponibilidade | ⬜ |
| SubEquipe_03 | Mínimo | Login/Cadastro & Autenticação (incl. 2FA/OAuth) | Segurança de acesso é a porta de entrada de todo o sistema | ✅ modelado (Pool 7 · Identidade e Sessões) |
| SubEquipe_03 | Extra | Início de Transmissão com validação de direitos do streamer (proteção de conteúdo) | Segurança de conteúdo, não só de acesso | ✅ modelado (Pool 4 · Fábrica de Vídeo e Ingestão & Pool 13 · Moderação de Vídeo) |
| SubEquipe_03 | Extra | Moderação de Conteúdo UGC (denúncia, banimento, filtragem) | Liga Segurança à ênfase obrigatória de UGC do tema | ✅ modelado (Pool 5 · Chat e AutoMod & Pool 13 · Moderação de Vídeo) |

## 6. Requisitos Não Funcionais Candidatos (insumo para os SIGs)

> Cada subequipe elabora **um SIG** (NFR Framework) sobre um critério de qualidade (*softgoal*) diferente. Registrar a divisão aqui para evitar duplicidade.

| Subequipe | Softgoal / critério de qualidade | Justificativa (por que é crítico neste domínio) | Status |
| -- | -- | -- | -- |
| SubEquipe_01 | Performance / Latência | Streaming ao vivo tolera pouco atraso; é a ênfase "Transmissões ao Vivo" do tema traduzida em NFR | 🟨 SIG v1 · O04 (LL-HLS) a corrigir após a engenharia reversa |
| SubEquipe_02 | Confiabilidade / Disponibilidade | Picos de audiência e transações (doações) exigem robustez a falha e uptime | ⬜ |
| SubEquipe_03 | Confiabilidade, Disponibilidade e Segurança | Autenticação, proteção de conteúdo e moderação de UGC — cobre acesso e a ênfase "Conteúdo UGC" expandida em 5 dimensões e trade-offs | ✅ concluído (SIG v1.0) |

## 7. Fora de Escopo

Recortes deliberados desta entrega, com a razão de cada um:

| # | Fora de escopo | Por quê |
| -- | -- | -- |
| FE01 | Implementação de código do produto | A Entrega 1 (Base) é documental. Implementação entra a partir do módulo de Padrões de Projeto. |
| FE02 | Arquitetura interna de ingestão, transcodificação e distribuição de vídeo | Não é observável pela Engenharia Reversa por caixa-preta que a equipe consegue aplicar. Modelar isso seria especulação apresentada como achado. |
| FE03 | Algoritmo de recomendação e ordenação de conteúdo | Mesma razão de FE02: o comportamento é observável, mas a regra que o produz não é. Pode aparecer como *caixa-preta* nos modelos, nunca como fluxo detalhado. |
| FE04 | Versões desktop, mobile nativa, console e TV | A equipe fixou a **versão web** como recorte (§1) para manter comparabilidade entre os achados das três subequipes. |
| FE05 | Regras contratuais e fiscais de repasse a criadores | Domínio jurídico/financeiro, fora do alcance de observação e alheio às ênfases do tema. |
| FE06 | Uso do nome real e da identidade visual da plataforma de referência | **Vedado pela diretriz da disciplina.** A referência é sempre descrita por características. |

## 8. Referências

Consolidadas em [Referências do Projeto](Referencias.md). Sustentam este escopo, em especial:

- **R01** (documentação oficial de desenvolvedor) e **R02** (arquitetura em ingestão + distribuição) — base da descrição da aplicação de referência em §1 e do levantamento preliminar de funcionalidades em §4;
- **R05** (design de streaming ao vivo, agnóstico de plataforma) — base conceitual das ênfases descritas em §2;
- **R04** (arquitetura de uma plataforma concorrente) — insumo do comparativo previsto como iniciativa extra.

> A avaliação crítica da confiabilidade de cada fonte está em [Referências §1.1](Referencias.md#_11-senso-crítico-sobre-as-fontes) e é o que sustenta os não-escopos **FE02** e **FE03** desta página.

## Histórico de Versões

| Versão | Data | Descrição | Autor(es) | Revisor(es) |
| -- | -- | -- | -- | -- |
| 1.0 | 21/08/2026 | Criação do documento de escopo | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.1 | 22/08/2026 | Definição da aplicação de referência, ênfases, público-alvo, levantamento preliminar de funcionalidades e não-escopo (Reunião Geral 01) | [Equipe G7](Equipe.md) | Lucas Andrade Zanetti |
| 1.2 | 23/08/2026 | Correção da divisão de softgoals e fluxos entre SubEquipe_02 e SubEquipe_03 (§5 e §6) e atualização do rótulo do projeto para G7_ProjetoStreamingVideo | Lucas Andrade Zanetti | Heitor Macedo Ricardo |
| 1.3 | 28/08/2026 | Atualização do status dos fluxos BPMN (13 pools integradas) e softgoals da SubEquipe_03 para concluído (✅) | Eduardo Lôbo Moreira, Hugo Freitas Silva, Philipe Amâncio Reis Caetano | Equipe G7 |
