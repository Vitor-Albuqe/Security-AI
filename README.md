# Security-AI# Detecção de Fraude em Reembolso de Plano de Saúde

Sistema que lê documentos de pedidos de reembolso, cruza as informações com dados públicos e usa grafos para encontrar padrões de fraude, entregando ao auditor uma fila de casos suspeitos com o motivo de cada alerta.

> 🚧 Projeto em construção. Veja o [roadmap](#roadmap).

---

## O problema

Fraudes em reembolso encarecem os planos de saúde para todos os beneficiários, por causa do mutualismo.

- O IESS estima prejuízo de **R$ 30 a 34 bilhões** com fraudes de reembolso em 2022.
- A Neurotech, que atende operadoras, encontrou **até 8%** de abusos e fraudes nos reembolsos analisados.

### Tipos de fraude abordados

| Fraude | Como funciona | Como detectar |
|---|---|---|
| Fracionamento de recibo | 1 consulta vira 2 ou mais recibos para reembolsar mais | Cruzando pedidos (mesmo CPF + clínica + data) |
| Reembolso sem desembolso | Paciente não paga; a clínica usa o login dele e fica com o reembolso | Padrões de rede (contas e clínicas em comum) |
| Estado clínico falso | Procedimento estético descrito como médico | Descrição do documento + CNAE da clínica |
| Procedimento não realizado | O recibo existe, o atendimento não | Padrões e cruzamentos |
| Empréstimo de carteirinha | Outra pessoa usa o plano | Padrões de uso |

Um pedido de reembolso reúne documentos **sem formato padrão**: recibos (às vezes escritos à mão), notas fiscais que variam por cidade, Receita Saúde, pedido médico e comprovante de pagamento. Por isso a leitura usa um modelo de visão, e não um extrator baseado em template.

---

## Arquitetura

O projeto segue uma arquitetura em camadas, organizada como um monólito modular. Cada etapa do pipeline tem uma responsabilidade clara, e as integrações externas ficam isoladas para poderem ser substituídas sem alterar as regras de negócio.

```
                     ┌─────────────────────┐
                     │ Interfaces          │
                     │ CLI / API / auditor │
                     └──────────┬──────────┘
                                ▼
┌─────────────────────┐   ┌─────────────────────┐
│ Infraestrutura      │──▶│ Aplicação           │
│ Modelo, fontes,     │   │ Casos de uso e      │
│ Neo4j, persistência │   │ orquestração        │
└─────────────────────┘   └──────────┬──────────┘
      implementa                      ▼
       os ports          ┌─────────────────────┐
                         │ Domínio             │
                         │ Entidades e regras  │
                         └─────────────────────┘
```

O fluxo de negócio é: documento → extração de campos → validação e enriquecimento com dados externos → regras e análise de relações no grafo → caso priorizado e explicado para revisão humana. Cada etapa deve registrar sua saída e sua origem para que resultados possam ser auditados.

### Estrutura do repositório

```text
src/security_ai/
├── config.py               # Configuração por variáveis de ambiente (.env.example)
├── bootstrap.py            # Raiz de composição: escolhe os adaptadores concretos
├── domain/                 # Entidades e regras de negócio, sem dependências externas
│   ├── value_objects/      # CPF e CNPJ validados, conversão de datas e valores
│   ├── entities/           # Documento lido, pedido, prestador, sinal e caso de análise
│   └── services/           # Regras de fraude e pontuação de prioridade
├── application/            # Casos de uso e coordenação do fluxo
│   ├── ports/              # Contratos para leitores, fontes, grafo e armazenamento
│   └── use_cases/          # Ler documento, analisar pedido, listar fila do auditor
├── infrastructure/         # Implementações concretas dos contratos
│   ├── document_reading/   # Leitor do gabarito e leitor OpenRouter (modelo de visão)
│   ├── external_data/      # Cadastro de prestadores (em memória por enquanto)
│   ├── graph/              # Grafo de relações (em memória; Neo4j no roadmap)
│   └── persistence/        # Repositórios (em memória por enquanto)
└── interfaces/             # Pontos de entrada e apresentação
    └── cli/                # `security-ai ler <imagem>`
docs/                       # Explicações, registros de decisão e histórico de alterações
tests/
├── unit/                   # Domínio e casos de uso isolados
├── integration/            # Adaptadores e integrações
└── e2e/                    # Fluxo completo com dados de teste
scripts/                    # Comandos auxiliares de avaliação e desenvolvimento
Data/                       # Documentos de avaliação já existentes
train.jsonl                 # Anotações do conjunto de treino já existente
```

**Direção das dependências:** interfaces chamam casos de uso; casos de uso dependem do domínio e de contratos em `application/ports`; infraestrutura implementa esses contratos. O domínio não conhece provedores de IA, banco de dados, rede ou interface. Assim, por exemplo, a análise pode ser testada com adaptadores em memória sem chamar o modelo ou o Neo4j.

- A saída de cada etapa deve ser preservada com proveniência para facilitar auditoria e diagnóstico.
- A IA gera sinais e explicações; não determina que uma pessoa cometeu fraude. A decisão final é do auditor.
- `Data/` e `train.jsonl` foram mantidos no local atual; a estrutura não move nem altera esses arquivos.

### Como rodar

```bash
pip install -e ".[dev]"
python -m pytest
python -m security_ai ler Data/5c4c46b2-79b6-4ad3-8a1c-93c007fc8b4d.jpeg
```

A explicação de cada parte e o motivo de cada escolha estão em [docs/](docs/README.md).

---

## Decisões de tecnologia

Cada tecnologia passou por um filtro: *o que faz de diferente, em qual parte do problema toca, qual seria a alternativa simples, e se a escolha se justifica.*

| Tecnologia | Papel | Por quê |
|---|---|---|
| **Neo4j** | Camada 3 | Fraudes organizadas acontecem em redes. A fraude aparece nas *relações*, e não em cada transação isolada |
| **Nemotron 3.5 Super VL** (NVIDIA) | Camada 1 | Modelo aberto que lê imagens e PDFs. Acesso gratuito via OpenRouter |
| Python | Todo o pipeline | — |

**Descartadas:** DeepInfer e llm-d (infraestrutura para servir modelos em escala massiva; não é o problema deste projeto).

---

## Dados

Não existem bases públicas de reembolsos reais, por se tratar de dados sensíveis. A estratégia:

1. **[dokki-pagamentos](https://huggingface.co/datasets/gugaio/dokki-pagamentos):** 35 documentos brasileiros (comprovantes e cupons) com gabarito, usados para medir a qualidade da leitura.
2. **Clínicas reais** (dados públicos de CNPJ e cadastros de estabelecimentos) **+ pacientes e recibos sintéticos**, para que o cruzamento externo seja verdadeiro.
3. **Fraudes plantadas** com gabarito conhecido, e recibos sintéticos convertidos em imagem, para testar o sistema de ponta a ponta.

---

## Roadmap

- [x] Definição do problema e pesquisa dos tipos de fraude
- [x] Avaliação de tecnologias
- [x] Inspeção do dataset de teste
- [ ] Avaliação da leitura do Nemotron no dokki-pagamentos
- [ ] Gerador de recibos sintéticos com fraudes plantadas
- [ ] Modelagem do grafo no Neo4j
- [ ] Cruzamento com dados externos
- [ ] Regras de detecção
- [ ] Tela do auditor

---

## Limitações conhecidas

- O dataset de teste é pequeno (35 documentos): cada erro pesa cerca de 3% na métrica.
- O gabarito do dokki-pagamentos contém erros de leitura, que exigem tratamento antes da comparação.
- Dados sintéticos não comprovam desempenho em produção; servem para validar a arquitetura.
- O Nemotron não tem o português como foco de treino; o desempenho em português será medido.

---

## Fontes

- IESS / Abramge (via Milliman): prejuízo de fraudes em reembolso
- Neurotech: plataforma "Inteligência de Reembolso"
- FenaSaúde, Unimed, Abramge: tipos de fraude
- NVIDIA, OpenRouter, Artificial Analysis: Nemotron 3.5
- Neo4j: grafos para detecção de fraude