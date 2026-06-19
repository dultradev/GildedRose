# Riscos do Projeto — Gilded Rose Refactoring Kata

Este documento cataloga os principais riscos identificados durante o processo de refatoração, suas causas raiz no contexto do Gilded Rose e as estratégias de mitigação adotadas.

---

## Sumário de Riscos

| ID | Risco | Probabilidade | Impacto |
|----|-------|--------------|---------|
| R-01 | Efeito Dominó por Acoplamento Lógico | Alta | Alto |
| R-02 | Quebra de Regras de Negócio Implícitas | Média | Alto |
| R-03 | Violação da Restrição do Goblin | Baixa | Crítico |
| R-04 | Modificação Prematura / Overengineering | Média | Médio |

---

## R-01 — Efeito Dominó por Acoplamento Lógico

### O que é o risco

Alterar a lógica de atualização de um item específico e, acidentalmente, quebrar o comportamento de outro item que não tinha nenhuma relação com a mudança.

### Por que acontece no Gilded Rose

O *Long Method* original usa lógica negativa encadeada para separar os fluxos de execução:

```python
if item.name != "Aged Brie" and item.name != "Backstage passes":
    ...
```

O fluxo de execução de um item depende diretamente de ele **não ser** outro item. Alterar a ordem ou o escopo de um desses `if`s pode silenciosamente fechar a porta de entrada para outra categoria sem nenhum erro de sintaxe — o código continua rodando, mas com comportamento errado.

### Mitigação

- **Rigor na execução de testes:** rodar a suíte completa a cada alteração unitária, por menor que seja — inclusive ao renomear uma variável ou inverter um `if`.
- **Isolamento de alterações por commit:** mudar apenas uma ramificação lógica por vez. Se o trabalho for no fluxo do Aged Brie, o fluxo dos Backstage passes não deve ser tocado no mesmo commit.

---

## R-02 — Quebra de Regras de Negócio Implícitas

### O que é o risco

"Corrigir" o código achando que ele está errado por não bater com a documentação textual, quando na verdade o código legado é a regra de negócio que está rodando em produção.

### Por que acontece no Gilded Rose

Dois exemplos concretos de comportamento implícito não documentado:

| Comportamento | O que a documentação diz | O que o código faz |
|--------------|--------------------------|-------------------|
| Aged Brie pós-vencimento | Aumenta de valor com o tempo | Incrementa `Quality` em **+2** após `SellIn < 0` |
| Sulfuras e `SellIn` | Mantém qualidade em 80 | `SellIn` **nunca é decrementado** — sequer entra no laço geral |

Tentar "limpar" o código decrementando o `SellIn` de todos os itens de forma genérica no início do laço, por exemplo, quebraria silenciosamente o comportamento do Sulfuras.

### Mitigação

- **Abordagem *Bug-for-Bug Compatibility*:** o comportamento do código legado é a verdade absoluta. A documentação textual serve apenas como guia inicial de orientação. Se o teste passou com o código antigo, o código refatorado tem que passar exatamente do mesmo jeito — sem exceções.

---

## R-03 — Violação da Restrição do Goblin *(Quebra de Escopo da Arquitetura)*

### O que é o risco

Desenhar uma solução arquitetonicamente elegante que viola os limites do que é permitido alterar, tornando o projeto inválido perante o cliente.

> ⚠️ Este é o risco de **menor probabilidade**, mas de **impacto crítico**: uma violação invalida todo o projeto independentemente da qualidade do restante da solução.

### Por que acontece no Gilded Rose

A tentação natural ao ver a classe `Item` em Python é:

- Adicionar propriedades ou métodos diretamente nela (`item.update()`)
- Herdar dela para criar subclasses especializadas (`class BrieItem(Item)`)
- Modificar o construtor para receber comportamentos

Todas essas abordagens violam a **Regra do Goblin**: a classe `Item` e a propriedade `Items` são intocáveis.

### Mitigação

- **Strategy Pattern como envelope:** em vez de alterar o `Item`, criamos classes utilitárias que recebem a instância original no construtor e manipulam apenas seus atributos permitidos (`name`, `sell_in`, `quality`):

  ```python
  class AgedBrieStrategy(UpdateStrategy):
      def update(self, item: Item) -> None:
          # Manipula item.quality e item.sell_in
          # sem alterar a classe Item em nenhum momento
          ...
  ```

---

## R-04 — Modificação Prematura / Overengineering

### O que é o risco

Tentar aplicar padrões de projeto complexos desde o primeiro dia, antes de organizar o código base, gerando um sistema novo tão confuso quanto o original.

### Por que acontece no Gilded Rose

É comum o impulso de criar imediatamente Factories, meta-classes ou hierarquias de polimorfismo antes mesmo de extrair os métodos do código legado — pulando etapas que garantem a legibilidade como pré-condição para a arquitetura.

O resultado é uma arquitetura "certa no papel" assentada sobre uma base ilegível, o que torna a depuração e os testes significativamente mais difíceis.

### Mitigação

- **Baby Steps — seguir estritamente a ordem de fases:**
  1. O código feio é isolado em funções menores, mas o comportamento permanece idêntico *(Fase 2)*
  2. Só depois que estiver legível em funções é que se pensa em objetos e polimorfismo *(Fase 3)*
  3. A segregação arquitetural vem por último, após a lógica estar estável *(Fase 4)*

  Avançar fases sem os critérios de validação anteriores satisfeitos é, em si, uma materialização deste risco.

---

## Matriz de Risco

```
Impacto
  ^
  │
Crítico  │              [R-03]
  │
Alto     │  [R-02]      [R-01]
  │
Médio    │              [R-04]
  │
Baixo    │
  └─────────────────────────────→ Probabilidade
           Baixa    Média    Alta
```

> A mitigação prioritária recai sobre **R-01** (alta probabilidade + alto impacto) via cobertura de testes, e sobre **R-03** (impacto crítico) via disciplina arquitetural desde a Fase 3.