# Requisitos do Sistema — Gilded Rose Refactoring Kata

---

## Requisitos Funcionais

### Itens Comuns e Regras Gerais

| ID | Nome | Descrição |
|----|------|-----------|
| RF-01 | Atualização de Prazo Geral | O sistema deve decrementar o valor de `SellIn` em 1 unidade para todos os itens a cada ciclo de atualização, exceto para itens lendários. |
| RF-02 | Degradação de Item Comum | O sistema deve decrementar a `Quality` de um item comum em 1 unidade por dia enquanto `SellIn >= 0`. |
| RF-03 | Degradação Pós-Vencimento | O sistema deve duplicar a velocidade de degradação da `Quality` de um item comum (−2/dia) assim que o prazo de venda expirar (`SellIn < 0`). |
| RF-04 | Piso de Qualidade | O sistema deve garantir que a `Quality` de nenhum item (exceto lendários) se torne menor que `0`. |
| RF-05 | Teto de Qualidade Geral | O sistema deve garantir que a `Quality` de nenhum item (exceto lendários) se torne maior que `50`. |

---

### Queijo Brie Envelhecido — `Aged Brie`

| ID | Nome | Descrição |
|----|------|-----------|
| RF-06 | Maturação do Aged Brie | O sistema deve incrementar a `Quality` do item "Aged Brie" em 1 unidade por dia enquanto `SellIn >= 0`. |
| RF-07 | Maturação Acelerada do Aged Brie | O sistema deve duplicar a velocidade de ganho de `Quality` do item "Aged Brie" (+2/dia) assim que o prazo de venda expirar (`SellIn < 0`). |

---

### Sulfuras, a Mão de Ragnaros — `Sulfuras, Hand of Ragnaros`

| ID | Nome | Descrição |
|----|------|-----------|
| RF-08 | Imutabilidade do Prazo Lendário | O sistema deve garantir que o `SellIn` do item "Sulfuras" permaneça estático a cada ciclo, não sofrendo o decremento geral diário. |
| RF-09 | Imutabilidade da Qualidade Lendária | O sistema deve garantir que a `Quality` do item "Sulfuras" permaneça estática a cada ciclo de atualização. |
| RF-10 | Exceção de Limite Lendário | O sistema deve permitir que a `Quality` do item "Sulfuras" seja fixada em `80`, como exceção direta ao teto geral de qualidade definido em RF-05. |

---

### Ingressos de Concerto — `Backstage passes to a TAFKAL80ETC concert`

| ID | Nome | Descrição |
|----|------|-----------|
| RF-11 | Valorização Padrão de Ingressos | O sistema deve incrementar a `Quality` de "Backstage passes" em 1 unidade por dia quando `SellIn > 10`. |
| RF-12 | Valorização Moderada de Ingressos | O sistema deve incrementar a `Quality` de "Backstage passes" em 2 unidades por dia quando `6 <= SellIn <= 10`. |
| RF-13 | Valorização Crítica de Ingressos | O sistema deve incrementar a `Quality` de "Backstage passes" em 3 unidades por dia quando `0 <= SellIn <= 5`. |
| RF-14 | Desvalorização Total Pós-Show | O sistema deve resetar a `Quality` de "Backstage passes" para `0` imediatamente após a data do concerto (`SellIn < 0`). |

---

### Itens Conjurados — `Conjured Items`

| ID | Nome | Descrição |
|----|------|-----------|
| RF-15 | Degradação Conjurada Padrão | O sistema deve decrementar a `Quality` de itens "Conjured" em 2 unidades por dia enquanto `SellIn >= 0`. |
| RF-16 | Degradação Conjurada Pós-Vencimento | O sistema deve decrementar a `Quality` de itens "Conjured" em 4 unidades por dia assim que o prazo de venda expirar (`SellIn < 0`). |

---

## Requisitos Não Funcionais

| ID | Nome | Descrição |
|----|------|-----------|
| RNF-01 | Restrição de Modificação de Terceiros *(Regra do Goblin)* | O sistema deve manter a classe `Item` original e a propriedade `Items` completamente intactas, sem alterações em suas assinaturas, atributos ou comportamento nativo. |
| RNF-02 | Legibilidade e Clean Code | O código refatorado deve seguir as diretrizes de estilo da linguagem Python (PEP 8) e eliminar os *Code Smells* mapeados durante a auditoria. |
| RNF-03 | Manutenibilidade / SOLID | A arquitetura final deve respeitar os princípios SOLID — especificamente o **Princípio do Aberto/Fechado (OCP)** —, permitindo a adição de novas categorias de itens sem modificar as classes existentes. |
| RNF-04 | Testabilidade | O sistema deve possuir uma arquitetura testável de forma isolada, permitindo a execução rápida de testes automatizados via linha de comando (`pytest`). |
| RNF-05 | Compatibilidade Tecnológica | A solução deve ser implementada utilizando Python 3.x estável e ferramentas de ecossistema padrão da linguagem para testes e relatórios de cobertura. |
| RNF-06 | Independência de Camadas *(Clean Architecture)* | O sistema deve segregar rigorosamente as regras de negócio puras (Domínio e Casos de Uso) das interfaces de entrada e saída (Adapters / Infrastructure), garantindo que a lógica de negócio não dependa de nenhuma estrutura de persistência ou interface externa. |

---

## Mapa de Cobertura RF × Estratégia

| Requisito | Estratégia Responsável |
|-----------|----------------------|
| RF-01, RF-02, RF-03, RF-04, RF-05 | `CommonItemStrategy` |
| RF-06, RF-07 | `AgedBrieStrategy` |
| RF-08, RF-09, RF-10 | `SulfurasStrategy` |
| RF-11, RF-12, RF-13, RF-14 | `BackstagePassStrategy` |
| RF-15, RF-16 | `ConjuredItemStrategy` |