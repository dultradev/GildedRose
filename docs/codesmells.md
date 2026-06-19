# Code Smells Identificados — Gilded Rose Refactoring Kata

Este documento cataloga os *code smells* presentes no código legado, organizados por categoria. Para cada smell, são descritos o conceito geral, onde ele aparece no Gilded Rose e qual é o seu impacto real na base de código.

---

## Sumário

| ID | Smell | Categoria | Princípio Violado |
|----|-------|-----------|-------------------|
| CS-01 | Long Method | Bloater | SRP |
| CS-02 | Primitive Obsession | Bloater | — |
| CS-03 | Switch Statements | OO Abuser | OCP |
| CS-04 | Divergent Change | Change Preventer | SRP |
| CS-05 | Feature Envy | Coupler | Encapsulamento |

---

## Bloaters — Inchados

> Códigos, métodos e classes que cresceram tanto que se tornaram impossíveis de gerenciar.

---

### CS-01 — Long Method

**O que é**

Ocorre quando um método centraliza tantas linhas de código e responsabilidades que se torna uma unidade monolítica. Métodos longos são difíceis de ler, manter e testar. Em geral, se um método tem mais de dez linhas ou exige comentários internos para explicar o que blocos específicos fazem, ele é um forte candidato a esse smell.

**Onde está no Gilded Rose**

No método `update_quality` da classe `GildedRose`. Ele gerencia o ciclo de atualização completo de todos os itens do inventário de uma só vez, resultando em um emaranhado de indentação profunda — o efeito conhecido como **Arrow Anti-Pattern** (ou *Seta da Perdição*).

> **Arrow Anti-Pattern:** o código se move horizontalmente para a direita devido ao recuo excessivo de múltiplos `if`s aninhados, criando o formato visual de uma seta ou pirâmide. Isso destrói a legibilidade do Python, que depende crucialmente da indentação como elemento semântico da linguagem.

```python
# Exemplo do padrão visual gerado (Arrow Anti-Pattern)
for item in self.items:
    if item.name != "Aged Brie":
        if item.name != "Backstage passes...":
            if item.quality > 0:
                if item.name != "Sulfuras...":
                    item.quality -= 1   # ← nível 4 de indentação
```

**Impacto**

Destrói a legibilidade do código. O esforço mental para rastrear o fluxo de execução de um único item através dos múltiplos níveis de condicionais aninhadas é exaustivo. Além disso, o risco de introduzir efeitos colaterais ao alterar qualquer linha central é altíssimo.

---

### CS-02 — Primitive Obsession

**O que é**

O hábito de usar tipos de dados primitivos da linguagem (strings, inteiros, dicionários puros) para representar conceitos do domínio do negócio que possuem suas próprias regras e validações — em vez de criar pequenos objetos dedicados.

**Onde está no Gilded Rose**

- **Identificação por string pura:** o sistema diferencia tipos de itens mágicos através do campo `item.name` comparado a literais de texto (`item.name == "Aged Brie"`).
- **Limites como inteiros soltos:** os campos `quality` e `sell_in` são `int` puros, deixando a responsabilidade de validar os limites (`0` e `50`) dispersa no meio de equações lógicas espalhadas pelo método.

**Impacto**

Fragilidade extrema contra erros de digitação. Se o nome de um item chegar como `"aged brie"` (minúsculas) ou com um espaço extra, o sistema falhará silenciosamente — tratando-o como item comum sem nenhum aviso. Além disso, as regras de limite precisam ser repetidas matematicamente em vários pontos do código em vez de serem validadas pelo próprio tipo do dado.

---

## Object-Orientation Abusers — Abusadores de Orientação a Objetos

> Ocorre quando as possibilidades da orientação a objetos são ignoradas ou substituídas por lógica puramente procedimental.

---

### CS-03 — Switch Statements

**O que é**

Ocorre quando o código utiliza sequências longas de `if/elif/else` para ramificar o comportamento com base no tipo ou propriedade de um objeto. Em sistemas orientados a objetos, essa ramificação deve ser substituída por **Polimorfismo**.

**Onde está no Gilded Rose**

