# Instruções para o Claude

## Contexto

Projeto de portfólio do Vitor: detecção de fraude em reembolso de plano de saúde.
- Visão geral, arquitetura e decisões: `README.md`
- Estado atual, perguntas em aberto e histórico: `docs/06-diario/diario.md`
- Índice de toda a documentação: `docs/README.md`

**Leia `README.md` e o diário antes de qualquer tarefa.**

Vamos construir este projeto juntos, mas o Vitor precisa saber **cada passo e o porquê de cada parte**. Por isso, tudo que for feito é explicado por escrito dentro de `docs/`, em português simples, no arquivo certo (ver "Organização de `docs/`").

O objetivo do projeto é conseguir o primeiro emprego (estágio/júnior em dados/IA). O Vitor precisa **defender o projeto em entrevista**: explicar cada decisão, mexer ao vivo e refazer partes sozinho.

## Modo de trabalho

- Você pode acelerar o código, mas **cada bloco precisa ser entendido** pelo Vitor. Depois de entregar algo, pergunte o que ele faz e por quê.
- Antes de uma etapa nova, peça que ele descreva o fluxo em palavras ou em caixas e setas.
- Trabalhe em **blocos pequenos e testáveis**. Não avance sem o bloco anterior funcionando.
- **Sempre teste antes de criar.** Antes de adicionar algo ao projeto, experimente numa pasta temporária (fora do repositório) e confirme que funciona. Depois de adicionar, rode `python -m pytest` e o comando afetado. Nunca diga que algo está pronto sem ter rodado; se não deu para testar, diga isso e registre em `docs/05-problemas-e-pendencias/`.
- Todo código novo vem com teste em `tests/`.
- Quando ele propuser uma ideia, questione: o que acontece com dado nulo? E com dado errado? Qual a alternativa mais simples?
- Erros: explique o que a mensagem significa e pergunte o que ele acha que causou, antes de dar a solução.
- Fatos sobre bibliotecas, APIs, preços e limites: **verifique na documentação**, não responda de memória.

## Regras do projeto

- Linguagem: Python.
- Segredos (chave do OpenRouter etc.) ficam em `.env`. O `.env` deve estar no `.gitignore` e **nunca** vai para o GitHub.
- Cada camada do pipeline salva a sua saída, para permitir isolar falhas.
- Não usar números de marketing (ex.: "1000x mais rápido") como argumento.

## Organização de `docs/`

| Pasta | O que vai nela |
|---|---|
| `01-resumo-do-projeto/` | Apresentação em slides, visão geral e glossário |
| `02-como-funciona/` | Arquitetura, guia do código arquivo por arquivo e o que os testes provam |
| `03-decisoes/` | Um arquivo por decisão técnica (copiar `modelo.md`, numerar em sequência, nunca apagar; se mudar, criar outra que substitui) |
| `04-roadmap/` | Etapas com status e critério de "pronto" |
| `05-problemas-e-pendencias/` | Erros e limitações encontrados e o que fazer com cada um |
| `06-diario/` | Estado atual, perguntas em aberto e histórico de cada passo |
| `07-defesa-em-entrevista/` | Perguntas difíceis com respostas |

`docs/` está no `.gitignore`: é material de estudo local do Vitor.

## Ao terminar uma etapa (ou qualquer mudança no código)

- Atualize `docs/06-diario/diario.md`: o que foi feito, o porquê, **como foi testado** e o que se aprendeu.
- Escolha que alguém poderia questionar: novo arquivo em `docs/03-decisoes/`.
- Erro ou limitação encontrada: registre em `docs/05-problemas-e-pendencias/problemas-encontrados.md`.
- Arquivo novo ou alterado: atualize `docs/02-como-funciona/guia-do-codigo.md` e, se houver teste novo, `testes.md`.
- Marque a etapa em `docs/04-roadmap/roadmap.md` e no roadmap do `README.md`.
- Mova para "respondidas" as perguntas em aberto que foram resolvidas, junto com a resposta do Vitor.