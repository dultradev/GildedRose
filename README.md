# Gilded Rose Refactoring Kata

> Refatoração completa de um script procedural legado em um sistema desacoplado, extensível e de alta performance — usando **Arquitetura Limpa** e **Padrões de Projeto GoF**.

📄 **Documentação completa** (decisões arquiteturais, diário de bordo, relatórios de auditoria):
[Notion — Gilded Rose Kata](https://brainy-manchego-171.notion.site/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2)

---

## Estrutura de Pastas

O projeto segue os princípios da Arquitetura Limpa, separando estritamente o **Domínio** (regras puras de negócio), os **Casos de Uso** (orquestração) e a **Infraestrutura** (adaptadores e ponto de entrada legado).

```text
gildedrose/
├── src/
│   ├── domain/
│   │   ├── constants.py               # Limites globais (MAX_QUALITY, MIN_QUALITY)
│   │   ├── entities.py                # Entidade Item (legada/preservada)
│   │   └── strategies/
│   │       ├── base.py                # Interface abstrata UpdateStrategy
│   │       ├── aged_brie.py
│   │       ├── backstage_passes.py
│   │       ├── common.py
│   │       ├── conjured.py            # Fase 5 — item Conjured
│   │       └── sulfuras.py
│   │
│   ├── use_cases/
│   │   ├── factory.py                 # Fábrica polimórfica com Flyweight Cache
│   │   └── update_inventory.py        # Caso de uso principal
│   │
│   └── infrastructure/
│       └── gilded_rose_adapter.py
│
├── tests/
│   ├── test_gilded_rose.py            # Testes unitários e de regressão
│   ├── test_conjured.py               # Testes específicos do item Conjured
│   └── approved_files/                # Artefatos do Golden Master (Approval Tests)
│
├── docs/
│   ├── codesmells.md                   # Code Smells encontrados
│   ├── contigencyplan.md               # Plano de contigência
│   ├── risks.md                        # Riscos possíveis
│   └── requisitos.md                   # RF's e RNF'S
│   └── testimages/                     # Prints dos Testes
│
├── gilded_rose.py                     # Facade / ponto de entrada legado
├── texttest_fixture.py                # Simulação interativa por linha de comando
└── requirements.txt
```

---

## Decisões de Design

### 1. Cláusulas de Guarda

O aninhamento profundo de `if/else` foi substituído por validações e retornos antecipados. Isso eliminou a complexidade ciclomática e tornou os limites de qualidade (`0` e `50`) explícitos logo na entrada do fluxo.

### 2. Padrão Strategy

Toda a lógica de atualização foi extraída para classes especialistas que herdam de `UpdateStrategy`. A classe principal deixou de acumular o conhecimento de todos os tipos de item, respeitando o **SRP (Single Responsibility Principle)**.

### 3. Flyweight Cache na Fábrica

A `ItemStrategyFactory` utiliza o padrão Flyweight: estratégias são *stateless* e instanciadas uma única vez, sendo reutilizadas via `_flyweight_cache`. Isso reduz pressão no Garbage Collector em inventários grandes.

### 4. Matching por Substring vs. Match Exato

A fábrica distingue dois comportamentos na resolução de estratégias:

- **Substring (`in`):** usado para `"Aged Brie"`, `"Backstage passes"` e `"Conjured"` — permite que novos produtos da mesma categoria sejam criados sem alterar o código.
- **Match exato (`==`):** reservado para `"Sulfuras, Hand of Ragnaros"` — evita que réplicas recebam indevidamente os privilégios de um item lendário único.

### 5. Princípio Aberto/Fechado na Prática

A adição do item **Conjured** (Fase 5) validou a arquitetura: foi necessário apenas criar uma nova classe de estratégia e adicionar uma entrada na fábrica. **Nenhuma linha de regra existente foi alterada**, eliminando o risco de regressão.

---

## Executando o Projeto

### Pré-requisitos

- Python 3.10+
- `venv` disponível no PATH

```bash
python --version  # deve retornar 3.10 ou superior
```

### Setup

```bash
git clone https://github.com/dultradev/GildedRose/tree/develop
cd gildedrose

# Linux / macOS
python3 -m venv venv && source venv/bin/activate

# Windows (PowerShell)
python -m venv venv; .\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Rodando os Testes

```bash
pytest
```

### Simulação de Inventário

```bash
python texttest_fixture.py 30  # simula 30 dias
```

---

## Cobertura de Testes

| Tipo | Quantidade | Descrição |
|------|-----------|-----------|
| Regressão histórica | 12 | Limites e comportamentos do código original |
| Expansão (Conjured) | 3 | Comportamento e travas do novo item |
| Approval Test global | 1 | Validação da saída completa contra o Golden Master |

---

## Tecnologias

- **Python 3.10+**
- **pytest** — testes unitários e de regressão
- **approvaltests** — Golden Master / Approval Tests
