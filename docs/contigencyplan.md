# Plano de Contingência — Gilded Rose Refactoring Kata

Este documento descreve o roteiro de execução da refatoração em cinco fases incrementais. Cada fase possui uma ação técnica delimitada, critérios de validação mensuráveis e uma branch Git dedicada — garantindo que nenhuma fase avance sem a rede de segurança da fase anterior estar intacta.

---

## Visão Geral das Fases

| Fase | Nome | Branch | Objetivo |
|------|------|--------|----------|
| 1 | A Rede de Segurança | `test/cobertura-inicial` | Mapear e proteger o comportamento atual com testes |
| 2 | O Desmembramento | `refactor/limpando-codigo` | Quebrar o Arrow Anti-Pattern via Extract Method |
| 3 | Implementação do Strategy | `refactor/polymorphism-strategy` | Substituir condicionais por polimorfismo |
| 4 | Arquitetura Limpa | `refactor/clean-architecture` | Segregar camadas seguindo Clean Architecture |
| 5 | Nova Funcionalidade | `feat/conjured-items` | Adicionar itens Conjured sem tocar no código existente |

---

## Fase 1 — A Rede de Segurança

> Antes de alterar um único caractere do código original, o comportamento atual deve estar totalmente mapeado e protegido por testes automatizados.

**Branch:** `test/cobertura-inicial` (a partir de `develop`)

### Ação Técnica

Escrever testes unitários com `pytest` (ou `unittest`) cobrindo todas as categorias de itens em situações normais e de fronteira — valores limítrofes de `Quality` e `SellIn`.

### Critérios de Validação

- [ ] **100% de Cobertura de Código**
  O relatório do `pytest-cov` deve indicar que todas as linhas e ramificações lógicas do método `update_quality` original foram executadas pelos testes.

- [ ] **Testes de Fronteira Incluídos**
  Existem testes validando o teto de qualidade (`50`), o piso (`0`) e o comportamento específico do Sulfuras (`80`).

- [ ] **Green State Consolidado**
  Todos os testes passam com sucesso sobre o código legado intacto.

---

## Fase 2 — O Desmembramento

> Quebrar o *Arrow Anti-Pattern* e reduzir o método longo, sem alterar o paradigma do código. Continuamos no procedimental — apenas organizando a casa.

**Branch:** `refactor/limpando-codigo`

### Ação Técnica

Aplicar a técnica de refatoração **Extract Method**: isolar a lógica de cada tipo de item em métodos privados dentro da própria classe `GildedRose`.

```python
# Exemplos de métodos extraídos
_update_aged_brie(item)
_update_backstage_passes(item)
_update_sulfuras(item)
_update_common_item(item)
```

O método `update_quality` principal passa a ser apenas um laço `for` limpo que direciona cada item ao seu método auxiliar correspondente.

### Critérios de Validação

- [ ] **Redução de Complexidade**
  O método `update_quality` central não deve ultrapassar poucas linhas altamente legíveis.

- [ ] **Zero Regressão**
  A suíte de testes da Fase 1 continua 100% verde sem que nenhuma linha de teste tenha sido alterada.

- [ ] **Histórico Granular**
  Cada método extraído possui seu próprio commit focado.
  ```
  refactor: extract aged brie update logic
  refactor: extract backstage passes update logic
  ```

---

## Fase 3 — Implementação do Strategy

> Com o código desmembrado e legível, atacamos os *code smells* de Switch Statements, Feature Envy e Primitive Obsession — transformando a lógica procedimental em uma arquitetura orientada a objetos.

**Branch:** `refactor/polymorphism-strategy`

### Ação Técnica

Como a classe `Item` não pode ser alterada (Regra do Goblin), criamos uma estrutura baseada no **Padrão Strategy**:

1. **Interface base abstrata** — define o contrato comum com o método `update(item)`.
2. **Subclasses especialistas** — cada tipo de item recebe sua própria classe:
   - `AgedBrieStrategy`
   - `BackstagePassStrategy`
   - `SulfurasStrategy`
   - `CommonItemStrategy`
