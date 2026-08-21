# Padrão de Assets & Imagens

Todas as imagens dos artefatos ficam **versionadas no repositório**, nunca apenas em link externo (Drive, Figma público etc. podem sair do ar no dia da apresentação — e a diretriz recomenda baixar o conteúdo com antecedência).

## Estrutura

| Pasta | Conteúdo |
| -- | -- |
| `assets/artefatos/` | Rich Pictures e Mapas Mentais (FOCO_01) |
| `assets/nfr/` | SIGs na notação do NFR Framework (FOCO_01) |
| `assets/engenharia-reversa/` | Capturas de tela e evidências da exploração (FOCO_02) |
| `assets/bpmn/` | Diagramas BPMN exportados (FOCO_02) |

## Convenção de nomes

```
subequipe_<NN>_<tipo>[-<sequencia>].<ext>
```

Exemplos:

```
subequipe_01_artefato-generalista.png
subequipe_02_sig.png
subequipe_03_bpmn.png
subequipe_01_evidencia-01.png
```

## Regras

- **Formato**: `.png` para diagramas (fundo branco, sem transparência), `.jpg` apenas para fotos;
- **Legibilidade**: largura mínima de 1600px em diagramas densos — se o texto não for legível com zoom, o artefato não conta;
- **Arquivo-fonte**: versionar também o editável (`.drawio`, `.bpmn`, `.xmind`, `.png` do Miro não substitui o fonte) na mesma pasta;
- **Versões**: ao substituir um artefato, sobrescrever o arquivo e registrar a mudança no *Histórico de Versões* da página correspondente — o histórico do Git é o comprobatório;
- **Legenda**: toda figura na documentação leva legenda com número, descrição, autor(es) e data.

## Referência em markdown

Dentro de uma página de subequipe (`Base/Relatorios/<SubEquipe>/`), o caminho relativo é:

```markdown
![Descrição](../../../assets/bpmn/subequipe_01_bpmn.png)
```