O método `update_quality` realiza checagens explícitas e repetitivas de strings espalhadas por toda a sua extensão:

```python
if item.name != "Aged Brie" and item.name != "Backstage passes...":
    ...
if item.name == "Sulfuras, Hand of Ragnaros":
    ...
if item.name == "Aged Brie" or item.name == "Backstage passes...":
    ...
```

**Impacto**

Violação direta do **Princípio do Aberto/Fechado (OCP)**:

> *"Entidades de software devem estar abertas para extensão, mas fechadas para modificação."*

O código está fechado para expansão. Para adicionar o item *Conjured*, é necessário caçar os pontos exatos da árvore de `if`s e injetar novas checagens de string — aumentando a fragilidade do sistema e quebrando o encapsulamento a cada nova categoria de item.

---

## Change Preventers — Impedidores de Mudança

> Problemas que fazem com que alterar o código em um lugar exija modificações em vários outros lugares, gerando medo de mexer no sistema.

---

### CS-04 — Divergent Change

**O que é**

Manifesta-se quando uma mesma classe ou método precisa ser alterada por motivos completamente diferentes e independentes sempre que o negócio evolui. É um sintoma claro de que o código mistura conceitos que deveriam estar separados.

**Onde está no Gilded Rose**

Na classe `GildedRose` e especificamente no método `update_quality`. Ele acumula quatro responsabilidades distintas ao mesmo tempo:

1. Descobrir o tipo do item
2. Atualizar a qualidade com base no tipo
3. Atualizar o prazo de venda (`sell_in`)
4. Garantir que os limites (`0` e `50`) sejam respeitados

Se a regra do *Aged Brie* mudar, você altera `update_quality`. Se a regra dos ingressos mudar, você altera o exato mesmo método no mesmo arquivo.

**Impacto**

Violação do **Princípio da Responsabilidade Única (SRP)**:

> *"Uma classe deve ter apenas uma razão para mudar."*

Em equipes reais, a Modificação Divergente gera conflitos constantes de mesclagem de código (*merge conflicts*) quando múltiplos desenvolvedores implementam regras de itens diferentes ao mesmo tempo no mesmo arquivo.

---

## Couplers — Acopladores

> Smells que causam acoplamento excessivo entre classes, fazendo com que uma conheça detalhes íntimos demais da outra.

---

### CS-05 — Feature Envy

**O que é**

Ocorre quando um método de uma classe passa mais tempo acessando e manipulando dados de outra classe do que os seus próprios. É uma quebra do princípio clássico da Orientação a Objetos: *"mantenha os dados e os comportamentos que os usam no mesmo lugar."*

**Onde está no Gilded Rose**

A classe `GildedRose` passa o tempo todo inspecionando e alterando diretamente as propriedades internas da classe `Item`:

```python
item.name      # inspecionando o tipo
item.quality   # lendo e escrevendo o valor
item.sell_in   # lendo e escrevendo o prazo
```

A classe `Item`, por sua vez, age apenas como um contêiner de dados passivo — uma *Data Class* sem comportamento próprio.

**Impacto**

Violação do **Encapsulamento** e geração de alto acoplamento. A classe `GildedRose` sabe detalhes íntimos demais de como um `Item` funciona internamente. Se a estrutura de `Item` precisar mudar no futuro, toda a lógica de negócio centralizada em `GildedRose` será quebrada em cascata.

---

## Mapa de Resolução — Smell × Padrão Aplicado

| Smell | Onde aparece | Padrão / Técnica de Resolução |
|-------|-------------|-------------------------------|
| CS-01 Long Method | `update_quality` | Extract Method → Strategy Pattern |
| CS-02 Primitive Obsession | `item.name`, `item.quality` | Strategy Pattern + Guard Clauses |
| CS-03 Switch Statements | Condicionais de `item.name` | Polimorfismo via Strategy + Factory |
| CS-04 Divergent Change | Classe `GildedRose` | Segregação de responsabilidades (SRP) |
| CS-05 Feature Envy | `GildedRose` → `Item` | Encapsulamento via Strategy Pattern |