3. **Simple Factory** — mapeia a string do nome do item à sua classe especialista correspondente.

### Critérios de Validação

- [ ] **Eliminação de Condicionais de Tipo**
  O método principal delega a execução e não contém mais checagens como `if item.name == "Aged Brie"`.

- [ ] **Encapsulamento Respeitado**
  A lógica de alteração dos dados pertence a cada classe especializada, eliminando a *Feature Envy*.

- [ ] **Classe `Item` Intacta**
  A classe `Item` original e sua propriedade `Items` não sofreram nenhuma modificação.

- [ ] **Rede de Segurança Intacta**
  Os testes originais da Fase 1 continuam passando sem alteração.

---

## Fase 4 — Arquitetura Limpa

> Com as regras de negócio isoladas por especialidade, realizamos a segregação arquitetural seguindo os princípios de Clean Architecture (Uncle Bob), garantindo independência de camadas e extensibilidade futura.

**Branch:** `refactor/clean-architecture`

### Ação Técnica

Reorganizar o projeto em três camadas explícitas:

| Camada | Diretório | Responsabilidade |
|--------|-----------|------------------|
| Domínio | `domain/strategies/` | Regras de negócio puras — as classes Strategy da Fase 3 |
| Casos de Uso | `use_cases/` | `UpdateInventoryUseCase` — orquestra a lista, aciona a Factory e dispara as atualizações |
| Infraestrutura | `infrastructure/` | `GildedRoseAdapter` — ponto de entrada legado; recebe a chamada externa, invoca o Caso de Uso e devolve o resultado mantendo o contrato original |

### Critérios de Validação

- [ ] **Independência de Domínio**
  A camada `domain/` não importa nada de arquivos externos ou de infraestrutura.

- [ ] **Segregação Rigorosa de Pastas**
  O projeto reflete visualmente as camadas da Arquitetura Limpa através de diretórios explícitos.

- [ ] **Zero Regressão Global**
  O teste de caracterização de 30 dias (Golden Master) continua passando sem alterar uma única linha do log original, provando que a reestruturação de pastas não quebrou o ecossistema.

---

## Fase 5 — Nova Funcionalidade

> Com o sistema perfeitamente refatorado, modular e extensível, adicionamos os **Conjured Items** — a prova de fogo do OCP.

**Branch:** `feat/conjured-items`

### Ação Técnica

Graças ao polimorfismo da Fase 3, a adição se resume a:

1. Criar a classe `ConjuredItemStrategy`, herdando da interface base e implementando a regra de degradação dupla.
2. Registrar a nova estratégia na Factory — sem tocar em nenhuma classe existente.

```python
# Regra de negócio do ConjuredItemStrategy
# SellIn >= 0  →  Quality -= 2
# SellIn <  0  →  Quality -= 4
```

### Critérios de Validação

- [ ] **Implementação sem Impacto**
  Nenhuma das classes especialistas das fases anteriores foi modificada para adicionar o item Conjured (OCP respeitado).

- [ ] **Novos Testes Unitários**
  Foram adicionados testes específicos cobrindo:
  - Degradação normal (`−2`)
  - Degradação pós-vencimento (`−4`)
  - Limites de qualidade (`0` e `50`)

- [ ] **Sucesso Global**
  100% dos testes — antigos e novos — estão passando em verde.

- [ ] **Merge para Main**
  O código está pronto para o Pull Request e pode ser integrado com segurança na branch `main`.

---

## Fluxo de Branches

```
main
 └── develop
      ├── test/cobertura-inicial       ← Fase 1
      ├── refactor/limpando-codigo     ← Fase 2
      ├── refactor/polymorphism-strategy  ← Fase 3
      ├── refactor/clean-architecture  ← Fase 4
      └── feat/conjured-items          ← Fase 5
```

> **Regra de ouro:** nenhuma fase avança enquanto houver testes vermelhos. A rede de segurança é o contrato entre as fases.