# Gilded Rose Refactoring Kata

> *Carlos Eduardo, Marcos Menezes, Rafael Guerra, Rian Dultra e Vínicius Fernandes*
> 

[https://github.com/dultradev/GildedRose](https://github.com/dultradev/GildedRose)

# Sobre a Gilded Rose

[https://github.com/emilybache/GildedRose-Refactoring-Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata)

A Gilded Rose é uma pequena pousada, localizada estrategicamente em uma prestigiosa cidade, onde quem atende é o amigável Alisson, que foi quem lhe contratou. O grande diferencial é que além de ser uma pousada, eles também compram e vendem mercadorias da mais alta qualidade. 

Atualmente já conta com um sistema que atualiza automaticamente os preços do estoque, criado pelo antigo funcionário Leeroy que não faz mais parte do negócio. Uma das classes centrais do sistema (a classe `Item`) pertence a um **goblin furioso** que fica no canto da taverna.

Esse druida não acredita em propriedade compartilhada de código e, se você alterar uma única linha da classe dele, ele vai se enfurecer e atacar o seu personagem. Por isso, a classe `Item` é considerada um "código intocável".

O negócio da estalagem está crescendo. Allison acabou de assinar um contrato com um fornecedor de **itens conjurados (magicamente criados)**. O sistema atual não sabe como lidar com esses novos itens de forma nativa.

Como o desenvolvedor original sumiu e o código virou um emaranhado incompreensível de condições (`if/else`), você foi chamado para arrumar a bagunça, garantir que o sistema atual não pare de funcionar e implementar essa nova categoria de produtos.

<aside>
<img src="https://app.notion.com/icons/description_gray.svg" alt="https://app.notion.com/icons/description_gray.svg" width="40px" />

### Resumo

- É uma pousada/loja que compra e comercializa mercadorias.
- Já tem um sistema de atualização de preços feito por um funcionário que não está mais na empresa.
- A classe `Item` não pode ser alterada.
- O Sistema precisa suportar uma nova categoria de itens.
</aside>

# Regras de Negócio

Todos os itens possuem uma propriedade `SellIn` que representa o prazo de validade em dias para a venda, e uma propriedade `Quality` que representa quão valioso o item é. 

À medida que o tempo passa, a qualidade dos itens se comporta de maneiras muito específicas.

Itens Comuns

### Itens Comuns (Items Padrão)

São os produtos genéricos da loja (ex: *"+5 Dexterity Vest"*, *"Elixir of the Mongoose"*). Eles seguem o fluxo natural de envelhecimento e depreciação.

- **Comportamento do `SellIn`:** Diminui em **1** unidade por dia.
- **Comportamento da `Quality`:**
    - Enquanto o `SellIn >= 0`: A qualidade diminui em **1** unidade por dia.
    - Assim que o prazo de venda expira (`SellIn < 0`): a qualidade passa a diminuir **duas vezes mais rápido** (ou seja, diminui em **2** unidades por dia).
- **Limites:** A qualidade nunca pode ser menor que **0** e não pode ser maior que 50.

Queijo Brie Envelhecido

### Queijo Brie Envelhecido (`*Aged Brie*`)

Um produto peculiar que contradiz a lógica natural: quanto mais velho fica, melhor é o seu estado.

- **Comportamento do `SellIn`:** Diminui em **1** unidade por dia.
- **Comportamento da `Quality`:**
    - A qualidade **aumenta** em **1** unidade a cada dia que passa.
    - *Nuance do código original:* Quando o `SellIn` expira (`SellIn < 0`), a velocidade com que ele ganha qualidade **dobra**, passando a aumentar em **2** unidades por dia.
- **Limites:** A qualidade máxima nunca pode ultrapassar **50**.

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

#### Nota sobre o código

Embora a especificação de requisitos escrita não explicite esse detalhe, a análise do código legado revela que o `Aged Brie` duplica sua velocidade de ganho de qualidade (passando para +2 por dia) após o vencimento (`SellIn < 0`). 
Para garantir a compatibilidade com o sistema atual e não quebrar funcionalidades existentes, essa regra foi mantida e protegida pelos testes de caracterização.

</aside>

Sulfuras

### Sulfuras, a Mão de Ragnaros (`*Sulfuras, Hand of Ragnaros*`)

Este é um item lendário. Por ser um artefato mágico e único, ele desafia as leis do tempo e do desgaste.

- **Comportamento do `SellIn`:**
    - Sendo lendário, ele não tem uma data de validade. O valor de `SellIn` **nunca muda** (permanece estático, independentemente de quantos dias passem).
- **Comportamento da `Quality`:**
    - A qualidade **nunca muda**. Ela é fixa e imutável.
- **Limites e Exceção:**
    - Sendo um item lendário, sua qualidade foge à regra geral do limite de 50: ela é fixada estritamente em **80**.

Ingressos de Concerto

### Ingressos de Concerto (`*Backstage passes to a TAFKAL80ETC concert*`)

Os ingressos para o festival são itens altamente sazonais. O comportamento do seu valor é determinado pela urgência e proximidade do evento.

- **Comportamento do `SellIn`:** Diminui em **1** unidade por dia.
- **Comportamento da `Quality`:**
    - Aumenta em **1** unidade por dia quando faltam **mais de 10 dias** para o show.
    - Aumenta em **2** unidades por dia quando faltam **10 dias ou menos** (`SellIn <= 10`).
    - Aumenta em **3** unidades por dia quando faltam **5 dias ou menos** (`SellIn <= 5`).
    - Cai abruptamente para **0** imediatamente após a data do concerto (`SellIn < 0`), pois o ingresso perde totalmente a utilidade.
- **Limites:**
    - Enquanto o show não passa, a qualidade respeita o teto máximo de **50**.

Conjurados

### Itens Conjurados (*Conjured Items*)

São itens criados por magia e, por isso, sua estrutura molecular se degrada de forma acelerada.

- **Comportamento do `SellIn`:** Diminui em **1** unidade por dia.
- **Comportamento da `Quality`:**
    - Eles degradam em qualidade **duas vezes mais rápido** que os itens comuns.
    - Enquanto o `SellIn` for maior ou igual a 0: a qualidade diminui em **2** unidades por dia.
    - Assim que o prazo de venda expira (`SellIn < 0`): a degradação também dobra em relação ao seu estado atual, diminuindo em **4** unidades por dia.
- **Limites:** A qualidade nunca pode ser menor que **0**.

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

**Nota sobre o código**

*Esta é a nova funcionalidade a ser implementada após a refatoração.*

</aside>
		

### Tabela de Resumo

| **Categoria do Item** | **Alteração Diária (Sell In >= 0)** | **Alteração Diária (Sell In < 0)** | **Limite de Qualidade** |
| --- | --- | --- | --- |
| **Comum** | $-1$ | $-2$ | Mínimo: $0$ / Máximo: $50$ |
| **Aged Brie** | $+1$ | $+2$ | Mínimo: $0$ / Máximo: $50$ |
| **Sulfuras** | $0$ (**Não muda**) | $0$ (**Não muda**) | **Fixo em** $80$ |
| **Backstage Passes** | $BP_{(d)} = \begin{cases} +1 & \text{se } d > 10 \text{ dias} \\ +2 & \text{se } d \le 10 \text{ dias} \\ +3 & \text{se } d \le 5 \text{ dias} \end{cases}$ | **Reseta para** $0$ | Mínimo: $0$ / Máximo: $50$ |
| **Conjured** *(Nova)* | $-2$ | $-4$ | Mínimo: $0$ / Máximo: $50$ |

## Documentação de Requisitos

Esta seção converte a narrativa de negócios da taverna em requisitos técnicos formais, servindo como base de aceitação para a suíte de testes automatizados e para a arquitetura de código.

No contexto de engenharia de software, os **Requisitos Funcionais** ditam *o que o sistema deve fazer* (as regras de atualização de cada item), enquanto os **Requisitos Não Funcionais** ditam *como o sistema deve operar ou quais restrições ele deve respeitar* (restrições de arquitetura, legibilidade e desempenho).

### Requisitos Funcionais (RF)

Itens Comuns

### Itens Comuns e Regras Gerais

- **RF-01 (Atualização de Prazo Geral):** O sistema deve decrementar o valor de `SellIn` em **1** unidade para todos os itens a cada ciclo de atualização, exceto para itens lendários.
- **RF-02 (Degradação de Item Comum):** O sistema deve decrementar a `Quality` de um item comum em **1** unidade por dia enquanto o `SellIn` for maior ou igual a 0.
- **RF-03 (Degradação Pós-Vencimento):** O sistema deve duplicar a velocidade de degradação da `Quality` de um item comum (decrementar em **2** unidades por dia) assim que o prazo de venda expirar (`SellIn < 0`).
- **RF-04 (Piso de Qualidade):** O sistema deve garantir que a `Quality` de nenhum item (exceto lendários) se torne **menor que 0**.
- **RF-05 (Teto de Qualidade Geral):** O sistema deve garantir que a `Quality` de nenhum item (exceto lendários) se torne **maior que 50**.

Queijo Brie Envelhecido

### Queijo Brie Envelhecido (`*Aged Brie*`)

- **RF-06 (Maturação do Aged Brie):** O sistema deve incrementar a `Quality` do item *"Aged Brie"* em **1** unidade por dia enquanto o `SellIn` for maior ou igual a 0.
- **RF-07 (Maturação Acelerada do Aged Brie):** O sistema deve duplicar a velocidade de ganho de `Quality` do item *"Aged Brie"* (incrementar em **2** unidades por dia) assim que o prazo de venda expirar (`SellIn < 0`).

Sulfuras

### Sulfuras, a Mão de Ragnaros (`*Sulfuras, Hand of Ragnaros*`)

- **RF-08 (Imutabilidade do Prazo Lendário):** O sistema deve garantir que o valor de `SellIn` do item *"Sulfuras, Hand of Ragnaros"* permaneça **inalterado** (estático) a cada ciclo de atualização, não sofrendo o decremento geral diário.
- **RF-09 (Imutabilidade da Qualidade Lendária):** O sistema deve garantir que a `Quality` do item *"Sulfuras, Hand of Ragnaros"* permaneça **inalterada** (estática) a cada ciclo de atualização.
- **RF-10 (Exceção de Limite Lendário):** O sistema deve permitir que a `Quality` do item *"Sulfuras, Hand of Ragnaros"* seja fixada estritamente em **80**, agindo como uma exceção direta ao teto geral de qualidade (RF-05).

Ingressos de Concerto

### Ingressos de Concerto (`*Backstage passes to a TAFKAL80ETC concert*`)

- **RF-11 (Valorização Padrão de Ingressos):** O sistema deve incrementar a `Quality` de *"Backstage passes"* em **1** unidade por dia quando o `SellIn` for maior que 10 dias.
- **RF-12 (Valorização Moderada de Ingressos):** O sistema deve incrementar a `Quality` de *"Backstage passes"* em **2** unidades por dia quando o `SellIn` estiver entre 10 e 6 dias ($6 \le SellIn \le 10$).
- **RF-13 (Valorização Crítica de Ingressos):** O sistema deve incrementar a `Quality` de *"Backstage passes"* em **3** unidades por dia quando o `SellIn` estiver entre 5 e 0 dias ($0 \le SellIn \le 5$).
- **RF-14 (Desvalorização Total Pós-Show):** O sistema deve resetar a `Quality` de *"Backstage passes"* para **0** imediatamente após a data do concerto (`SellIn < 0`).

Conjurados

### Itens Conjurados (*Conjured Items*)

- **RF-15 (Degradação Conjurada Padrão):** O sistema deve decrementar a `Quality` de itens *"Conjured"* em **2** unidades por dia enquanto o `SellIn` for maior ou igual a 0.
- **RF-16 (Degradação Conjurada Pós-Vencimento):** O sistema deve decrementar a `Quality` de itens *"Conjured"* em **4** unidades por dia assim que o prazo de venda expirar (`SellIn < 0`).
		

### Requisitos não Funcionais

Os Requisitos Não Funcionais definem as restrições de design, técnico-arquiteturais e de qualidade que o software precisa cumprir.

<aside>
<img src="https://app.notion.com/icons/clock_gray.svg" alt="https://app.notion.com/icons/clock_gray.svg" width="40px" />

#### RNF’S

- **RNF-01 (Restrição de Modificação de Terceiros - Regra do Goblin):**
    - O sistema deve manter a classe `Item` original e a propriedade `Items` completamente intactas, sem alterações em suas assinaturas, atributos ou comportamento nativo.
- **RNF-02 (Legibilidade e Clean Code):**
    - O código refatorado deve seguir as diretrizes de estilo da linguagem Python (**PEP 8**) e eliminar os *Code Smells* mapeados.
- **RNF-03 (Manutenibilidade / SOLID):**
    - A arquitetura final do sistema de atualização deve respeitar os princípios SOLID, especificamente o Princípio do Aberto/Fechado (OCP), permitindo a adição de futuras novas categorias de itens sem a necessidade de modificar as classes existentes.
- **RNF-04 (Testabilidade):**
    - O sistema deve possuir uma arquitetura testável de forma isolada, permitindo a execução rápida de testes automatizados via linha de comando (utilizando `pytest`).
- **RNF-05 (Compatibilidade Tecnológica):**
    - A solução deve ser implementada utilizando **Python 3.x** estável e ferramentas de ecossistema padrão da linguagem para testes e relatórios de cobertura.
- **RNF-06 (Independência de Camadas - Clean Architecture):**
    - O sistema deve segregar rigorosamente as regras de negócio puras (Regras de Domínio e Casos de Uso) das interfaces de entrada e saídas de dados (Adapters/Infrastructure), garantindo que a lógica de alteração dos itens não dependa de nenhuma estrutura de persistência ou interface externa.
</aside>

# Código (Antes da refatoração)

```python
# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
```

## Análise Estática de Código

Antes de qualquer modificação no código original, é fundamental identificar os principais pontos de melhoria que devem ser feitas no sistema para evitar uma falência técnica do projeto, e assim estabelecer uma estratégia para codificar com segurança, rapidez e qualidade. Para isso, foram mapeados os **Code Smells.**

<aside>
<img src="https://app.notion.com/icons/command-line_gray.svg" alt="https://app.notion.com/icons/command-line_gray.svg" width="40px" />

#### Code Smells

São **sintomas ou pistas no código-fonte que indicam a presença de problemas mais profundos de design ou arquitetura**.

Eles não são bugs, mas indicam que o código está se tornando difícil de entender, manter e testar. Eles evidenciam quais partes do código precisam ser limpas e reorganizadas antes de receberem novas funcionalidades.

</aside>

Como guia de identificação, utilizamos o site **Refactoring Guru**, um dos sites educacionais mais famosos e respeitados do mundo para desenvolvedores.

<aside>
<img src="https://app.notion.com/icons/gears_gray.svg" alt="https://app.notion.com/icons/gears_gray.svg" width="40px" />

#### Refactoring Guru

> https://refactoring.guru/
> 

Ele funciona como um **guia visual e prático focado em qualidade de código**, explicando de forma muito simples como transformar códigos confusos em sistemas limpos e fáceis de manter.

O autor do projeto utiliza **ilustrações lúdicas, metáforas visuais e histórias em quadrinhos** para explicar conceitos abstratos e complexos de engenharia de software. Isso torna o aprendizado muito menos maçante do que ler livros técnicos tradicionais. Além disso, boa parte do site possui uma excelente [**versão traduzida para o português**](https://refactoring.guru/pt-br).

</aside>

### Code Smells encontrados

Bloaters

### Bloaters (Inchados)

São códigos, métodos e classes que cresceram tanto que se tornaram impossíveis de gerenciar.

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

### Long Method

- **O que é:**
    - Ocorre quando um método centraliza tantas linhas de código e responsabilidades que se torna uma unidade monolítica.
    - Métodos longos são difíceis de ler, manter e testar. Em geral, se um método tem mais de dez linhas ou exige comentários internos para explicar "o que blocos específicos fazem", ele é um forte candidato a esse *smell*.
- **Onde está no Gilded Rose:**
    - Está localizado no método `update_quality` da classe `GildedRose`. Esse método gerencia o ciclo de atualização completo de todos os itens do inventário de uma só vez, resultando em um emaranhado visual de indentação profunda (gerando o efeito visual conhecido na comunidade como *Arrow Anti-Pattern* ou Seta da Perdição).
    
    <aside>
    <img src="https://app.notion.com/icons/arrows-swap-horizontally_red.svg" alt="https://app.notion.com/icons/arrows-swap-horizontally_red.svg" width="40px" />
    
    #### Arrow Anti-Pattern
    
    O código começa a se mover horizontalmente para a direita devido ao recuo excessivo provocado por múltiplos `if`s um dentro do outro, criando o formato de uma seta ou pirâmide (`if` dentro de `if` dentro de `if`), Destruindo a legibilidade visual do Python, que depende crucialmente da indentação.
    
    </aside>
    
- **Impacto:**
    - Destrói a legibilidade do código em Python. Como há múltiplos níveis de condicionais aninhadas para controlar os decrementos e incrementos de `quality` e `sell_in`, o esforço mental necessário para rastrear o fluxo de execução de um único item é exaustivo. Além disso, o risco de introduzir efeitos colaterais (bugs acidentais) ao alterar qualquer linha central é altíssimo.
</aside>

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

### Primitive Obssession

- **O que é:**
    - É o hábito de usar tipos de dados primitivos do próprio ecossistema da linguagem (como strings, inteiros, dicionários puros) para representar conceitos do domínio do negócio que possuem suas próprias regras e validações. Em vez de criar pequenos objetos dedicados, o desenvolvedor confia em dados brutos.
- **Onde está no Gilded Rose:**
    - O sistema utiliza strings puras (`str`) para identificar e diferenciar os tipos de itens mágicos através do campo `item.name` (ex: `item.name == "Aged Brie"`).
    - Além disso, os campos `quality` e `sell_in` são tratados como inteiros puros (`int`), deixando a responsabilidade de validar se a qualidade passou de 50 ou caiu para menos de 0 dispersa no meio de equações lógicas.
- **Impacto:**
    - Fragilidade extrema contra **erros de digitação** (*typos*) e falta de **segurança de tipo**. Se em algum lugar do banco de dados ou da entrada do sistema o nome for enviado como `"aged brie"` (com letras minúsculas) ou com um espaço extra, o sistema falhará silenciosamente em aplicar a regra correta, tratando-o como um item comum.
    - Além disso, as regras de limites (mínimo 0, máximo 50) precisam ser repetidas matematicamente em vários pontos do código em vez de serem validadas nativamente pelo próprio tipo do dado.
</aside>

OO Abusers

### Object-Orientation Abusers (Abusadores de Orientação a Objetos)

Ocorre quando as possibilidades da orientação a objetos são ignoradas ou usadas de forma errada (frequentemente substituídas por lógica procedimental).

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

### Switch Statements

- **O que é:**
    - Ocorre quando o código utiliza uma estrutura de escolha (como `switch/case` ou sequências longas de `if/elif/else`) para ramificar o comportamento do sistema com base no tipo ou propriedade de um objeto.
    - Em sistemas puramente orientados a objetos, esse tipo de ramificação deve ser substituído pelo uso de **Polimorfismo**.
- **Onde está no Gilded Rose:**
    - O método `update_quality` faz checagens explícitas e repetitivas de strings como `item.name != "Aged Brie"`, `item.name != "Backstage passes..."` e `item.name == "Sulfuras..."` espalhadas por toda a sua extensão para decidir quais regras aritméticas aplicar à qualidade do item.
- **Impacto:**
    - Violação direta do **Princípio do Aberto/Fechado (OCP)** do **SOLID**.
        - O código está "fechado" para expansão. Se o proprietário da taverna solicitar a adição de um novo tipo de item (como os itens *Conjured*), você será obrigado a caçar os pontos exatos da árvore de `if`s para injetar novas checagens de string, aumentando a fragilidade do sistema e quebrando o encapsulamento.
        
        <aside>
        <img src="https://app.notion.com/icons/immigration_gray.svg" alt="https://app.notion.com/icons/immigration_gray.svg" width="40px" />
        
        #### Open Closed Principle
        
        Define que as entidades de software (classes, módulos, funções) devem estar **abertas para extensão, mas fechadas para modificação**. 
        
        Para adicionar o novo item **"Conjured"**, você é obrigado a entrar no meio daquela bagunça e injetar mais `if`s. O código atual não permite extensão sem alteração cirúrgica no código antigo.
        
        </aside>
        

</aside>

Change Preventers

### Change Preventers (Impedidores de Mudança)

São problemas que fazem com que alterar o código em um lugar exija modificações em vários outros lugares, gerando medo de mexer no sistema.

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

### Divergent Change

- **O que é:**
    - Esse *smell* se manifesta quando você se vê obrigado a alterar uma mesma classe ou método por motivos completamente diferentes e independentes entre si sempre que o negócio evolui.
    - É um sintoma claro de que o código mistura conceitos que **deveriam estar separados**.
- **Onde está no Gilded Rose:**
    - Na classe `GildedRose` (e especificamente no método `update_quality`).
        - Se a regra de negócio do queijo `*Aged Brie*` mudar (ex: ele passar a ganhar +3 de qualidade), você alterará o método `update_quality`. Se a regra dos ingressos do concerto mudar, você alterará o **exato mesmo método** no mesmo arquivo.
- **Impacto:**
    - Violação gritante do **Princípio da Responsabilidade Única (SRP)** do **SOLID**.
        - O método falha em ter "apenas uma razão para mudar". Em equipes reais, a Modificação Divergente gera conflitos constantes de mesclagem de código (os temidos *merge conflicts* no Git) quando múltiplos desenvolvedores tentam implementar regras de itens diferentes ao mesmo tempo.
        
        <aside>
        <img src="https://app.notion.com/icons/badge_gray.svg" alt="https://app.notion.com/icons/badge_gray.svg" width="40px" />
        
        #### Single Responsability Principle
        
        Defende que uma classe, módulo ou função deve ter **apenas uma razão para mudar.**
        
        O método `update_quality` é responsável por:
        
        1. Descobrir o tipo do item.
        2. Atualizar a qualidade com base no tipo.
        3. Atualizar o tempo de venda (`sell_in`).
        4. Garantir que os limites (0 e 50) sejam respeitados.
        
        Se o dono da loja mudar a regra de como o `sell_in` do Brie funciona, você terá que mexer no mesmo método gigante onde altera a qualidade dos ingressos.
        
        </aside>
        
</aside>

Couplers

### Couplers (Acopladores)

Smells que causam acoplamento excessivo entre as classes, fazendo com que uma saiba detalhes íntimos demais da outra.

<aside>
<img src="https://app.notion.com/icons/code_red.svg" alt="https://app.notion.com/icons/code_red.svg" width="40px" />

### Feature Envy

- **O que é:**
    - Ocorre quando um método de uma classe passa mais tempo acessando, examinando e manipulando os dados de *outra* classe do que os seus próprios dados. É uma quebra do princípio clássico da Orientação a Objetos que dita: *"mantenha os dados e os comportamentos que usam esses dados no mesmo lugar"*.
- **Onde está no Gilded Rose:**
    - A classe `GildedRose` passa o tempo todo inspecionando, perguntando e alterando diretamente as propriedades internas da classe `Item` (`item.name`, `item.quality`, `item.sell_in`).
    - passa o tempo todo inspecionando, perguntando e alterando diretamente as propriedades internas da classe `Item` (`item.name`, `item.quality`, `item.sell_in`) e alterando os valores de `quality` e `sell_in` diretamente, enquanto a classe `Item` é apenas um contenedor de dados burro (uma *Data Class*).
- **Impacto:**
    - Violação do princípio do [**Encapsulamento e alto Acomplamento**](https://app.notion.com/p/POO-PHP-291486a71eae8053bb7de0c7923516a8?pvs=21).
        - A classe `GildedRose` sabe detalhes íntimos demais de como um `Item` funciona. Se a estrutura interna de `Item` precisar mudar no futuro, toda a lógica de negócio centralizada na outra classe será quebrada. O código perde a coesão.
</aside>
		

# Estratégia de Refatoração

Para garantir que o código seja limpo sem que a taverna sofra prejuízos com comportamentos inesperados, seguiremos uma estratégia estrita dividida em mitigação de riscos, ordem de execução e critérios de aceitação.

## Riscos e Cuidados no Código Legado

Refatorar o Gilded Rose não é apenas reorganizar linhas de código; é alterar a engenharia interna de um sistema sutilmente interconectado. Abaixo estão os riscos críticos identificados e os cuidados cirúrgicos que devemos tomar para mitigá-los.

<aside>
<img src="https://app.notion.com/icons/report_yellow.svg" alt="https://app.notion.com/icons/report_yellow.svg" width="40px" />

### Risk 1: Efeito Dominó por Acoplamento lógico

- **O que é o risco:**
    - Alterar a lógica de atualização de um item específico e, acidentalmente, quebrar o comportamento de outro item que não tinha nada a ver com a mudança.
- **Por que acontece no Gilded Rose:**
    - Por causa do *Code Smell* **Long Method** e da árvore de condicionais aninhadas.
        - Como as checagens usam lógica negativa (ex: `if item.name != "Aged Brie" and item.name != "Backstage passes":`), o fluxo de execução de um item depende diretamente de ele *não ser* outro item. Se alterarmos a ordem ou o escopo de um desses `if`s, podemos fechar a porta de entrada para uma categoria de item sem perceber.
- **Cuidados de Mitigação:**
    - **Rigor na Execução de Testes:**
        - Rodar a suíte de testes automatizados a *cada* alteração unitária (por menor que seja, como renomear uma variável ou inverter um `if`).
    - **Isolamento de Alterações:**
        - Mudar apenas uma ramificação lógica por vez. Se começarmos a mexer no fluxo do *Aged Brie*, não devemos tocar no fluxo dos *Backstage passes* no mesmo commit.
</aside>

<aside>
<img src="https://app.notion.com/icons/report_yellow.svg" alt="https://app.notion.com/icons/report_yellow.svg" width="40px" />

### **Risk 2: Quebra das Regras de Negócio Implícitas**

- **O que é o risco:**
    - Corrigir o código achando que ele está errado por não bater com a documentação em texto, quando na verdade o código original *é* a regra de negócio que está rodando em produção.
- **Por que acontece no Gilded Rose:**
    - Como analisamos antes, o ganho duplo ($+2$) de qualidade do *Aged Brie* após o vencimento não está nos requisitos textuais, mas está na lógica de produção.
    - Outro exemplo sutil é o item lendário *Sulfuras*: ele não apenas mantém a qualidade em 80, como o código original sequer altera o seu `SellIn`. Se tentarmos "limpar" o código diminuindo o `SellIn` de todos os itens de forma genérica no início do laço, quebraremos a regra do *Sulfuras*.
- **Cuidados de Mitigação:**
    - **Abordagem "Bug-for-Bug Compatibility":**
        - O comportamento do código legado é a nossa verdade absoluta. A documentação textual serve apenas como um guia inicial. Se o teste passar com o código antigo, o código refatorado *tem* que passar exatamente do mesmo jeito.
</aside>

<aside>
<img src="https://app.notion.com/icons/report_yellow.svg" alt="https://app.notion.com/icons/report_yellow.svg" width="40px" />

### Risk 3: Violação da Restrição do Goblin (Quebra de Escopo da Arquitetura)

- **O que é o risco:**
    - Desenhar uma solução linda arquitetonicamente, mas que viola os limites do que nos é permitido alterar, tornando o projeto inválido perante o "cliente" (o Goblin furioso).
- **Por que acontece no Gilded Rose:**
    - A tentação do desenvolvedor Python ao ver a classe `Item` é adicionar propriedades nela, criar métodos como `item.update()` ou herdar dela para criar `BrieItem(Item)`. No entanto, a regra proíbe alterar a classe `Item`.
- **Cuidados de Mitigação:**
    - **Uso de Design Patterns de Envelopamento:** Devemos usar padrões como o **Wrapper / Adapter** ou no nosso caso, o **Strategy Pattern**.
        - Em vez de alterar o `Item`, criaremos classes utilitárias ou que "envelopam" o item original (ex: uma classe `AgedBriePropagator` que recebe o `Item` bruto no construtor e manipula seus atributos permitidos), respeitando estritamente o código intocado.
</aside>

<aside>
<img src="https://app.notion.com/icons/report_yellow.svg" alt="https://app.notion.com/icons/report_yellow.svg" width="40px" />

### Risk 4: Modificação Prematura (Parálise por Análise ou Overengineering)

- **O que é o risco:**
    - Tentar aplicar padrões de projeto ultra complexos logo no primeiro dia, antes de organizar a casa, gerando um código novo que é tão confuso quanto o antigo.
- **Por que acontece no Gilded Rose:**
    - É muito comum o desenvolvedor querer criar imediatamente fábricas (*Factories*), meta-classes ou estruturas complexas de polimorfismo antes mesmo de extrair os métodos legados.
- **Cuidados de Mitigação:**
    - **Passos de Bebê (*Baby Steps*):**
        - Seguir estritamente a ordem de mudança que planejamos. Primeiro o código feio fica idêntico, mas isolado em funções menores. Só depois que ele estiver legível em funções é que pensaremos na estrutura de objetos e polimorfismo.
</aside>

## Fases e Critérios

Para mitigar os riscos de regressão e garantir um fluxo de trabalho profissional, o projeto será executado em passos incrementais. Cada fase possui um escopo fechado, uma estratégia de Git própria e critérios rígidos para ser considerada concluída.

Fase 1

## **Fase 1: A Rede de Segurança**

Antes de alterar um único caractere do código original, precisamos garantir que o comportamento atual esteja totalmente mapeado e protegido por testes automatizados.

- :github: **Git:**
    - Criar a branch `test/cobertura-inicial` a partir da `develop`.
- **Ação Técnica:**
    - Escrever testes unitários utilizando o framework `pytest` (ou `unittest`). Focaremos em cobrir todas as categorias de itens em situações normais e de fronteira (valores limítrofes de `Quality` e `SellIn`).
- **Critérios de Validação**
    - [ ]  **100% de Cobertura de Código:**
    - O relatório de cobertura (ex: `pytest-cov`) deve indicar que todas as linhas e ramificações lógicas do método `update_quality` original foram executadas pelos testes.
    - [ ]  **Testes de Fronteira Incluídos:**
    - Existem testes validando o teto de qualidade ($50$), o piso ($0$) e o comportamento específico do *Sulfuras* ($80$).
    - [ ]  **Green State Consolidado:**
    - Todos os testes passam com sucesso sobre o código legado intacto.

Fase 2

## Fase 2: O Desmembramento

Nesta fase, o objetivo é quebrar a "Seta da Perdição" (*Arrow Anti-Pattern*) e reduzir drasticamente o tamanho do método longo, mas **sem alterar o paradigma do código**. Continuaremos usando lógica procedimental estruturada, apenas organizando a casa.

- :github: **Git:**
    - Branch `refactor/limpando-codigo`.
- **Ação Técnica:**
    - Aplicar a técnica de refatoração **Extract Method** (Extrair Método). Isolaremos a lógica complexa de cada tipo de item em métodos privados dentro da própria classe `GildedRose`.
        - *Exemplo:* Criar `_update_aged_brie(item)`, `_update_backstage_passes(item)`, etc.
        - O método `update_quality` principal passará a ser apenas um laço `for` limpo que direciona cada item para sua respectiva função auxiliar.
- **Critérios de Validação (Definition of Done da Fase 2)**
    - [ ]  **Redução de Complexidade:**
    - O método `update_quality` central não deve passar de poucas linhas altamente legíveis.
    - [ ]  **Zero Regressão:**
    - A suíte de testes criada na Fase 1 continua 100% verde sem que nenhuma linha de teste tenha sido alterada.
    - [ ]  **Histórico Granular:**
    - Cada método extraído deve possuir seu próprio commit focado (ex: `refactor: extract aged brie update logic`).

Fase 3

## Fase 3: Implementação do Strategy

Com o código desmembrado e legível, atacaremos os *smells* de **Switch Statements**, **Feature Envy** e **Primitive Obsession**. Vamos transformar a lógica procedimental em uma arquitetura orientada a objetos elegante.

- :github: **Git:**
    - Branch `refactor/polymorphism-strategy`.
- **Ação Técnica:**
    - Como não podemos alterar a classe `Item` (regra do Goblin), criaremos uma estrutura baseada no padrão **Strategy**.
        - Criaremos uma classe abstrata/interface base que define um contrato comum (ex: método `update_quality()`).
        - Criaremos subclasses para cada tipo de item: `AgedBrieItem`, `BackstagePassItem`, `SulfurasItem`, `StandardItem`. Essas classes receberão o `Item` original no construtor e encapsularão a lógica de atualização interna.
        - Implementar uma `Simple Factory` para mapear a string do nome do item para a sua respectiva classe especialista.
- **Critérios de Validação**
    - [ ]  **Eliminação de Condicionais de Tipo:**
    - O método principal delegará a execução e não possuirá mais nenhuma checagem de string como `if item.name == "Aged Brie"`.
    - [ ]  **Encapsulamento Respeitado:**
    - A lógica de alteração dos dados pertence agora a cada classe especializada, eliminando a "Inveja de Funcionalidade".
    - [ ]  **Classe Item Intacta:**
        - A classe `Item` original e sua propriedade `Items` não sofreram nenhuma modificação de código.
    - [ ]  **Rede de Segurança Intacta:**
    - Os testes originais continuam passando perfeitamente.

Fase 4

## Fase 4:  Arquitetura Limpa

Com as regras de negócio totalmente orientadas a objetos e isoladas por especialidade, realizaremos a segregação arquitetural do projeto seguindo os conceitos de **Clean Architecture** (*Uncle Bob*), garantindo a independência de camadas e preparando o sistema para extensões futuras.

- :github: **GitHub:**
    - Branch: `refactor/clean-architecture`
- **Ação Técnica:**
    - **Camada de Domínio (`domain/entities/`):**
        - Mover as subclasses criadas no Strategy (Brie, Passes, etc.) para cá. Elas representam as regras de negócio cruciais e puras do sistema.
    - **Camada de Casos de Uso (`domain/use_cases/`):**
        - Criar o `UpdateInventoryUseCase`. Sua única função será orquestrar a lista de itens, passá-los pela Factory e disparar a atualização.
    - **Camada de Infraestrutura/Adapters (`infrastructure/`):**
        - A classe `GildedRose` original passará a residir aqui, funcionando apenas como um ponto de entrada (um "Controller"). Ela receberá a chamada do sistema legado, invocará o Caso de Uso do domínio e devolverá o resultado, mantendo o contrato original intacto.
- **Critérios de Validação:**
    - [ ]  **Independência de Domínio:**
    - A camada `domain` não importa nada de arquivos externos ou de infraestrutura.
    - [ ]  **Segregação Rigorosa de Pastas:**
    - O projeto reflete visualmente as camadas da Arquitetura Limpa através de diretórios explícitos.
    - [ ]  **Zero Regressão Global:**
    - O teste de caracterização de 30 dias (*Golden Master*) continua passando sem mudar uma única linha de texto do log original, provando que a reestruturação de pastas não quebrou o ecossistema.

Fase 5

## Fase 5:  Nova Funcionalidade

Com o sistema perfeitamente refatorado, modular e extensível, chegou o momento de adicionar a funcionalidade dos itens **Conjurados (*Conjured Items*)**.

- :github: **Git:**
    - Branch `feat/conjured-items`.
- **Ação Técnica:**
    - Se o polimorfismo da Fase 3 foi bem feito, adicionar o novo comportamento será incrivelmente simples.
        - Bastará criar uma nova classe `ConjuredItem` que herda da nossa estrutura e implementa a regra de degradar duas vezes mais rápido. Depois, basta registrar essa nova classe na nossa fábrica (*Factory*).
- **Critérios de Validação**
    - [ ]  **Implementação sem Impacto:**
    - Nenhuma das classes especialistas criadas na Fase 3 para os outros itens foi modificada para adicionar o item *Conjured* (respeitando o OCP).
    - [ ]  **Novos Testes Unitários:**
    - Foram adicionados testes específicos para cobrir o comportamento dos itens *Conjured*
        - Degradação normal $-2$
        - Degradação pós-vencimento $-4$
        - Limites de qualidade.
    - [ ]  **Sucesso Global:**
    - 100% dos testes (antigos + novos) estão passando em verde.
    - [ ]  **Merge para a Main:**
    - O código está pronto para sofrer o *Pull Request* e ser integrado com segurança na branch principal (`main`).
		

[Versionamento](Versionamento%20374486a71eae800c963ec23aa1b67f6b.csv)

# Fase 1 - Testes

O Primeiro passo no terminal foi criar a branch dedicada para essa cobertura de testes:

`git checkout -b test/cobertura-inicial`

Como o código original usa a classe `GildedRose` que recebe uma lista de objetos `Item`, vamos escrever nossos testes usando o framework `pytest`. Ele é mais moderno, limpo e pythônico do que o `unittest` nativo.

<aside>
<img src="https://app.notion.com/icons/code_gray.svg" alt="https://app.notion.com/icons/code_gray.svg" width="40px" />

### Testes unitários

`*test_gilded_rose.py`* 

```python
# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("fixme", items[0].name)

        
if __name__ == '__main__':
    unittest.main()
```

#### Test_foo

Esse teste padrão que vem no repositório (o `test_foo`) serve apenas como um **esqueleto de exemplo**. Ele foi deixado ali pelo criador do Kata por dois motivos:

- **Garantir que o ambiente funciona:**
    - Ele serve para você rodar logo após clonar o repositório e checar se o Python consegue encontrar a classe `GildedRose` e o `Item` sem dar erro de importação.
- **Ele quebra de propósito:**
    - Repare na linha `self.assertEqual("fixme", items[0].name)`. O teste cria um item com o nome `"foo"`, roda a atualização e depois tenta checar se o nome virou `"fixme"`. Como o nome continua sendo `"foo"`, o teste falha. Isso é uma brincadeira do autor (o famoso *"fixme"* ou *"corrija-me"*), te desafiando a começar a escrever testes de verdade ali.

Além disso, ele está usando a estrutura do `unittest` (com `class` e `self.assertEqual`), que é o framework nativo e mais antigo do Python. Como nossa meta é construir um portfólio de alto nível (padrão cimatec) no GitHub e usar o **Pytest** (que é o padrão moderno de mercado para Python), nós vamos **substituir completamente** esse esqueleto.

O `pytest` é uma escolha mais acertada porque ele consegue ler e rodar arquivos que usam `unittest`, mas ele nos permite escrever funções de teste muito mais simples e limpas, usando apenas o comando `assert` puro do Python, sem precisar criar classes ou usar `self.assertEqual`.

#### Novos Testes

Visando testar cada requisito funcional (RF) que estabelecemos, com exceção dos relacionados aos itens conjurados que ainda serão implementados; estabelecemos o seguinte script para realização dos testes unitários:

```python
# test_gilded_rose.py
from gilded_rose import Item, GildedRose

# ==========================================
# 📦 1. ITENS COMUNS (RF-01 ao RF-05)
# ==========================================

def test_item_comum_degrada_qualidade_e_sell_in_corretamente():
    """RF-01 & RF-02: Item comum perde 1 de SellIn e 1 de Quality antes do vencimento"""
    items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == 9
    assert items[0].quality == 19

def test_item_comum_degrada_em_dobro_apos_vencimento():
    """RF-03: Quando vencido (SellIn < 0), a qualidade cai de 2 em 2"""
    items = [Item(name="+5 Dexterity Vest", sell_in=0, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 18

def test_qualidade_de_um_item_nunca_e_negativa():
    """RF-04: Qualidade do item comum não pode cair abaixo de 0"""
    items = [Item(name="Elixir of the Mongoose", sell_in=5, quality=0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 0

# ==========================================
# 🧀 2. AGED BRIE (RF-05 ao RF-07)
# ==========================================

def test_aged_brie_limite_maximo_de_qualidade():
    """RF-05: Qualidade do Brie nunca pode passar de 50"""
    items = [Item(name="Aged Brie", sell_in=5, quality=50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 50

def test_aged_brie_aumenta_qualidade_conforme_envelhece():
    """RF-06: Aged Brie ganha +1 de qualidade antes do vencimento"""
    items = [Item(name="Aged Brie", sell_in=5, quality=10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 11

def test_aged_brie_ganha_qualidade_em_dobro_apos_vencimento():
    """RF-07: A pegadinha do código legado! Vencido, o Brie ganha +2 de qualidade"""
    items = [Item(name="Aged Brie", sell_in=0, quality=10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 12

# ==========================================
# 🌋 3. SULFURAS (RF-11.1 ao RF-11.3)
# ==========================================

def test_sulfuras_permanece_imutavel():
    """RF-08 & RF-10: Item lendário não altera SellIn e nem Quality"""
    items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == 10
    assert items[0].quality == 80

# ==========================================
# 🎟️ 4. BACKSTAGE PASSES (RF-08 ao RF-11)
# ==========================================

def test_backstage_passes_com_mais_de_10_dias():
    """RF-11: Aumenta em 1 quando faltam mais de 10 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 21

def test_backstage_passes_com_10_dias_ou_menos():
    """RF-12: Aumenta em 2 quando faltam entre 6 e 10 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 22

def test_backstage_passes_com_5_dias_ou_menos():
    """RF-13: Aumenta em 3 quando faltam entre 0 e 5 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 23

def test_backstage_passes_apos_o_show():
    """RF-14: Qualidade cai para 0 imediatamente após o show (SellIn < 0)"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 0
```

</aside>

<aside>
<img src="https://app.notion.com/icons/code_gray.svg" alt="https://app.notion.com/icons/code_gray.svg" width="40px" />

### Approval Tests

`*texttest_fixture.py*`

```python
# -*- coding: utf-8 -*-
from __future__ import print_function

from gilded_rose import *

def main():
    print("OMGHAI!")
    items = [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
    ]
    days = 2
    import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1
    for day in range(days):
        print("-------- day %s --------" % day)
        print("name, sellIn, quality")
        for item in items:
            print(item)
        print("")
        GildedRose(items).update_quality()

if __name__ == "__main__":
    main()

```

`*test_gilded_rose_approvals.py*`

```python
import io
import sys

from approvaltests import verify
from texttest_fixture import main

def test_gilded_rose_approvals():
    orig_sysout = sys.stdout
    try:
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        sys.argv = ["texttest_fixture.py", 30]
        main()
        answer = fake_stdout.getvalue()
    finally:
        sys.stdout = orig_sysout

    verify(answer)

if __name__ == "__main__":
    test_gilded_rose_approvals()
```

`*approvaltests_config.json*`

```json
{
  "subdirectory": "approved_files"
}
```

Esse arquivo usa uma biblioteca chamada `approvaltests`. Essa técnica (também chamada de ***Golden Master***) faz o seguinte:

1. Ela roda o script `texttest_fixture.py` simulando o comportamento da loja por **30 dias**.
2. Ela captura tudo o que o sistema imprime no terminal (`sys.stdout`) ao longo desses 30 dias (nomes dos itens, qualidade e sell_in mudando dia após dia).
3. Na primeira vez que roda, ela gera um arquivo de texto com essa saída e "aprova" esse arquivo como a **foto oficial do sistema**.
4. Sempre que você alterar o código no futuro, o teste roda tudo de novo por 30 dias e compara a nova saída de texto com o arquivo aprovado. Se mudar um único caractere, o teste falha.
    1. Sempre que for feito uma alteração ao código enquanto estiver refatorando, pode rodar o script novamente para um arquivo temporário e comparar através do comando `diff`. Se o `diff` não apontar nada, o comportamento do sistema não foi alterado.
    
    ```
    python texttest_fixture.py > current_output.txt
    diff golden_master.txt current_output.txt
    ```
    

> *Se o Approval Test já cobre tudo, porque preciso dos testes unitários?*
> 

Pense no **Approval Test** como um alarme de segurança geral da sua casa: se um ladrão entrar por qualquer janela, o alarme toca. Mas ele não te diz *qual* janela foi aberta, apenas que a casa foi invadida.

No código, se você errar uma linha de matemática na **Fase 3 (Polimorfismo)**, o Approval Test vai falhar e te mostrar uma tela cheia de textos vermelhos dizendo: *"A string gerada no dia 18 não bate com a original"*. Descobrir onde está o erro olhando para um relatório de 30 dias de logs é muito difícil e cansativo.

É aqui que entram os **Testes Unitários**. Eles funcionam como sensores específicos em cada janela:

- Eles testam uma única regra (um Requisito Funcional - RF) de forma isolada.
    - Exemplo: Se você quebrar a regra do *Aged Brie*, o teste `test_aged_brie_ganha_qualidade` vai falhar imediatamente, apontando o dedo para o erro: *"Esperava qualidade 22, mas veio 21"*.

<aside>
<img src="https://app.notion.com/icons/code_gray.svg" alt="https://app.notion.com/icons/code_gray.svg" width="40px" />

#### **Resumo**

O Approval Test garante que você não mude o comportamento macro do sistema. O Teste Unitário te dá a certeza de qual regra específica você está mexendo e facilita muito o seu trabalho na hora de debugar (encontrar erros).

</aside>

#### Resultados

Esse foi o resultado do script de teste gerado pelo Approval Test para simulação de 30 dias de funcionamento da loja, que servirá como arquivo de texto soberano, garantindo 100% de cobertura contra regressões globais.

`*test_gilded_rose_approvals.test_gilded_rose_approvals.approved.txt*`

```
OMGHAI!
-------- day 0 --------
name, sellIn, quality
+5 Dexterity Vest, 10, 20
Aged Brie, 2, 0
Elixir of the Mongoose, 5, 7
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 15, 20
Backstage passes to a TAFKAL80ETC concert, 10, 49
Backstage passes to a TAFKAL80ETC concert, 5, 49
Conjured Mana Cake, 3, 6

-------- day 1 --------
name, sellIn, quality
+5 Dexterity Vest, 9, 19
Aged Brie, 1, 1
Elixir of the Mongoose, 4, 6
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 14, 21
Backstage passes to a TAFKAL80ETC concert, 9, 50
Backstage passes to a TAFKAL80ETC concert, 4, 50
Conjured Mana Cake, 2, 5

-------- day 2 --------
name, sellIn, quality
+5 Dexterity Vest, 8, 18
Aged Brie, 0, 2
Elixir of the Mongoose, 3, 5
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 13, 22
Backstage passes to a TAFKAL80ETC concert, 8, 50
Backstage passes to a TAFKAL80ETC concert, 3, 50
Conjured Mana Cake, 1, 4

-------- day 3 --------
name, sellIn, quality
+5 Dexterity Vest, 7, 17
Aged Brie, -1, 4
Elixir of the Mongoose, 2, 4
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 12, 23
Backstage passes to a TAFKAL80ETC concert, 7, 50
Backstage passes to a TAFKAL80ETC concert, 2, 50
Conjured Mana Cake, 0, 3

-------- day 4 --------
name, sellIn, quality
+5 Dexterity Vest, 6, 16
Aged Brie, -2, 6
Elixir of the Mongoose, 1, 3
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 11, 24
Backstage passes to a TAFKAL80ETC concert, 6, 50
Backstage passes to a TAFKAL80ETC concert, 1, 50
Conjured Mana Cake, -1, 1

-------- day 5 --------
name, sellIn, quality
+5 Dexterity Vest, 5, 15
Aged Brie, -3, 8
Elixir of the Mongoose, 0, 2
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 10, 25
Backstage passes to a TAFKAL80ETC concert, 5, 50
Backstage passes to a TAFKAL80ETC concert, 0, 50
Conjured Mana Cake, -2, 0

-------- day 6 --------
name, sellIn, quality
+5 Dexterity Vest, 4, 14
Aged Brie, -4, 10
Elixir of the Mongoose, -1, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 9, 27
Backstage passes to a TAFKAL80ETC concert, 4, 50
Backstage passes to a TAFKAL80ETC concert, -1, 0
Conjured Mana Cake, -3, 0

-------- day 7 --------
name, sellIn, quality
+5 Dexterity Vest, 3, 13
Aged Brie, -5, 12
Elixir of the Mongoose, -2, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 8, 29
Backstage passes to a TAFKAL80ETC concert, 3, 50
Backstage passes to a TAFKAL80ETC concert, -2, 0
Conjured Mana Cake, -4, 0

-------- day 8 --------
name, sellIn, quality
+5 Dexterity Vest, 2, 12
Aged Brie, -6, 14
Elixir of the Mongoose, -3, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 7, 31
Backstage passes to a TAFKAL80ETC concert, 2, 50
Backstage passes to a TAFKAL80ETC concert, -3, 0
Conjured Mana Cake, -5, 0

-------- day 9 --------
name, sellIn, quality
+5 Dexterity Vest, 1, 11
Aged Brie, -7, 16
Elixir of the Mongoose, -4, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 6, 33
Backstage passes to a TAFKAL80ETC concert, 1, 50
Backstage passes to a TAFKAL80ETC concert, -4, 0
Conjured Mana Cake, -6, 0

-------- day 10 --------
name, sellIn, quality
+5 Dexterity Vest, 0, 10
Aged Brie, -8, 18
Elixir of the Mongoose, -5, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 5, 35
Backstage passes to a TAFKAL80ETC concert, 0, 50
Backstage passes to a TAFKAL80ETC concert, -5, 0
Conjured Mana Cake, -7, 0

-------- day 11 --------
name, sellIn, quality
+5 Dexterity Vest, -1, 8
Aged Brie, -9, 20
Elixir of the Mongoose, -6, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 4, 38
Backstage passes to a TAFKAL80ETC concert, -1, 0
Backstage passes to a TAFKAL80ETC concert, -6, 0
Conjured Mana Cake, -8, 0

-------- day 12 --------
name, sellIn, quality
+5 Dexterity Vest, -2, 6
Aged Brie, -10, 22
Elixir of the Mongoose, -7, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 3, 41
Backstage passes to a TAFKAL80ETC concert, -2, 0
Backstage passes to a TAFKAL80ETC concert, -7, 0
Conjured Mana Cake, -9, 0

-------- day 13 --------
name, sellIn, quality
+5 Dexterity Vest, -3, 4
Aged Brie, -11, 24
Elixir of the Mongoose, -8, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 2, 44
Backstage passes to a TAFKAL80ETC concert, -3, 0
Backstage passes to a TAFKAL80ETC concert, -8, 0
Conjured Mana Cake, -10, 0

-------- day 14 --------
name, sellIn, quality
+5 Dexterity Vest, -4, 2
Aged Brie, -12, 26
Elixir of the Mongoose, -9, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 1, 47
Backstage passes to a TAFKAL80ETC concert, -4, 0
Backstage passes to a TAFKAL80ETC concert, -9, 0
Conjured Mana Cake, -11, 0

-------- day 15 --------
name, sellIn, quality
+5 Dexterity Vest, -5, 0
Aged Brie, -13, 28
Elixir of the Mongoose, -10, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 0, 50
Backstage passes to a TAFKAL80ETC concert, -5, 0
Backstage passes to a TAFKAL80ETC concert, -10, 0
Conjured Mana Cake, -12, 0

-------- day 16 --------
name, sellIn, quality
+5 Dexterity Vest, -6, 0
Aged Brie, -14, 30
Elixir of the Mongoose, -11, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -1, 0
Backstage passes to a TAFKAL80ETC concert, -6, 0
Backstage passes to a TAFKAL80ETC concert, -11, 0
Conjured Mana Cake, -13, 0

-------- day 17 --------
name, sellIn, quality
+5 Dexterity Vest, -7, 0
Aged Brie, -15, 32
Elixir of the Mongoose, -12, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -2, 0
Backstage passes to a TAFKAL80ETC concert, -7, 0
Backstage passes to a TAFKAL80ETC concert, -12, 0
Conjured Mana Cake, -14, 0

-------- day 18 --------
name, sellIn, quality
+5 Dexterity Vest, -8, 0
Aged Brie, -16, 34
Elixir of the Mongoose, -13, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -3, 0
Backstage passes to a TAFKAL80ETC concert, -8, 0
Backstage passes to a TAFKAL80ETC concert, -13, 0
Conjured Mana Cake, -15, 0

-------- day 19 --------
name, sellIn, quality
+5 Dexterity Vest, -9, 0
Aged Brie, -17, 36
Elixir of the Mongoose, -14, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -4, 0
Backstage passes to a TAFKAL80ETC concert, -9, 0
Backstage passes to a TAFKAL80ETC concert, -14, 0
Conjured Mana Cake, -16, 0

-------- day 20 --------
name, sellIn, quality
+5 Dexterity Vest, -10, 0
Aged Brie, -18, 38
Elixir of the Mongoose, -15, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -5, 0
Backstage passes to a TAFKAL80ETC concert, -10, 0
Backstage passes to a TAFKAL80ETC concert, -15, 0
Conjured Mana Cake, -17, 0

-------- day 21 --------
name, sellIn, quality
+5 Dexterity Vest, -11, 0
Aged Brie, -19, 40
Elixir of the Mongoose, -16, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -6, 0
Backstage passes to a TAFKAL80ETC concert, -11, 0
Backstage passes to a TAFKAL80ETC concert, -16, 0
Conjured Mana Cake, -18, 0

-------- day 22 --------
name, sellIn, quality
+5 Dexterity Vest, -12, 0
Aged Brie, -20, 42
Elixir of the Mongoose, -17, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -7, 0
Backstage passes to a TAFKAL80ETC concert, -12, 0
Backstage passes to a TAFKAL80ETC concert, -17, 0
Conjured Mana Cake, -19, 0

-------- day 23 --------
name, sellIn, quality
+5 Dexterity Vest, -13, 0
Aged Brie, -21, 44
Elixir of the Mongoose, -18, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -8, 0
Backstage passes to a TAFKAL80ETC concert, -13, 0
Backstage passes to a TAFKAL80ETC concert, -18, 0
Conjured Mana Cake, -20, 0

-------- day 24 --------
name, sellIn, quality
+5 Dexterity Vest, -14, 0
Aged Brie, -22, 46
Elixir of the Mongoose, -19, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -9, 0
Backstage passes to a TAFKAL80ETC concert, -14, 0
Backstage passes to a TAFKAL80ETC concert, -19, 0
Conjured Mana Cake, -21, 0

-------- day 25 --------
name, sellIn, quality
+5 Dexterity Vest, -15, 0
Aged Brie, -23, 48
Elixir of the Mongoose, -20, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -10, 0
Backstage passes to a TAFKAL80ETC concert, -15, 0
Backstage passes to a TAFKAL80ETC concert, -20, 0
Conjured Mana Cake, -22, 0

-------- day 26 --------
name, sellIn, quality
+5 Dexterity Vest, -16, 0
Aged Brie, -24, 50
Elixir of the Mongoose, -21, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -11, 0
Backstage passes to a TAFKAL80ETC concert, -16, 0
Backstage passes to a TAFKAL80ETC concert, -21, 0
Conjured Mana Cake, -23, 0

-------- day 27 --------
name, sellIn, quality
+5 Dexterity Vest, -17, 0
Aged Brie, -25, 50
Elixir of the Mongoose, -22, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -12, 0
Backstage passes to a TAFKAL80ETC concert, -17, 0
Backstage passes to a TAFKAL80ETC concert, -22, 0
Conjured Mana Cake, -24, 0

-------- day 28 --------
name, sellIn, quality
+5 Dexterity Vest, -18, 0
Aged Brie, -26, 50
Elixir of the Mongoose, -23, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -13, 0
Backstage passes to a TAFKAL80ETC concert, -18, 0
Backstage passes to a TAFKAL80ETC concert, -23, 0
Conjured Mana Cake, -25, 0

-------- day 29 --------
name, sellIn, quality
+5 Dexterity Vest, -19, 0
Aged Brie, -27, 50
Elixir of the Mongoose, -24, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -14, 0
Backstage passes to a TAFKAL80ETC concert, -19, 0
Backstage passes to a TAFKAL80ETC concert, -24, 0
Conjured Mana Cake, -26, 0

-------- day 30 --------
name, sellIn, quality
+5 Dexterity Vest, -20, 0
Aged Brie, -28, 50
Elixir of the Mongoose, -25, 0
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, -15, 0
Backstage passes to a TAFKAL80ETC concert, -20, 0
Backstage passes to a TAFKAL80ETC concert, -25, 0
Conjured Mana Cake, -27, 0
```

#### Itens Conjurados

> *Como o sistema testou um item que nós ainda não implementamos (Conjured Mana Cake)?*
> 

Se você abrir o arquivo `texttest_fixture.py` (o script que gera os 30 dias), você verá que o criador do exercício já deixou o item `"Conjured Mana Cake"` na lista de estoque inicial. No entanto, o **código original do Gilded Rose ainda não sabe o que é um item conjurado**.

- **O que aconteceu nos bastidores?**
    - Como o código legado (`gilded_rose.py`) não tem nenhuma condição `if item.name == "Conjured Mana Cake"`, ele tratou o bolo conjurado como um **Item Comum**.

Vamos olhar os dados do seu log para provar isso:

- No **Dia 2**, o item está com: `Conjured Mana Cake, 1, 4` (SellIn = 1, Quality = 4).

```
-------- day 2 --------
name, sellIn, quality
+5 Dexterity Vest, 8, 18
Aged Brie, 0, 2
Elixir of the Mongoose, 3, 5
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 13, 22
Backstage passes to a TAFKAL80ETC concert, 8, 50
Backstage passes to a TAFKAL80ETC concert, 3, 50
Conjured Mana Cake, 1, 4
```

- Pelas regras que documentamos, se ele fosse um item Conjurado *de verdade*, no dia seguinte (Dia 4) ele deveria perder **2** de qualidade por estar no prazo, ou **4** se já estivesse vencido.

```
-------- day 3 --------
name, sellIn, quality
+5 Dexterity Vest, 7, 17
Aged Brie, -1, 4
Elixir of the Mongoose, 2, 4
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 12, 23
Backstage passes to a TAFKAL80ETC concert, 7, 50
Backstage passes to a TAFKAL80ETC concert, 2, 50
Conjured Mana Cake, 0, 3
```

Se você olhar o seu arquivo completo `.approved`, vai notar que no **Dia 3** ele foi de `Quality = 4` para `3` (comportando-se exatamente como um item comum, perdendo apenas 1 ponto, e não o dobro).

O autor do Kata colocou o item lá de propósito para que, na **Fase 4**, quando você implementar a lógica correta dos Conjurados, **o Approval Test quebre.** Ele vai falhar porque a nova saída (com a degradação rápida real) não vai bater com a saída antiga, onde ele se comportava como item comum.

Isso é proposital para te mostrar o poder do teste de aprovação em detectar mudanças de comportamento. Na Fase 4, nós vamos atualizar esse arquivo aprovado.

</aside>

### Auditoria dos Critérios de Validação

*Check-off* de cada um dos três critérios que estabelecemos em [**Fase 1: A Rede de Segurança** ](https://app.notion.com/p/Fase-1-A-Rede-de-Seguran-a-374486a71eae80088ff8e965ed1149e7?pvs=21) para ter certeza absoluta de que a **Fase 1** foi cumprida.

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  ***Testes de Fronteira Incluídos***
- **Verificação:**
    - Olhando para o código do arquivo `test_gilded_rose.py` que estruturamos:
        - **Piso ($0$):** Validado na função [`test_qualidade_de_um_item_nunca_e_negativa`](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21).
        - **Teto ($50$):** Validado na função [`test_aged_brie_limite_maximo_de_qualidade`](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21).
        - **Sulfuras ($80$):** Validado na função [`test_sulfuras_permanece_imutavel`](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21) (que testa o valor estático de 80 e a imutabilidade do prazo).
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  ***Green State Consolidado***

![image.png](image.png)

- **Verificação:**
    - Você executou o comando `pytest` no terminal e obteve o retorno oficial de **`12 passed in 0.04s`**. Isso significa que nenhum teste falhou (fase vermelha) e o código legado intacto foi totalmente aprovado pela nova suíte de testes.

</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  100% de Cobertura de Código (Linhas e Ramificações)
    
    ![image.png](image%201.png)
    
- **Verificação:**
    - No arquivo  `gilded_rose.py`, foi alcançado **100% de cobertura de linhas (Stmts) e 100% de cobertura de ramificações (Branch)**, com **zero** partes perdidas (`BrPart = 0` e `Missing = vazio`).
        - Isso significa que a rede de segurança que estabelecemos para o código legado é **absoluta**. Cada decisão que o algoritmo original toma foi mapeada pelos testes.

*Arquivo gerado pelo `pytest --cov=gilded_rose --cov-branch --cov-report=term-missing`*

![image.png](image%202.png)

![image.png](image%203.png)

![image.png](image%204.png)

> *Por que o relatório em HTML deu 98%?*
> 

Essa pequena diferença de 2% no relatório geral em HTML acontece porque, quando foi rodado o comando `--cov` sem especificar o arquivo, o Pytest mede a cobertura de **todos** os arquivos da pasta, incluindo:

- O próprio arquivo de testes (`test_gilded_rose.py`).
- O arquivo de configurações do approval tests.
- O script `texttest_fixture.py` (que possui aquele bloco `if __name__ == "__main__":` que às vezes não é totalmente executado pelo framework de testes).

Como o arquivo alvo da nossa refatoração (`gilded_rose.py`) está cravado em 100%, o critério de validação foi **completamente atingido**.

</aside>

### :github: Github

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento

Foi criada uma branch exclusiva `test/cobertura-inicial` para realização dos testes a partir da branch `develop`.

 Os commits realizados foram:

[Sem título](Sem%20t%C3%ADtulo%2037a486a71eae80ff8d6beb4c2eb3e6e5.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/1](https://github.com/dultradev/GildedRose/pull/1)

**Objetivo do Pull Request**

Este PR estabelece a **Fase 1: Rede de Segurança** do projeto Gilded Rose. Antes de iniciar qualquer refatoração no código legado estruturado, foi implementada uma suíte robusta de testes para garantir a integridade das regras de negócio existentes e evitar regressões futuras.

---

**O que foi implementado?**

### 1. Testes de Caracterização (Golden Master / Approval Tests)

- Utilização da biblioteca `approvaltests` para capturar a saída do script `texttest_fixture.py`.
- Congelamento e aprovação do comportamento macro do inventário ao longo de **30 dias simulados** no arquivo `.approved`.
- **Garantia:** Qualquer alteração que modifique o comportamento original do sistema (incluindo o item *Conjured*, que atualmente se comporta como item comum) fará este teste falhar.

**2. Testes Unitários Comportamentais (Pytest)**

Substituição do esqueleto do `unittest` original por testes granulares utilizando o padrão pythônico do `pytest`, mapeando os seguintes Requisitos Funcionais (RF):

- **Itens Comuns (RF-01 a RF-05):** Validação de degradação diária, degradação em dobro pós-vencimento e limites de qualidade (piso 0).
- **Aged Brie (RF-05 a RF-07):** Validação do ganho de qualidade diária e ganho em dobro após o vencimento (teto 50).
- **Sulfuras (RF-11.1 a RF-11.3):** Validação da imutabilidade do `SellIn` e da `Quality` travada em 80.
- **Backstage Passes (RF-08 a RF-11):** Validação dos três estágios de ganho de qualidade baseados nos dias restantes e reset total para 0 após o concerto.

---

**Critérios de Aceitação Cumpridos**

- [x]  100% de cobertura de código no método `update_quality`.
- [x]  Execução bem-sucedida no terminal local dos testes de fronteira (`12 passed`).
- [x]  Green State Consolidado com todos os testes passando com sucesso sobre o código legado intacto.

---

*Este Pull Request encerra a etapa de blindagem teórica e prática, permitindo o avanço seguro para a **Fase 2**.*

</aside>

</aside>

# Fase 2 - Descentralização

Nesta fase, o objetivo central foi quebrar a complexidade do método `update_quality` original utilizando técnicas de refatoração clássicas na branch `refactor/limpando-codigo`. O foco foi aumentar a **cognição do código** (facilidade de leitura e entendimento) para preparar o terreno para a arquitetura limpa.

## Código Refatorado

Vendo o  `gilded_rose.py` original, verá um laço `for item in self.items:` que engole mais de 60 linhas de pura confusão.

Nós vamos reescrever esse laço para que ele se torne um **direcionador de fluxo claro**. O método principal `update_quality` deve ficar legível de forma clara, delegando a responsabilidade para métodos privados (prefixados com `_` por convenção em Python).

```python
# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # O laço principal agora apenas lê o nome e direciona para a função correta
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                self._update_sulfuras(item)
            elif item.name == "Aged Brie":
                self._update_aged_brie(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self._update_backstage_passes(item)
            else:
                self._update_common_item(item)

    def _update_aged_brie(self, item):
        # RF-01 & RF-06: Diminui o prazo de venda e aumenta a qualidade
        item.sell_in -= 1
        
        if item.quality < 50:
            item.quality += 1
            
            # RF-07: Se já passou do prazo, ganha qualidade em dobro
            if item.sell_in < 0 and item.quality < 50:
                item.quality += 1

    def _update_backstage_passes(self, item):
        # RF-01: Diminui o prazo de venda
        item.sell_in -= 1

        # RF-14: Se o show já passou, o ingresso perde todo o valor
        if item.sell_in < 0:
            item.quality = 0
            return

        # RF-11: Valorização padrão (+1)
        if item.quality < 50:
            item.quality += 1

            # RF-12: Janela crítica de 10 dias ou menos (ganha +1 adicional, totalizando +2)
            if item.sell_in < 10 and item.quality < 50:
                item.quality += 1

            # RF-13: Janela crítica de 5 dias ou menos (ganha +1 adicional, totalizando +3)
            if item.sell_in < 5 and item.quality < 50:
                item.quality += 1

    def _update_common_item(self, item):
        # RF-01: Diminui o prazo de venda
        item.sell_in -= 1

        # RF-02 & RF-04: Degradação padrão respeitando o piso de 0
        if item.quality > 0:
            item.quality -= 1
            
            # RF-03: Se já venceu, degrada em dobro (-2 no total)
            if item.sell_in < 0 and item.quality > 0:
                item.quality -= 1

    def _update_sulfuras(self, item):
        # RF-11.1, RF-11.2, RF-11.3: Itens lendários não mudam nada
        pass

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
```

## Técnicas de Refatoração Aplicadas

Para transformar o emaranhado original em um fluxo limpo, foram aplicadas duas técnicas catalogadas por Martin Fowler:

<aside>
<img src="https://app.notion.com/icons/priority-mid_gray.svg" alt="https://app.notion.com/icons/priority-mid_gray.svg" width="40px" />

### Decompose Conditional

É uma técnica de refatoração que simplifica instruções `if/else` e `switch` complexas. 

Ela divide o bloco de código em três métodos menores e auto-explicativos: o teste de **condição**, o bloco de **sucesso** (then) e o bloco de **falha** (else).

- **Por que usar?**
    - **Melhora a legibilidade:**
        - O código passa a ler quase como uma frase em linguagem natural.
    - **Isola a lógica de negócios:**
        - O desenvolvedor não precisa ler detalhes de cálculo na mesma tela em que avalia o cenário de validação.
- **Onde está?**
    - **O Problema Original:**
        - O código legado utilizava lógica negativa cruzada (ex: `if item.name != "Aged Brie" and item.name != "Backstage passes":`). Isso forçava o cérebro do desenvolvedor a fazer uma ginástica mental para entender quem *entrava* em qual bloco.
    - **A Solução:**
        - Invertemos a lógica para **condicionais afirmativas e explícitas**. Em vez de adivinhar quem sobrava, o laço principal agora pergunta diretamente pelo nome do item (`if item.name == "Aged Brie"`).
</aside>

<aside>
<img src="https://app.notion.com/icons/merge_gray.svg" alt="https://app.notion.com/icons/merge_gray.svg" width="40px" />

### Extract Method

É uma técnica popular de refatoração de código usada para **quebrar funções grandes e complexas em unidades menores e mais focadas**, pegando um bloco de código e movendo-o para um método novo e independentemente. **Melhora drasticamente a legibilidade e a reutilização de código.**

- **Por que usar?**
    - **Melhora da legibilidade:**
        - Grandes blocos de código são mais difíceis de entender. Ao extrair um bloco lógico específico, você dá um nome descritivo (por exemplo, `calculateTax()` ou `validateUser()`), fazendo o código ser lido como inglês simples.
    - **Duplicação reduzida:**
        - Se você precisar executar a mesma sequência de ações em vários lugares, extraí-lo em um método permite que você chame em qualquer lugar em vez de copiar e colar.
    - **Princípio de Responsabilidade Única:**
        - Ajuda a garantir que o metódo seja responsável por fazer uma única coisa.
- **Onde está?**
    - **O Problema Original:**
        - Um único método longo detinha o conhecimento de todas as regras do negócio da taverna. Se houvesse um bug no cálculo do ingresso, todo o sistema corria risco por falta de isolamento de escopo.
    - **A Solução:**
        - Cada ramificação afirmativa foi extraída para um método privado especializado (`_update_aged_brie`, `_update_sulfuras`, etc.). O método principal `update_quality` foi transformado em um **Roteador de Fluxo**, cuja única responsabilidade é ler o nome do item e despachá-lo para a função correta.

</aside>

## Decisões e Justificativas

Durante o desmembramento, tomamos decisões estratégicas baseadas em princípios de desenvolvimento limpo:

### Uso de Métodos Privados Procedimentais

- **Decisão:**
    - Mantivemos a lógica em formato procedural (funções dentro da mesma classe), em vez de criar novas classes ou arquivos imediatamente.
- **Justificativa:**
    - Apesar de ser tentador pular direto para a Orientação a Objetos, o código original era tão confuso que tentar criar classes logo de cara aumentaria o risco de erro de tradução das regras. Ao isolar em funções primeiro, conseguimos "enxergar" a assinatura exata e os comportamentos repetidos de cada item de forma pura.

### A Estratégia de "Early Return"

- **Decisão:**
    - No método `_update_backstage_passes`, assim que o `sell_in` fica menor que 0, definimos a qualidade como 0 e executamos um `return`.
- **Justificativa:**
    - Isso elimina a necessidade de colocar o restante do código dentro de um bloco `else`. O *Early Return* limpa o ruído visual e deixa explícito que, se o show passou, o processamento daquele item acabou.

### Preservação da Classe `Item`

- **Decisão:**
    - A classe `Item` permaneceu intocada, funcionando apenas como uma estrutura de dados (*Anemic Model*).
- **Justificativa:**
    - Respeito estrito à **Restrição do Goblin**. Toda e qualquer manipulação de atributos foi feita por fora da classe.

## Rastreabilidade de Requisitos (Mapeamento no Código)

Cada método foi blindado com base nos **Requisitos Funcionais (RF)**:

| **Método Extraído** | **Requisitos Atendidos** | **Comportamento Chave** |
| --- | --- | --- |
| `_update_sulfuras` | **RF-11.1, RF-11.2, RF-11.3** | O método usa a instrução `pass` (não faz nada). Isso garante visualmente que o prazo e a qualidade do item lendário são imutáveis e ignoram o decremento global. |
| `_update_aged_brie` | **RF-01, RF-06, RF-07, RF-05** | Decrementa o prazo. Incrementa a qualidade em $+1$. Se `sell_in < 0`, incrementa mais um  $+1$ (ganho em dobro), sempre travando o teto em $50$. |
| `_update_backstage_passes` | **RF-01, RF-08, RF-09, RF-10, RF-11** | Decrementa o prazo. Aplica a escada de valorização progressiva baseada nos limites de dias ($10$ e $5$), limpando o valor para $0$ se o prazo expirar. |
| `_update_common_item` | **RF-01, RF-02, RF-03, RF-04** | A lógica padrão para itens de mercado. Perde valor comercial diariamente, dobra o prejuízo pós-vencimento, e nunca cai abaixo de $0$. |

## Auditoria dos Critérios de Validação

Vamos analisar minuciosamente cada um dos três critérios estabelecidos para a **Fase 2**:

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Redução de Complexidade
- **Verificação:**
    - Se olharmos para o método `update_quality` central após a nossa mudança, ele se transformou em um laço simples de apenas **11 linhas**:
        
        ```python
        def update_quality(self):
            for item in self.items:
                if item.name == "Sulfuras, Hand of Ragnaros":
                    self._update_sulfuras(item)
                elif item.name == "Aged Brie":
                    self._update_aged_brie(item)
                elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                    self._update_backstage_passes(item)
                else:
                    self._update_common_item(item)
        ```
        
    - Ele passou de um bloco com alta complexidade ciclomática (condicionais aninhadas tridimensionais) para uma estrutura puramente linear e altamente legível.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Zero Regressão
- **Verificação:**
    - Foi executado o comando `pytest` logo após a alteração do código e a suíte retornou **12 passed**. Como não tocamos em nenhuma linha do arquivo de testes (`test_gilded_rose.py`) nem do arquivo de aprovação, provamos que o comportamento do sistema permanece idêntico.
        
        ![image.png](image%205.png)
        
    
    Como os testes de cobertura passaram com 100% de sucesso, provamos empiricamente que:
    
    - **A Complexidade Ciclomática caiu drasticamente:**
        - O método principal passou de um emaranhado impossível de testar mentalmente para uma estrutura linear simples.
    - **O código se tornou Autodocumentado:**
        - Um desenvolvedor júnior que entrar no projeto hoje consegue entender o que a taverna vende em menos de 1 minuto apenas lendo os nomes dos métodos.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Histórico Granular
- **Verificação:**
    - Este critério dita que *cada método extraído deve possuir seu próprio commit focado*. Verifique em [Github](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21).
</aside>

### :github: Github

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento

Foi criada uma branch exclusiva `refactor/limpando-codigo` para realização limpeza e clareza do código a partir da branch `develop`.

 Os commits realizados foram:

[Sem título](Sem%20t%C3%ADtulo%20380486a71eae80f9abd8c16640cd3986.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/2](https://github.com/dultradev/GildedRose/pull/2)

**Objetivo do Pull Request**

Este PR consolida a **Fase 2: O Desmembramento**. O foco central foi eliminar a altíssima complexidade ciclomática do método principal `update_quality` através da decomposição de condicionais e isolamento de escopo por tipo de produto, preparando a base de código para a transição arquitetural.

---

**O que foi implementado?**

**1. Decomposição de Condicionais (*Decompose Conditional*)**

- Inversão da lógica negativa cruzada legada por condicionais afirmativas diretas e explícitas (`if item.name == "..."`), reduzindo drasticamente a carga cognitiva necessária para ler o fluxo principal.

**2. Extração de Métodos (*Extract Method*)**

Isolamento das regras de negócio em métodos privados específicos dentro da classe `GildedRose`:

- `_update_sulfuras(item)`: Garante visualmente e de forma isolada a imutabilidade do item lendário.
- `_update_aged_brie(item)`: Centraliza a maturação padrão e acelerada pós-vencimento.
- `_update_backstage_passes(item)`: Implementa a escada de valorização e o gatilho de *Early Return* (retorno antecipado) para zerar o valor pós-show.
- `_update_common_item(item)`: Isola a depreciação padrão de mercado.

**Impacto na Complexidade Ciclomática**

- O método central `update_quality` foi transformado em um **Roteador de Fluxo** puramente linear de apenas 11 linhas, delegando responsabilidades e tornando o código autogerenciável e autodocumentado.

---

**Critérios de Aceitação Cumpridos (Auditoria Interna)**

- [x]  **Redução de Complexidade:** Método central altamente enxuto e legível.
- [x]  **Zero Regressão:** Suíte de testes automatizados e Golden Master de 30 dias mantidos em 100% verde (`12 passed`) sem nenhuma alteração nos arquivos de teste.
- [x]  **Histórico Granular:** Commits fatiados e organizados via `git add -p`, garantindo que cada método extraído possua seu próprio registro histórico e sem commits "monolíticos".
</aside>

</aside>

---

# Fase 3 - Strategy e Otimização

Nesta fase, o objetivo central foi erradicar os *code smells* de **Switch Statements** (estruturas condicionais repetitivas de controle de tipo), **Feature Envy** (Inveja de Funcionalidade) e **Primitive Obsession** (dependência de strings para guiar regras de negócio). O paradigma puramente procedural foi substituído por um design polimórfico elegante.

## Código Refatorado

O método `update_quality` central precisava conhecer as regras de evolução de cada tipo de item da loja. Qualquer alteração ou novo item exigiria modificar a mesma função longa, violando o princípio Open/Closed (OCP).

A solução foi implementar o padrão de projeto **Strategy** junto com o **Simple Factory**, criando uma classe abstrata `UpdateStrategy` (usando o módulo nativo `abc` do Python) que define a estratégia que as classes especialistas implementarão. Cada tipo de item ganhou sua própria classe especialista (`AgedBrieUpdateStrategy`, `BackstagePassesUpdateStrategy`, etc.).

Além disso, Em vez de injetar o `Item` no construtor da estratégia, passamos o objeto diretamente como argumento no método `update(item: Item)`. Isso tornou as estratégias **Stateless** (sem estado interno), permitindo que elas funcionem como comportamento puro.

## Código Refatorado

```python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Dict

# ==========================================
# --- CONSTANTES DE DOMÍNIO ---
# ==========================================
MIN_QUALITY = 0
MAX_QUALITY = 50

# ==========================================
# --- CLASSE ITEM (INTACTA) ---
# ==========================================
class Item:
    """Classe de domínio representando um item da loja.
    
    Nota:
        De acordo com as regras do Gilded Rose Kata, esta classe 
        não deve ser modificada.
    """
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

# ==========================================
# --- STRATEGY PATTERN (OTIMIZADO) ---
# ==========================================
class UpdateStrategy(ABC):
    """Interface base para as estratégias de atualização de itens."""

    @abstractmethod
    def update(self, item: Item) -> None:
        pass

class CommonUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para itens comuns."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        # Se sell_in < 0, degrada 2, senão 1
        degrade_amount = 2 if item.sell_in < 0 else 1
        # Garante matematicamente que não cai abaixo do piso (0)
        item.quality = max(MIN_QUALITY, item.quality - degrade_amount)

class AgedBrieUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item 'Aged Brie'."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        # Se sell_in < 0, melhora 2, senão 1
        increase_amount = 2 if item.sell_in < 0 else 1
        # Garante matematicamente que não ultrapassa o teto (50)
        item.quality = min(MAX_QUALITY, item.quality + increase_amount)

class BackstagePassesUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para 'Backstage passes'."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = MIN_QUALITY
            return

        # Calcula o bônus baseado nas janelas de dias de forma linear
        increase_amount = 1
        if item.sell_in < 10:
            increase_amount = 2
        if item.sell_in < 5:
            increase_amount = 3

        item.quality = min(MAX_QUALITY, item.quality + increase_amount)

class SulfurasUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item lendário 'Sulfuras'."""
    def update(self, item: Item) -> None:
        # Item lendário permanece intocável
        pass

# =============================
# --- SIMPLE FACTORY ---
# =============================
class ItemStrategyFactory:
    """Fábrica responsável por fornecer a estratégia correta baseada no item."""
    
    # Instanciamos as estratégias uma única vez no nível da classe 
    # (Flyweight) já que elas não mantêm estado interno.
    _strategies: Dict[str, UpdateStrategy] = {
        "Aged Brie": AgedBrieUpdateStrategy(),
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassesUpdateStrategy(),
        "Sulfuras, Hand of Ragnaros": SulfurasUpdateStrategy(),
    }
    
    _default_strategy: UpdateStrategy = CommonUpdateStrategy()

    @classmethod
    def get_strategy(cls, item_name: str) -> UpdateStrategy:
        """Obtém a estratégia de atualização apropriada para o nome do item.

        Args:
            item_name (str): O nome do item.

        Returns:
            UpdateStrategy: A instância da estratégia correspondente.
        """
        return cls._strategies.get(item_name, cls._default_strategy)

# =============================
# --- CONTEXTO PRINCIPAL ---
# =============================
class GildedRose:
    """Gerenciador principal do inventário da taverna Gilded Rose."""

    def __init__(self, items: List[Item]) -> None:
        """Inicializa o inventário.

        Args:
            items (List[Item]): Lista de itens disponíveis na taverna.
        """
        self.items = items

    def update_quality(self) -> None:
        """Itera sobre o inventário e aplica as atualizações de qualidade e validade."""
        for item in self.items:
            strategy = ItemStrategyFactory.get_strategy(item.name)
            strategy.update(item)
```

## Classe Abstrata

Nativamente o Python não tem uma palavra-chave para interface. Na realidade, ele se apoia no **Duck Typing** (*se anda como um pato, então é um pato*) ou em estruturas explicitas de **Typing Tools**.

Uma forma de implementar a interface é pelo padrão **Interface por Herança Clássica (ou Contrato de Tempo de Execução),** utilizando herança pura para ditar como as subclasses devem se comportar.

```python
# ======== INTERFACE DO STRATEGY============
class UpdateStrategy: 
	
	def __init__(self, item): 
		self.item = item 
		
		def update_quality(self): 
			"""Método abstrato/contrato que todas as subclasses devem implementar""" 
			raise NotImplementedError
```

Ao colocar `raise NotImplementedError`, você cria uma trava de segurança. Se alguém criar uma subclasse (como `AgedBrieUpdate`) e esquecer de programar o método `update_quality`, o Python vai permitir que o objeto seja criado, mas vai travar o sistema com um erro assim que o método for chamado.

```python
class AgedBrieUpdate(UpdateStrategy):
    pass  # Esqueceu de implementar o update_quality

estrategia = AgedBrieUpdate(item="Brie")
estrategia.update_quality()  # ❌ Erro! NotImplementedError
```

**Qual a diferença para o módulo `abc` (Abstract Base Classes)?**

Essa abordagem é perfeitamente válida e muito comum em códigos legados ou scripts simples, mas ela tem uma desvantagem em relação ao `abc.ABC`: **o momento da falha**.

| Característica | Sua Abordagem (`NotImplementedError`) | Abordagem com `abc.abstractmethod` |
| --- | --- | --- |
| **Momento do Erro** | Apenas quando o método é **chamado**. | Assim que você tenta **instanciar** o objeto (`obj = MinhaClasse()`). |
| **Instanciação Base** | Permite criar um objeto `UpdateStrategy` diretamente. | Proíbe criar um objeto `UpdateStrategy` diretamente. |

Então a decisão final foi implementar a Classe Abstrata, chegando a essa solução:

```python
from abc import ABC, abstractmethod

class UpdateStrategy(ABC):  # Herda de ABC
    def __init__(self, item):
        self.item = item

    @abstractmethod  # Transforma o método em uma obrigação estrita
    def update_quality(self):
        pass
```

## Padronização de Código (Google Python Style Guide)

Para garantir a máxima legibilidade, uniformidade e manutenibilidade entre diferentes desenvolvedores, todo o ecossistema refatorado do Gilded Rose foi escrito seguindo as diretrizes do **Google Python Style Guide**.

A adoção deste padrão eliminou a ambiguidade na escrita do código e garantiu documentações autoexplicativas integradas diretamente às IDEs.

### Estilo de Docstrings (Google Format)

Todas as funções, métodos e classes especialistas foram documentados utilizando o formato Google de Docstrings. Este padrão divide a documentação em blocos semânticos claros (`Args`, `Returns`, `Raises`), facilitando a geração automática de relatórios técnicos.

*Exemplo aplicado na nossa Fábrica:*

```python
class ItemStrategyFactory:
    """Fábrica polimórfica que gerencia e distribui as estratégias de atualização.

    Utiliza um dicionário interno para garantir o reuso de instâncias (Flyweight)
    e suporta a identificação de categorias por análise de substrings.
    """

    @classmethod
    def get_strategy(cls, item_name: str) -> UpdateStrategy:
        """Determina a estratégia ideal analisando o nome do item recebido.

        Analisa se o nome se enquadra em uma categoria por substring ou se
        corresponde estritamente a um item lendário imutável.

        Args:
            item_name: A string contendo o nome completo do item do inventário.

        Returns:
            Uma instância concreta derivada de UpdateStrategy correspondente à 
            regra de negócio daquele item.
        """
```

### Tipagem Estática Estrita (*Type Hints*)

Alinhado às diretrizes modernas do guia do Google, o código adota tipagem estática em 100% das assinaturas de métodos, parâmetros e retornos (utilizando o módulo `typing`).

- **Por que adotar:**
    - Evita erros em tempo de execução (*runtime*), melhora o autocompletar das IDEs e serve como uma camada de documentação viva do que o método espera receber e entregar.

### Convenção de Nomenclatura e Visibilidade

Seguindo o rigor do estilo Google para Python:

- **Classes:** `PascalCase` (ex: `AgedBrieUpdateStrategy`).
- **Métodos, Funções e Variáveis:** `snake_case` (ex: `get_strategy`, `item_name`).
- **Constantes Globais:** `UPPER_CASE` (ex: `MAX_QUALITY`, `MIN_QUALITY`).
- **Atributos Privados/Protegidos da Classe:** Prefixados com um *underscore* `_` (ex: `_flyweight_cache`) para explicitar que seu escopo é estritamente interno da classe, impedindo vazamento de escopo.

## Padrões de Projeto

**Padrões de projeto** (design patterns) são soluções típicas para problemas comuns em projeto de software. Cada padrão é como uma planta de construção que você pode customizar para resolver um problema de projeto particular em seu código.

Eles não são códigos prontos para se copiar e colar, São um conjunto de ferramentas para soluções de problemas comuns em design de software, criando sistemas mais flexíveis, legíveis e fáceis de manter. Eles definem uma linguagem comum que ajuda a equipe a se comunicar mais eficientemente.

Decidimos usar padrões de projeto para **separar as responsabilidades**, permitindo que o sistema cresça sem que o código antigo precise ser modificado.

### Padrões Utilizados

Para resolver os *code-smells* encontrados sem quebrar a restrição do Goblin (manter a classe `Item` intacta), guiamos nossa implementação pelo material do Refactoring Guru, do Arquiteto de Soluções e Produtor de conteúdo Renato Augusto e decidimos implementar dois padrões clássicos do livro do *GoF (Gang of Four)*:

<aside>
<img src="https://app.notion.com/icons/chess-rook_gray.svg" alt="https://app.notion.com/icons/chess-rook_gray.svg" width="40px" />

#### Strategy

O Strategy é um padrão de projeto **comportamental** que permite definir uma família de algoritmos, encapsular cada um em sua própria classe e **torná-los intercambiáveis**. Ele permite alterar o comportamento de um objeto em tempo de execução sem alterar sua estrutura principal.

- **No código**
    
    ```python
    #A classe abstrata determina a estratégia que as classes especialistas
    # devem implementar
    class UpdateStrategy(ABC):
        """Interface base para as estratégias de atualização de itens."""
    
        @abstractmethod
        def update(self, item: Item) -> None:
            pass
    # Exemplo de uma classe especialista com a estratégia
    class AgedBrieUpdateStrategy(UpdateStrategy):
        """Estratégia de atualização para o item 'Aged Brie'."""
        def update(self, item: Item) -> None:
            item.sell_in -= 1
            # Se sell_in < 0, melhora 2, senão 1
            increase_amount = 2 if item.sell_in < 0 else 1
            # Garante matematicamente que não ultrapassa o teto (50)
            item.quality = min(MAX_QUALITY, item.quality + increase_amount)
    ```
    
- **Por que ele?**
    - O coração do problema era que a regra de atualização de qualidade *variava* de acordo com o tipo de item. O **Strategy** serve justamente para isolar algoritmos intercambiáveis.
- **Na Prática:**
    - Em vez de a classe `GildedRose` decidir como cada item envelhece, nós criamos "estratégias" isoladas. A `GildedRose` agora apenas diz: *"Item, execute a sua estratégia de atualização"*. Se amanhã o comportamento do *Aged Brie* mudar, nós alteramos **apenas** a classe `AgedBrieUpdateStrategy`, sem risco de quebrar o comportamento dos ingressos ou dos itens comuns.

Mais detalhes sobre o **Strategy** aqui:

[Strategy](https://app.notion.com/p/Strategy-372486a71eae80068515ffdea2cc4fda?pvs=21) 

</aside>

<aside>
<img src="https://app.notion.com/icons/factory_gray.svg" alt="https://app.notion.com/icons/factory_gray.svg" width="40px" />

#### Simple Factory

O **Simple Factory** (Fábrica Simples) **é um padrão de criação que encapsula a lógica de instanciação de objetos**. Em vez de usar a palavra-chave `new` diretamente no código cliente, você delega a criação para uma classe dedicada que retorna a instância correta com base em um parâmetro.

- **No Código**
    
    ```python
    class ItemStrategyFactory:
        """Fábrica responsável por fornecer a estratégia correta baseada no item."""
        
        # Instanciamos as estratégias uma única vez no nível da classe 
        # (Flyweight) já que elas não mantêm estado interno.
        _strategies: Dict[str, UpdateStrategy] = {
            "Aged Brie": AgedBrieUpdateStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassesUpdateStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasUpdateStrategy(),
        }
        
        _default_strategy: UpdateStrategy = CommonUpdateStrategy()
    
        @classmethod
        def get_strategy(cls, item_name: str) -> UpdateStrategy:
            """Obtém a estratégia de atualização apropriada para o nome do item.
    
            Args:
                item_name (str): O nome do item.
    
            Returns:
                UpdateStrategy: A instância da estratégia correspondente.
            """
            return cls._strategies.get(item_name, cls._default_strategy)
    ```
    
- **Por que ele?**
    - Se as estratégias estão isoladas em classes diferentes, alguém precisa olhar para o nome do item e decidir *qual* estratégia instanciar. Se colocássemos essa decisão (os `if`s de nome) dentro da `GildedRose`, o acoplamento continuaria lá.
- **Na Prática:**
    - A **Factory** centraliza o mapeamento de criação. Ela encapsula a "sujeira" de ler a string do nome do item e nos devolve o objeto correto pronto para o uso. O contexto principal (`GildedRose`) fica completamente limpo e agnóstico a strings.
</aside>

## Otimizações Algorítmicas

Após estabilizar a Orientação a Objetos local, aplicamos duas refatorações táticas focando na clareza do código de cada estratégia:

<aside>
<img src="https://app.notion.com/icons/factory_gray.svg" alt="https://app.notion.com/icons/factory_gray.svg" width="40px" />

#### Magic Numbers

Números como `50` e `0` espalhados pelo código são "magic numbers". São a quantidade de dias que o sistema atualmente considera como valores mínimos e máximos de qualidade. Nomeá-los e centraliza-los s torna as regras de negócio legíveis e facilita possíveis ajustes.

```python
MAX_QUALITY = 50
MIN_QUALITY = 0
```

</aside>

<aside>
<img src="https://app.notion.com/icons/factory_gray.svg" alt="https://app.notion.com/icons/factory_gray.svg" width="40px" />

#### Substituição de Condicionais por Funções Matemáticas (`min` / `max`)

O código anteriormente utilizava `if item.quality < 50:` repetidamente para testar se podia incrementar o valor. Isso gerava condicionais aninhadas de até 3 níveis de profundidade (escadas de `if`).

```python
    def _update_backstage_passes(self, item):
        # RF-01: Diminui o prazo de venda
        item.sell_in -= 1

        # RF-14: Se o show já passou, o ingresso perde todo o valor
        if item.sell_in < 0:
            item.quality = 0
            return

        # RF-11: Valorização padrão (+1)
        if item.quality < 50:
            item.quality += 1

            # RF-12: Janela crítica de 10 dias ou menos (ganha +1 adicional, totalizando +2)
            if item.sell_in < 10 and item.quality < 50:
                item.quality += 1

            # RF-13: Janela crítica de 5 dias ou menos (ganha +1 adicional, totalizando +3)
            if item.sell_in < 5 and item.quality < 50:
                item.quality += 1

```

- **Depois:** Eliminamos os blocos de decisão aninhados e passamos a calcular apenas a taxa de variação (`degrade_amount` ou `increase_amount`). Ao final, usamos as funções nativas `min()` e `max()` do Python para travar os valores de forma matemática linear:

```python
class BackstagePassesUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para 'Backstage passes'."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = MIN_QUALITY
            return

        # Calcula o bônus baseado nas janelas de dias de forma linear
        increase_amount = 1
        if item.sell_in < 10:
            increase_amount = 2
        if item.sell_in < 5:
            increase_amount = 3

        item.quality = min(MAX_QUALITY, item.quality + increase_amount)

```

</aside>

## Rastreabilidade de Requisitos Pós-Otimização

A implementação dos padrões de projeto junto com a otimização algorítmica resultou em um código muito mais limpo e que atende ainda atende os requisitos previamente apontados.

| **Classe Estratégia** | **Complexidade Visual** | **Abordagem Matemática Aplicada** |
| --- | --- | --- |
| `CommonUpdateStrategy` | Linear (Sem aninhamento) | Usa operador ternário para taxa e `max()` para travar o piso em 0. |
| `AgedBrieUpdateStrategy` | Linear (Sem aninhamento) | Usa operador ternário para taxa e `min()` para travar o teto em 50. |
| `BackstagePassesUpdateStrategy` | Escopo achatado | Removeu 4 níveis de `if`s aninhados. Avalia a janela crítica de dias sequencialmente e aplica o incremento via `min()` em uma única linha. |
| `SulfurasUpdateStrategy` | Vazio (`pass`) | Mantém a regra estrita de imutabilidade total do item lendário. |

## Auditoria dos Critérios de Validação

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Eliminação de Condicionais de Tipo
- **Verificação:**
    - O método principal `update_quality` dentro da classe `GildedRose` foi reduzido a isto:
        
        ```python
        def update_quality(self) -> None:
            for item in self.items:
                strategy = ItemStrategyFactory.get_strategy(item.name)
                strategy.update(item)
        ```
        
    - Não existe nenhuma checagem de string (ex: `if item.name == "Aged Brie"`). Toda a seleção foi delegada para a Fábrica e a execução para o Polimorfismo. A complexidade ciclomática do método central é 1.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Encapsulamento Respeitado
- **Verificação:**
    - A lógica de alteração dos dados foi totalmente distribuída para cada classe especialista (`CommonUpdateStrategy`, `AgedBrieUpdateStrategy`, etc.).
        
        ```python
        class CommonUpdateStrategy(UpdateStrategy):
            """Estratégia de atualização para itens comuns."""
            def update(self, item: Item) -> None:
                item.sell_in -= 1
                # Se sell_in < 0, degrada 2, senão 1
                degrade_amount = 2 if item.sell_in < 0 else 1
                # Garante matematicamente que não cai abaixo do piso (0)
                item.quality = max(MIN_QUALITY, item.quality - degrade_amount)
        ```
        
    - Além disso, com a nossa última otimização, eliminamos a "Inveja de Funcionalidade" profunda limpando as estruturas de `if item.quality < 50` aninhadas, substituindo-as por atribuições matemáticas diretas com `min()` e `max()`.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Classe Item Intacta
- **Verificação:**
    - A classe `Item` original e sua estrutura de inicialização/propriedades não sofreram nenhuma alteração de código. O contrato do Goblin foi respeitado à risca.
        
        ```python
        # ==========================================
        # --- CLASSE ITEM (INTACTA) ---
        # ==========================================
        class Item:
            """Classe de domínio representando um item da loja.
            
            Nota:
                De acordo com as regras do Gilded Rose Kata, esta classe 
                não deve ser modificada.
            """
            def __init__(self, name, sell_in, quality):
                self.name = name
                self.sell_in = sell_in
                self.quality = quality
        
            def __repr__(self):
                return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
        ```
        
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Rede de Segurança Intacta (Zero Regressão)
- **Verificação:**
    - Executamos o `pytest` após a refatoração polimórfica e após a otimização matemática com `min/max`. O terminal retornou **`12 passed`**, provando que o comportamento macro e micro do sistema permaneceu idêntico ao código espaguete original de 30 dias atrás.
    
    ![image.png](image%206.png)
    
</aside>

## :github: GitHub

![image.png](image%207.png)

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento

Foi criada uma branch exclusiva **`Refactor/polymorphism-strategy`** para implementação do strategy e de otimizações algorítimicas a partir da branch `develop`.

 Os commits realizados foram:

[Sem título](Sem%20t%C3%ADtulo%20383486a71eae808ea371f932463d5a78.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/3](https://github.com/dultradev/GildedRose/pull/3)

**Objetivo do Pull Request**

Este PR consolida a **Fase 3: Polimorfismo, Padrão Strategy e Otimização Algorítmica**. O objetivo foi erradicar os *code smells* de *Switch Statements* (estruturas condicionais repetitivas), *Feature Envy* (Inveja de Funcionalidade) e *Primitive Obsession* (dependência de strings para guiar regras de negócio), migrando o sistema para um design orientado a objetos maduro, sustentável e de alta performance.

---

**Padrões de Projeto & Arquitetura Implementados**

**1. Padrão Strategy (Variabilidade de Comportamento)**

- Criação de uma hierarquia baseada na classe abstrata `UpdateStrategy` (utilizando o módulo nativo `abc` do Python).
- Isolamento das regras de negócio em classes especialistas totalmente independentes (`AgedBrieUpdateStrategy`, `BackstagePassesUpdateStrategy`, etc.).
- **Abordagem Stateless:** As estratégias não mantêm estado interno; o objeto `Item` é passado diretamente como argumento no método `update(item: Item)`, permitindo o reuso puro de comportamento.

**2. Simple Factory & Padrão Flyweight (Instanciação e Performance)**

- Implementação da classe `ItemStrategyFactory` para centralizar o mapeamento de strings para objetos polimórficos.
- As estratégias são instanciadas uma única vez no nível do dicionário estático da fábrica (**Flyweight**), garantindo que o sistema reutilize as mesmas instâncias em memória independentemente do tamanho do inventário, reduzindo drasticamente a pressão sobre o *Garbage Collector*.

**3. Otimização Algorítmica (Achatamento de Escopo)**

- **Remoção de Números Mágicos:** Centralização dos limites regulatórios da taverna em constantes globais expressivas: `MIN_QUALITY = 0` e `MAX_QUALITY = 50`.
- **Substituição de Condicionais por Funções Matemáticas (`min` / `max`):** Eliminação completa de escadas de `if`s aninhados (redução da complexidade ciclomática do método principal para $1$). O cálculo agora avalia a taxa de variação e aplica os limites de forma matemática linear.

---

**Critérios de Aceitação Cumpridos (Auditoria Interna)**

- [x]  **Eliminação de Ifs de Tipo:**
- O método principal da `GildedRose` tornou-se 100% polimórfico e agnóstico a strings.
- [x]  **Encapsulamento Respeitado:**
- A responsabilidade de alteração pertence estritamente a cada classe especialista.
- [x]  **Classe Item Intacta:**
- A restrição imposta pelo Goblin foi cumprida com rigor (nenhuma linha da classe `Item` foi alterada).
- [x]  **Rede de Segurança Intacta:**
- Suíte de testes automatizados e Golden Master de 30 dias cravando **`12 passed`** pós-otimização.
</aside>

</aside>

# Fase 4: Arquitetura Limpa

Nesta fase, o foco migrou do design de código orientado a objetos (tratado na Fase 3) para a **arquitetura estrutural do projeto**. O objetivo foi aplicar os conceitos de Arquitetura Limpa para separar as preocupações do sistema, isolar a lógica de negócio de detalhes de implementação e garantir a sustentabilidade do software a longo prazo.

<aside>
<img src="https://app.notion.com/icons/target_gray.svg" alt="https://app.notion.com/icons/target_gray.svg" width="40px" />

## Arquitetura Limpa

A **Arquitetura Limpa (Clean Architecture)**, popularizada por Robert C. Martin (Uncle Bob), é um padrão de design arquitetural baseado na **segregação de responsabilidades em camadas concêntricas**. 

![image.png](image%208.png)

A sua regra fundamental é a **Regra de Dependência**: o código das camadas internas nunca deve conhecer ou depender do código das camadas externas. As dependências de código devem apontar apenas para dentro, em direção às regras de negócio.

Embora o Gilded Rose seja um projeto de escopo contido, a escolha da Arquitetura Limpa se justifica por três fatores críticos de engenharia:

- **Isolamento do Legado (Proteção contra o Goblin):**
    - O sistema original nos impõe restrições severas (a classe `Item` e a interface da classe `GildedRose` não podem ser alteradas para não quebrar os sistemas que já a consomem). A Arquitetura Limpa nos permite encapsular esse legado na periferia do sistema, impedindo que os caprichos do código antigo poluam as novas regras que estamos criando.
- **Independência de Detalhes de Infraestrutura:**
    - Se amanhã a taverna decidir parar de receber os itens por uma lista em memória e passar a consumi-los de uma API HTTP, de um banco de dados SQL ou de um arquivo CSV, a lógica de evolução de qualidade dos itens permanecerá **100% intocada**. Mudaremos apenas a camada externa.
- **Facilidade de Evolução (Extensibilidade):**
    - Ao isolar o núcleo do negócio, a inserção de novos comportamentos (como os futuros itens *Conjurados*) torna-se um processo cirúrgico, sem risco de gerar efeitos colaterais em outras partes do software.

</aside>

## Árvore de Diretórios

Para este projeto em Python, vamos adotar uma estrutura de diretórios que deixa as intenções do sistema explícitas na raiz do projeto (o chamado ***Screaming Architecture***).

<aside>
<img src="https://app.notion.com/icons/alert_gray.svg" alt="https://app.notion.com/icons/alert_gray.svg" width="40px" />

#### Screaming Architecture

**Screaming Architecture** (ou Arquitetura Gritante) **é um conceito de arquitetura de software criado por Robert C. Martin (conhecido como *Uncle Bob*)**. 

A ideia central é que a estrutura de pastas e arquivos de um sistema deve imediatamente comunicar o seu propósito de negócio, em vez de revelar quais frameworks ou ferramentas técnicas utilizam.

</aside>

Para evitar a complexidade acidental (*overengineering*) e respeitar o princípio **YAGNI** (*You Aren't Gonna Need It*) e o **KISS (***Keep It Simple, Stupid)*, o sistema foi mapeado estritamente em **três camadas essenciais**, eliminando componentes redundantes como repositórios ou controladores complexos que não fariam sentido para um sistema operando inteiramente em memória.

<aside>
<img src="https://app.notion.com/icons/close_gray.svg" alt="https://app.notion.com/icons/close_gray.svg" width="40px" />

#### **O Princípio YAGNI**

O **YAGNI** (*You Aren't Gonna Need It* foca em não adivinhar o futuro do seu software.

- **O que significa:**
    - A sigla significa "Você Não Vai Precisar Disso". Orienta o desenvolvedor a **não** implementar funcionalidades, arquiteturas ou bibliotecas extras com base na suposição de que "isso vai ser útil um dia".
- **Na prática:**
    - Você só deve construir uma funcionalidade quando houver uma demanda real e imediata por ela. Adicionar coisas extras gera código desnecessário (conhecido como *bloatware*) que torna o sistema pesado e difícil de alterar posteriormente.
- **Benefícios:**
    - Maior foco no que realmente agrega valor de imediato, entregas mais rápidas e um sistema mais enxuto e livre de complexidades inúteis.

Nossa referência de implementação desse princípio

> https://www.youtube.com/watch?v=wjtfJ9c4KdM
> 
</aside>

<aside>
<img src="https://app.notion.com/icons/condense_gray.svg" alt="https://app.notion.com/icons/condense_gray.svg" width="40px" />

#### **O Princípio KISS**

**KISS (***Keep It Simple, Stupid)* defende que a simplicidade deve ser o principal objetivo no design de sistemas e no código.

- **O que significa:**
    - O termo se traduz como "Mantenha Isso Simples, Estúpido". A ideia é que soluções simples, sem abstrações ou firulas desnecessárias, têm menos chances de conter bugs e são muito mais fáceis de dar manutenção.
- **Na prática:**
    - Evitar criar funções gigantescas ou usar lógicas mirabolantes para resolver problemas triviais. Se um problema pode ser resolvido com 5 linhas simples, não tente usar um design pattern complexo de 50 linhas para "prevenir o futuro".
- **Benefícios:**
    - Menor custo de manutenção, código mais legível e facilidade para novos desenvolvedores entenderem o sistema.

Nossa referência de implementação desse princípio

> https://www.youtube.com/watch?v=wjtfJ9c4KdM
> 
</aside>

O **KISS** e **YAGNI** **são pilares da engenharia de software focados em evitar complexidade e desperdício**. Juntos, eles guiam o programador a escrever apenas o código necessário para resolver o problema atual, da maneira mais fácil possível de ler, manter e alterar.

```
python/
│
├── src/
│		├── __init__.py
│		│
│		├── domain/                         # Camada 1: Regras de Negócio Puras
│   ├── __init__.py
│   ├── item.py                     # A entidade pura (Goblin)
│   ├── constants.py                # Constantes (MIN_QUALITY, MAX_QUALITY)
│   │
│   └── strategies/                 # Estratégias pertencem ao Domínio!
│   │   ├── __init__.py
│   │   ├── base.py                 # UpdateStrategy (ABC)
│   │   ├── common.py
│   │   ├── aged_brie.py
│   │   ├── backstage_passes.py
│   │   └── sulfuras.py
│   │
│		├── use_cases/                      # Camada 2: Orquestração/Aplicação
│   ├── __init__.py
│   ├── factory.py                  # ItemStrategyFactory (Mapeamento)
│   └── update_inventory.py         # Caso de Uso Puro: UpdateInventoryUseCase
│   │
│		├──infrastructure/                 # Camada 3: Mecanismos e Detalhes
│	  ├── __init__.py
│	  └── gilded_rose_adapter.py      # Classe GildedRose original (Interface legada)
│
└── tests/                      
```

O maior erro ao estudar Arquitetura Limpa é acreditar que ela exige uma "receita de bolo" engessada com todas as pastas possíveis. O verdadeiro propósito do Uncle Bob ao propor a Arquitetura Limpa é a **Segregação de Responsabilidades baseada no nível de política do sistema**.

Essa estrutura de três camadas abaixo é a expressão mais pura e enxuta da Arquitetura Limpa para o contexto do Gilded Rose. Ela resolve o acoplamento sem inflar o projeto com dezenas de arquivos vazios.

## Camadas

domain/

#### Camada de Domínio (`domain/`)

O coração financeiro e comercial da taverna. É a camada mais interna, estável e pura do sistema. Ela não importa nada de nenhuma outra pasta e desconhece qualquer tecnologia externa.

**Componentes inclusos:**

- **`item.py`**
    - A entidade de dados pura herdada do sistema legado.
- **`constants.py`**
    - Regras numéricas universais do negócio (como os tetos e pisos de qualidade: `MIN_QUALITY = 0`, `MAX_STANDARD_QUALITY = 50`).
- **`strategies/`**
    - A árvore polimórfica de evolução dos itens criada na Fase 3. Como o cálculo de como um queijo estraga ou um ingresso valoriza é uma regra de negócio pura da taverna, essas classes pertencem legitimamente ao Domínio.

use_cases/

#### Camada de Casos de Uso (`use_cases/`)

Esta camada abriga as regras de negócio específicas da aplicação. Ela define as ações que o sistema pode executar, orquestrando o fluxo de dados de e para as entidades do domínio.

**Componentes inclusos:**

- **`update_inventory.py` (`UpdateInventoryUseCase`)**
    - É o maestro do sistema. Sua única responsabilidade é receber uma lista de entidades, coordenar a execução passando-as pela fábrica e disparar a atualização polimórfica.
- **`factory.py` (`ItemStrategyFactory`)**
    - A fábrica abstrata que resolve qual estratégia do domínio deve ser aplicada com base no nome do produto. Ela serve de suporte logístico para a execução do caso de uso.

infrastrcuture/

### Camada de Infraestrutura (`infrastructure/`)

A camada mais externa da arquitetura, onde residem os detalhes de implementação, frameworks, ferramentas e os pontos de contato com o ecossistema externo ou legado.

**Componentes inclusos:**

- **`gilded_rose_adapter.py` (`GildedRose`)**
    - Esta classe atua estritamente como um **Adaptador de Fronteira (Boundary Adapter)**.
        - Ela mantém a assinatura e os contratos originais exigidos pelo sistema antigo e pelos testes, agindo como um *pass-through* (controlador simplificado) que recebe a requisição, delega o trabalho para o Caso de Uso interno e atualiza os objetos em memória.
		

Uma decisão totalmente arbitrária da nossa refatoração foi separar cada estratégia em seu próprio arquivo (`aged_brie.py`, `sulfuras.py`). O **Python não é como o Java**. O Java nos força a criar um arquivo por classe; o Python nos dá o poder dos módulos. 

Criar um arquivo para cada estratégia (`aged_brie.py`, `sulfuras.py`, etc.), sendo que cada classe tem literalmente de 2 a 5 linhas de código útil, viola o princípio **KISS**. Uma solução guiada pelo **YAGNI** seria unificar todas as estratégias em um único arquivo `src/domain/strategies.py`.

Porém acreditamos que **`strategies/` com um arquivo por estratégia** é a decisão mais importante. No arquivo original, tudo num arquivo só tornava invisível que cada estratégia é uma unidade de mudança independente. Quando chegar o item `Conjured` (a extensão clássica do kata), você cria `conjured.py`, registra na factory, e **não toca em nenhum outro arquivo** — isso é o Open/Closed Principle funcionando na estrutura de diretórios, não só no código.

Colocamos esse diretório dentro de `domain/`, porque a lógica de evolução de qualidade do queijo ou do ingresso é uma regra de negócio pura da taverna, e não um detalhe de aplicação.

### `domain/strategies`

base

#### Classe abstrata/Interface

```python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.domain.item import Item

class UpdateStrategy(ABC):
    """Interface base para as estratégias de atualização de itens."""

    @abstractmethod
    def update(self, item: Item) -> None:
        pass
```

Define a estratégia que será utilizada pelas demais classes especialistas

common

#### Classe dos itens comuns

```python
# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.constants import MIN_QUALITY
from src.domain.strategies.base import UpdateStrategy

class CommonUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para itens comuns."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        # Se sell_in < 0, degrada 2, senão 1
        degrade_amount = 2 if item.sell_in < 0 else 1
        # Garante matematicamente que não cai abaixo do piso (0)
        item.quality = max(MIN_QUALITY, item.quality - degrade_amount)
```

aged_brie

#### Classe dos queijos envelhecidos

```python
# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.constants import MAX_QUALITY
from src.domain.strategies.base import UpdateStrategy

class AgedBrieUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item 'Aged Brie'."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        # Se sell_in < 0, melhora 2, senão 1
        increase_amount = 2 if item.sell_in < 0 else 1
        # Garante matematicamente que não ultrapassa o teto (50)
        item.quality = min(MAX_QUALITY, item.quality + increase_amount)
```

backstage_passes

#### Classe dos ingressos

```python
# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.constants import MIN_QUALITY, MAX_QUALITY
from src.domain.strategies.base import UpdateStrategy

class BackstagePassesUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para 'Backstage passes'."""
    def update(self, item: Item) -> None:
        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = MIN_QUALITY
            return

        # Calcula o bônus baseado nas janelas de dias de forma linear
        increase_amount = 1
        if item.sell_in < 10:
            increase_amount = 2
        if item.sell_in < 5:
            increase_amount = 3

        item.quality = min(MAX_QUALITY, item.quality + increase_amount)
```

sulfuras

#### Classe das Sulfuras

```python
# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.strategies.base import UpdateStrategy

class SulfurasUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item lendário 'Sulfuras'."""
    def update(self, item: Item) -> None:
        # Item lendário permanece intocável
        pass
```
		

### Preservação da Fronteira Comercial

Um dos maiores desafios ao migrar para a Arquitetura Limpa é o risco de quebrar os clientes que já consomem o sistema. No nosso caso, o ecossistema de testes (`test_gilded_rose.py`) e os scripts de simulação de 30 dias esperavam importar `Item` e `GildedRose` diretamente da raiz do arquivo original.

Para solucionar isso sem alterar uma única linha de código dos testes originais, aplicamos o padrão **Facade (Fachada)** no arquivo `gilded_rose.py` original localizado na raiz.

```python
# python/gilded_rose.py
# -*- coding: utf-8 -*-
"""Arquivo de fachada mantido para preservar a compatibilidade com o sistema legado."""

from src.domain.item import Item
from src.infrastructure.gilded_rose_adapter import GildedRose

__all__ = ["Item", "GildedRose"]
```

Os testes continuam fazendo `from gilded_rose import GildedRose, Item`. Eles acham que estão conversando com o código antigo, mas, por baixo dos panos, a Fachada redireciona as chamadas para a nossa estrutura desacoplada em camadas. Isso prova o poder da Arquitetura Limpa em **estabilizar sistemas legados**.

<aside>
<img src="https://app.notion.com/icons/video-game-joystick_gray.svg" alt="https://app.notion.com/icons/video-game-joystick_gray.svg" width="40px" />

#### Facade

O padrão Facade (Fachada) é um padrão de projeto estrutural (do famoso catálogo *Design Patterns / GoF*) que **fornece uma interface simplificada para um corpo de código complexo**, como uma biblioteca, um framework ou um conjunto de várias classes/subsistemas.

Em termos simples: ele cria uma "frente de loja" bonita, amigável e fácil de usar, escondendo toda a fiação elétrica, engrenagens e bagunça que acontecem nos bastidores.

</aside>

Os testes continuam fazendo `from gilded_rose import GildedRose, Item`. Eles acham que estão conversando com o código antigo, mas, por baixo dos panos, a Fachada redireciona as chamadas para a nossa estrutura desacoplada em camadas. Isso prova o poder da Arquitetura Limpa em **estabilizar sistemas legados**.

## Auditoria dos Critérios de Validação

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Independência de Domínio
- **Verificação:**
    - Se abrirmos qualquer arquivo dentro de `src/domain/` (seja o `item.py`, `constants.py` ou as estratégias), as importações são puramente locais ou do próprio Python (como `abc`).
    
    ```python
    # -*- coding: utf-8 -*-
    
    class Item:
        """Modelo de domínio representando um item do inventário da taverna.
    
        Note:
            De acordo com as regras do Gilded Rose Kata, esta classe
            não deve ser modificada.
        """
    
        def __init__(self, name: str, sell_in: int, quality: int) -> None:
            self.name = name
            self.sell_in = sell_in
            self.quality = quality
    
        def __repr__(self) -> str:
            return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
    ```
    
    - O Domínio não importa nada de `use_cases/` e muito menos de `infrastructure/`. A regra de dependência do Uncle Bob foi respeitada: o coração do sistema é agnóstico ao resto do mundo.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Segregação Rigorosa de Pastas (*Screaming Architecture*)
- **Verificação:**
    - O projeto não é mais um "arquivo único espaguete". Agora, ao olhar para a raiz do projeto, a estrutura de diretórios deixa claro o nível de maturidade do software.
    
    ![image.png](image%209.png)
    
    - O Domínio isola as regras, o Caso de Uso isola a orquestração (`UpdateInventoryUseCase`) e a Infraestrutura isola o adaptador legado (`GildedRose`).
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Preservação de Contrato (Zero Regressão Global)
- **Verificação:**
    - A suíte de testes original e o Golden Master de 30 dias continuam cravando **`12 passed`** sem que tivéssemos alterado uma única linha sequer dos arquivos de teste.
    
    ![image.png](image%2010.png)
    
    - O padrão *Facade* (Fachada) aplicado na raiz do projeto traduziu perfeitamente o ecossistema antigo para a nova arquitetura limpa em total segredo.
</aside>

## :github: GitHub

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento

Foi criada uma branch exclusiva `refactor/clean-architecture` para implementação da Arquitetura Limpa a partir da branch `develop`.

 Os commits realizados foram:

[Sem título](Sem%20t%C3%ADtulo%20383486a71eae80559a43cd049be19568.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/4](https://github.com/dultradev/GildedRose/pull/4)

**Objetivo do Pull Request**

Este PR consolida a **Fase 4: Desacoplamento Arquitetural (Clean Architecture)**. O objetivo foi reestruturar a organização do projeto, distribuindo as responsabilidades em camadas concêntricas de acordo com as diretrizes de Robert C. Martin (Uncle Bob), blindando o domínio de efeitos colaterais e do acoplamento com o código legado.

---

**Divisão de Camadas Implementada**

**1. Camada de Domínio (`src/domain/`)**

- **Pureza de Negócio:** Isola a entidade `Item`, as constantes regulatórias da taverna (`MIN_QUALITY`, `MAX_STANDARD_QUALITY`) e a árvore polimórfica de estratégias. Esta camada possui zero dependências externas.

**2. Camada de Casos de Uso (`src/use_cases/`)**

- **Orquestração:** Abriga o `UpdateInventoryUseCase`, responsável único por ditar o fluxo de execução (mapear itens via fábrica e disparar as atualizações). Contém também a `ItemStrategyFactory`.

**3. Camada de Infraestrutura (`src/infrastructure/`)**

- **Adaptação:** Onde reside a classe `GildedRose` legada, atuando estritamente como um **Boundary Adapter** (Interface de Fronteira). Ela recebe a lista em memória do sistema antigo e aciona o caso de uso puro da aplicação.

**Compatibilidade e Padrão Facade**

- O arquivo `gilded_rose.py` original na raiz foi convertido em uma **Fachada (Facade)** de exportação. Isso garantiu que todo o ecossistema legado e os testes automatizados continuassem funcionando via retrocompatibilidade, sem quebras.

---

**Critérios de Aceitação Cumpridos**

- [x]  **Independência de Domínio:** Camada interna totalmente livre de importações externas.
- [x]  **Segregação Rigorosa:** Arquivos distribuídos por nível de política de software.
- [x]  **Zero Regressão Global:** Suíte de testes mantida em 100% verde (`12 passed`) de forma transparente.
</aside>

</aside>

# Fase 5: O novo item

Nesta fase final, o ecossistema arquitetural construído nas fases anteriores foi colocado à prova. O objetivo foi introduzir a nova funcionalidade exigida pelo negócio: o suporte aos itens mágicos **"Conjurados" (*Conjured*)**, garantindo que o sistema fosse expandido sem a necessidade de modificar as regras de negócio dos itens antigos.

No sistema legado anterior, adicionar o item *Conjured* (Conjurado) exigiria abrir o arquivo principal, caçar os blocos de `if/else` corretos, torcer para não quebrar qualquer outro item e aumentar ainda mais a complexidade do código.

No nosso sistema limpo, adicionar essa funcionalidade exige apenas **criar um arquivo novo** e **adicionar uma linha na fábrica**.

## Requisitos

Os itens com o prefixo **"Conjured"** possuem propriedades mágicas que fazem com que sua qualidade se deteriore duas vezes mais rápido do que a de um item comum:

- **Antes do prazo de validade (`sell_in >= 0`):**
    - Reduz a qualidade em **2** unidades por dia.
- **Após o prazo de validade (`sell_in < 0`):**
    - Reduz a qualidade em **4** unidades por dia.
- **Restrição Regulatória:**
    - A qualidade nunca pode ser reduzida abaixo do piso global (`MIN_QUALITY = 0`).

> [**Requisitos itens conjurados**](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21)
> 

## Implementando o novo item

Nova Estratégia

Como a nossa arquitetura é modular, vamos criar um arquivo exclusivo para a regra do novo item dentro da pasta de estratégias do domínio.

Crie o arquivo `src/domain/strategies/conjured.py` com o seguinte código calistênico e otimizado com `max()`:

```python
# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.strategies.base import UpdateStrategy
from src.domain.constants import MIN_QUALITY

class ConjuredUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para itens magicamente Conjurados.
    
    Degradam a qualidade duas vezes mais rápido que os itens comuns.
    """
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        
        # Degrada 2 antes do prazo, e 4 após o vencimento
        degrade_amount = 4 if item.sell_in < 0 else 2
        
        item.quality = max(MIN_QUALITY, item.quality - degrade_amount)
```

Nova Factory

Agora, precisamos avisar a nossa fábrica que há um novo Item **Conjurado** no sistema. O **Approval Test** testa o `"Conjured Mana Cake"` , mas o nosso sistema precisa admitir e aplicar a regra de negócio para qualquer novo item conjurado.

Isso se aplica também aos **Ingressos para o Backstage**, onde o código antigo usava a string exata `"Backstage passes to a TAFKAL80ETC concert"` , Porque no paradigma procedural acoplado, o desenvolvedor original não tinha abstrações. Ele codificou o **único exemplo que existia no banco de dados naquele momento**

A intenção do negócio (a especificação) diz: *"Ingressos de Backstage aumentam o valor conforme o show se aproxima"*. O nome do show (`TAFKAL80ETC`) é apenas um **detalhe de dado**, não a regra em si. Mudar a checagem para `"Backstage passes"` preserva 100% da regra histórica do item antigo e estende o benefício para novos shows.

A regra vale para ***Aged Brie* (Queijo Brie Envelhecido)**. Ele não é um item único com número de série; ele é um **tipo/categoria de produto**. Se amanhã o dono da taverna decidir vender `"Aged Brie de Cabra"`, `"Aged Brie Trufado"` ou `"Aged Brie Premium"`, a regra física de maturação do queijo continua sendo exatamente a mesma: ele ganha qualidade à medida que envelhece.

Porém para as **Sulfuras**, de acordo com a lore do World of Warcraft (de onde o Kata foi inspirado), *Sulfuras, a Mão de Ragnaros* é uma **Arma Lendária Única**. Não existe "Sulfuras de Bronze" ou "Sulfuras do Chef". Ela é um artefato estrito.

Se o sistema aceitasse qualquer string que contivesse "Sulfuras" (ex: um item falso chamado `"Fake Sulfuras replica"`), o sistema aplicaria a regra de imutabilidade (qualidade fixa em 80 e nunca quebra) para um item que deveria ser comum, gerando uma brecha nas regras da taverna. Ou seja, para as *Sulfuras*, o match deve continuar sendo **estrito (`==`)**, porque o nome identifica um objeto específico e imutável, e não uma categoria de produtos.

Para tornar a fábrica ainda mais robusta, vamos fazer uma checagem dinâmica para capturar qualquer substring no nome, iremos atualizar nossa `factory.py`:]

```python
# -*- coding: utf-8 -*-
from typing import Dict
from src.domain.strategies.base import UpdateStrategy
from src.domain.strategies.common import CommonUpdateStrategy
from src.domain.strategies.aged_brie import AgedBrieUpdateStrategy
from src.domain.strategies.backstage_passes import BackstagePassesUpdateStrategy
from src.domain.strategies.sulfuras import SulfurasUpdateStrategy
from src.domain.strategies.conjured import ConjuredUpdateStrategy

class ItemStrategyFactory:
    """Fábrica polimórfica que gerencia e distribui as estratégias de atualização.
    
    Utiliza um dicionário interno para garantir o reuso de instâncias (Flyweight).
    """
    
    # O dicionário agora funciona estritamente como o cache de instâncias únicas (Flyweight)
    _flyweight_cache: Dict[str, UpdateStrategy] = {
        "brie": AgedBrieUpdateStrategy(),
        "sulfuras": SulfurasUpdateStrategy(),
        "passes": BackstagePassesUpdateStrategy(),
        "conjured": ConjuredUpdateStrategy()
    }
    
    _default_strategy: UpdateStrategy = CommonUpdateStrategy()

    @classmethod
    def get_strategy(cls, item_name: str) -> UpdateStrategy:
        """Determina a estratégia analisando substrings (categorias) e matches exatos (itens únicos)."""
        if not item_name:
            return cls._default_strategy

        # 1. Avaliação de Categorias por Substring (Aberto para Expansão)
        if "Aged Brie" in item_name:
            return cls._flyweight_cache["brie"]

        if "Backstage passes" in item_name:
            return cls._flyweight_cache["passes"]
            
        if "Conjured" in item_name:
            return cls._flyweight_cache["conjured"]

        # 2. Match Exato para Itens Lendários Únicos
        if item_name == "Sulfuras, Hand of Ragnaros":
            return cls._flyweight_cache["sulfuras"]

        # 3. Fallback para itens comuns
        return cls._default_strategy
```

#### Porque utilizar o flyweight_cache?

Se não utilizássemos o flyweight, em relação a comportamento, o sistema funcionaria exatamente da mesma forma. Os testes passariam e as regras de negócio seriam aplicadas com perfeição. 

Porém se a taverna tivesse 10.000 itens do tipo "Conjured Mana Cake" no inventário, o loop do caso de uso chamaria esse método 10.000 vezes. O Python criaria 10.000 objetos `ConjuredUpdateStrategy` na memória e, logo após o uso, descartaria todos eles.

Em sistemas de altíssima performance ou microsserviços que processam milhões de requisições por segundo, essa criação e destruição em massa de objetos idênticos gera um fenômeno chamado *Garbage Collector Spikes* (picos de processamento para limpar a memória), o que pode deixar o sistema lento por alguns milissegundos.

Por isso, manter aquele dicionário estático como um cache de instâncias únicas (reutilizando o mesmo objeto para sempre) é o que diferencia um código apenas funcional de um código com **visão de engenharia**.

Testes

Lembra que o sistema vinha tratando os itens conjurados como itens comuns, justamente por não terem sua regra de negócio definida ainda?

> [O autor do Kata colocou o item lá de propósito para que, na **Fase 4**, quando você implementar a lógica correta dos Conjurados, **o Approval Test quebre.** Ele vai falhar porque a nova saída (com a degradação rápida real) não vai bater com a saída antiga, onde ele se comportava como item comum.](https://app.notion.com/p/Gilded-Rose-Refactoring-Kata-371486a71eae80e59c7dedc0bb75c9c2?pvs=21)
> 

Pois então, após criarmos a nova estratégia específica dos itens conjurados onde eles não mais se comportam como itens comuns e sim possuem seus próprios requisitos, sendo eles:

> "Itens **'Conjured'** (Conjurados) degradam em sua qualidade duas vezes mais rápido que os itens normais."
> 
- **Item Comum Novo:** Perde `1` de qualidade antes do prazo e `2` de qualidade após o prazo (`sell_in < 0`).
- **Item Conjurado:** Perde `2` de qualidade antes do prazo e `4` de qualidade após o prazo (`sell_in < 0`).

O **Approval Test** é justamente o teste que vai denunciar essa mudança de comportamento. Por meio da Golden Master, os testes que guiaram a gente por toda refatoração, vai estar claro a mudança de comportamento do item Conjurado.

**Golden Master**

```
OMGHAI!
-------- day 0 --------
name, sellIn, quality
+5 Dexterity Vest, 10, 20
Aged Brie, 2, 0
Elixir of the Mongoose, 5, 7
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 15, 20
Backstage passes to a TAFKAL80ETC concert, 10, 49
Backstage passes to a TAFKAL80ETC concert, 5, 49
Conjured Mana Cake, 3, 6

-------- day 1 --------
name, sellIn, quality
+5 Dexterity Vest, 9, 19
Aged Brie, 1, 1
Elixir of the Mongoose, 4, 6
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 14, 21
Backstage passes to a TAFKAL80ETC concert, 9, 50
Backstage passes to a TAFKAL80ETC concert, 4, 50
Conjured Mana Cake, 2, 5

-------- day 2 --------
name, sellIn, quality
+5 Dexterity Vest, 8, 18
Aged Brie, 0, 2
Elixir of the Mongoose, 3, 5
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 13, 22
Backstage passes to a TAFKAL80ETC concert, 8, 50
Backstage passes to a TAFKAL80ETC concert, 3, 50
Conjured Mana Cake, 1, 4
```

#### Novo Approval test

```
OMGHAI!
-------- day 0 --------
name, sellIn, quality
+5 Dexterity Vest, 10, 20
Aged Brie, 2, 0
Elixir of the Mongoose, 5, 7
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 15, 20
Backstage passes to a TAFKAL80ETC concert, 10, 49
Backstage passes to a TAFKAL80ETC concert, 5, 49
Conjured Mana Cake, 3, 6

-------- day 1 --------
name, sellIn, quality
+5 Dexterity Vest, 9, 19
Aged Brie, 1, 1
Elixir of the Mongoose, 4, 6
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 14, 21
Backstage passes to a TAFKAL80ETC concert, 9, 50
Backstage passes to a TAFKAL80ETC concert, 4, 50
Conjured Mana Cake, 2, 4

-------- day 2 --------
name, sellIn, quality
+5 Dexterity Vest, 8, 18
Aged Brie, 0, 2
Elixir of the Mongoose, 3, 5
Sulfuras, Hand of Ragnaros, 0, 80
Sulfuras, Hand of Ragnaros, -1, 80
Backstage passes to a TAFKAL80ETC concert, 13, 22
Backstage passes to a TAFKAL80ETC concert, 8, 50
Backstage passes to a TAFKAL80ETC concert, 3, 50
Conjured Mana Cake, 1, 2

```

![image.png](image%2011.png)

Para assegurar que os itens Conjurados estão atendendo seus requisitos, precisamos adicionar **novos testes unitários e definir uma nova Golden Master.**

```python
# -*- coding: utf-8 -*-
from gilded_rose import GildedRose, Item

def test_conjured_item_degrades_twice_as_fast_before_expiry():
    # Item comum perderia 1 de qualidade, o Conjurado deve perder 2
    items = [Item("Conjured Mana Cake", sell_in=10, quality=20)]
    gilded_rose = GildedRose(items)
    
    gilded_rose.update_quality()
    
    assert items[0].sell_in == 9
    assert items[0].quality == 18

def test_conjured_item_degrades_twice_as_fast_after_expiry():
    # Item comum vencido perderia 2 de qualidade, o Conjurado deve perder 4
    items = [Item("Conjured Mana Cake", sell_in=0, quality=20)]
    gilded_rose = GildedRose(items)
    
    gilded_rose.update_quality()
    
    assert items[0].sell_in == -1
    assert items[0].quality == 16

def test_conjured_item_quality_never_drops_below_zero():
    items = [Item("Conjured Mana Cake", sell_in=5, quality=1)]
    gilded_rose = GildedRose(items)
    
    gilded_rose.update_quality()
    
    assert items[0].quality == 0
```
		

## Auditoria dos Critérios de Validação

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Implementação sem Impacto
- **Verificação:**
    - Para adicionar a nova regra dos Conjurados, não alteramos nenhuma linha das estratégias já existentes (`aged_brie.py`, `sulfuras.py`, etc.). O código antigo ficou totalmente **fechado para modificação**.
    
    ```python
    # -*- coding: utf-8 -*-
    from src.domain.item import Item
    from src.domain.strategies.base import UpdateStrategy
    from src.domain.constants import MIN_QUALITY
    
    class ConjuredUpdateStrategy(UpdateStrategy):
        """Estratégia de atualização para itens magicamente Conjurados.
        
        Degradam a qualidade duas vezes mais rápido que os itens comuns.
        """
        def update(self, item: Item) -> None:
            item.sell_in -= 1
            
            # Degrada 2 antes do prazo, e 4 após o vencimento
            degrade_amount = 4 if item.sell_in < 0 else 2
            
            item.quality = max(MIN_QUALITY, item.quality - degrade_amount)
    ```
    
    - A nova regra foi criada em um arquivo isolado, tornando o sistema **aberto para expansão**.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Novos Testes Unitários
- **Verificação:**
    - O arquivo de testes recebeu mais 3 testes de validação dos RF’S dos itens Conjurados foi criado cobrindo todos os cenários matemáticos exigidos:
    
    ```python
    def test_conjured_item_degrades_twice_as_fast_before_expiry():
        # Item comum perderia 1 de qualidade, o Conjurado deve perder 2
        items = [Item("Conjured Mana Cake", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        
        gilded_rose.update_quality()
        
        assert items[0].sell_in == 9
        assert items[0].quality == 18
    
    def test_conjured_item_degrades_twice_as_fast_after_expiry():
        # Item comum vencido perderia 2 de qualidade, o Conjurado deve perder 4
        items = [Item("Conjured Mana Cake", sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        
        gilded_rose.update_quality()
        
        assert items[0].sell_in == -1
        assert items[0].quality == 16
    
    def test_conjured_item_quality_never_drops_below_zero():
        items = [Item("Conjured Mana Cake", sell_in=5, quality=1)]
        gilded_rose = GildedRose(items)
        
        gilded_rose.update_quality()
        
        assert items[0].quality == 0
    ```
    
    - O Domínio não importa nada de `use_cases/` e muito menos de `infrastructure/`. A regra de dependência do Uncle Bob foi respeitada: o coração do sistema é agnóstico ao resto do mundo.
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Sucesso Global
- **Verificação:**
    - A execução do `pytest` retornou sucesso em **100% dos testes**. Tanto a rede de segurança dos 12 testes antigos (que protegem o comportamento histórico da taverna) quanto os novos testes unitários e o teste de aprovação do Golden Master (*Approval Tests*) estão cravados em **verde**.
    
    ![image.png](image%2012.png)
    
</aside>

<aside>
<img src="https://app.notion.com/icons/checklist_gray.svg" alt="https://app.notion.com/icons/checklist_gray.svg" width="40px" />

- [x]  Merge para a Main
- **Verificação:**
    - A branch local `feat/conjured-items` já recebeu todos os commits organizados e está com o código limpo, testado e empurrado para o GitHub (`git push`).
    
    ![image.png](image%2013.png)
    
    - O código encontra-se em estado maduro, pronto para sofrer o *Pull Request* e ser integrado com total segurança à branch principal (`main`).
</aside>

## :github: GitHub

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento

Foi criada uma branch exclusiva [**`feat/conjured-items`**](https://github.com/dultradev/GildedRose/tree/feat/conjured-items) para implementação dos novos itens Conjurados a partir da branch `develop`.

 Os commits realizados foram:

[Sem título](Sem%20t%C3%ADtulo%20384486a71eae80daabf4d66d89dab880.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/5](https://github.com/dultradev/GildedRose/pull/5)

**Objetivo do Pull Request**

Este PR consolida a **Fase 5: Expansão de Funcionalidade (Itens Conjurados)**. O objetivo foi introduzir a regra de negócio para os novos itens mágicos (*Conjured*), colocando à prova a arquitetura extensível construída nas fases anteriores. A implementação foi feita de forma puramente aditiva, seguindo o Princípio Aberto/Fechado (OCP).

---

**Critérios de Aceitação Cumpridos**

- [x]  **1. Implementação sem Impacto (Aderência ao OCP)**
    - Nenhuma das classes especialistas criadas na Fase 3 para os outros itens (*Aged Brie*, *Sulfuras*, *Backstage passes* ou *Common*) foi modificada para adicionar o item *Conjured*.
    - A nova regra foi isolada em sua própria classe (`ConjuredUpdateStrategy`), demonstrando que o sistema está fechado para modificação e aberto para expansão.
- [x]  **2. Novos Testes Unitários**
Foram adicionados testes unitários específicos para cobrir todos os cenários de comportamento dos itens *Conjured*:
    - **Degradação normal ($-2$):** Validação de que o item perde o dobro de qualidade antes do vencimento.
    - **Degradação pós-vencimento ($-4$):** Validação de que o item perde o dobro de qualidade após o prazo.
    - **Limites de qualidade:** Garantia de que a qualidade do item nunca cai abaixo do piso regulatório ($0$).
- [x]  **3. Sucesso Global (Zero Regressão)**
    - **100% dos testes estão passando em verde.**
    - A rede de segurança histórica (12 testes originais) continuou intacta. O teste de cobertura global do Golden Master (*Approval Tests*) foi atualizado e aprovado com sucesso, garantindo a consistência da simulação de 30 dias com o novo item no inventário.
- [x]  **4. Pronto para o Merge na Main**
    - O código foi revisado, os commits foram devidamente fatiados por responsabilidade técnica e a branch `feat/conjured-items` está estável e pronta para ser integrada com segurança na branch principal (`main`).

---

## Alterações Relevantes de Design (Bônus de Engenharia)

- **Generalização na Fábrica:**
    - A `ItemStrategyFactory` foi evoluída para identificar categorias por substring (`in`), permitindo que o sistema aceite qualquer variação futura de itens conjurados (ex: *"Conjured Mana Cake"*, *"Conjured Shirataki"*).
- **Consolidação do Padrão Flyweight:**
    - O dicionário interno da fábrica foi convertido em um `_flyweight_cache` estático para reutilizar as instâncias das estratégias em memória, otimizando o Garbage Collector do Python ao processar grandes volumes de itens.
</aside>

</aside>

# Relatório de Auditoria Final (O Sucesso do Projeto)

Com a conclusão da Fase 5, **finalizamos a refatoração do Gilded Rose Kata**. Abaixo segue uma tabela comparativa:

| Métrica de Engenharia | Estado Original (Legado) | Estado Atual (Fase 5) | Benefício Arquitetural |
| --- | --- | --- | --- |
| **Complexidade Ciclomática Principal** | Alta (Escadas de `if` aninhados) | **1 (Execução Linear)** | Código imutável e livre de bugs de desvio. |
| **Risco de Regressão em Alterações** | Altíssimo (Código acoplado) | **Zero** | Regras isoladas em arquivos independentes. |
| **Tempo para Inserir Novo Item** | Lento e Perigoso | **Minutos (Apenas adicionar arquivo)** | Total aderência ao princípio Aberto/Fechado. |
| **Gerenciamento de Memória** | Instanciação procedural instável | **Otimizado (Flyweight Cache)** | Baixo consumo de memória e alta performa |

## Árvore final

```python
gildedrose/
├── src/
│   ├── domain/                         # Camada de Domínio (Negócio Puro)
│   │   ├── __init__.py
│   │   ├── constants.py               # Limites globais (MAX_QUALITY, MIN_QUALITY)
│   │   ├── entities.py                # Entidade Item (Legada/Preservada)
│   │   └── strategies/                # Padrão Strategy para Atualização de Itens
│   │       ├── __init__.py
│   │       ├── base.py                # Interface Abstrata UpdateStrategy
│   │       ├── aged_brie.py           # Regras do Aged Brie
│   │       ├── backstage_passes.py    # Regras do Backstage Passes
│   │       ├── common.py              # Regras de Itens Comuns
│   │       ├── conjured.py            # Regras de Itens Conjurados (Fase 5)
│   │       └── sulfuras.py            # Regras das Sulfuras
│   │
│   ├── use_cases/                      # Camada de Casos de Uso (Orquestração)
│   │   ├── __init__.py
│   │   ├── factory.py                 # Fábrica Polimórfica com Flyweight Cache
│   │   └── update_inventory.py        # Caso de Uso Principal (Update Inventory)
│   │
│   └── infrastructure/                 # Camada de Infraestrutura e Adaptação
│       └── __init__.py
│       └── gilded_rose_adapter.py
│
├── tests/                              # Suíte de Testes Automatizados
│   ├── __init__.py
│   ├── test_gilded_rose.py            # Testes Unitários e de Regressão
│   ├── test_conjured.py               # Testes de Unidade Específicos para Conjurados
│   └── approved_files/                # Artefatos do Golden Master (Approval Tests)
│
├── gilded_rose.py                      # Padrão Facade / Ponto de Entrada Legado
├── texttest_fixture.py                 # Fixture de Simulação por Linha de Comando
├── requirements.txt                    # Dependências do Projeto
└── README.md                           # Documentação Técnica

```

## Detalhamento das fases

Fase 1

### Fase 1: Escrevendo a Rede de Segurança (Testes)

- **O Cenário Inicial:**
    - O código era uma caixa preta com alta complexidade ciclomática. Mudar uma linha corria o risco de quebrar o comportamento de múltiplos itens.
- **O que foi feito:**
    - Escrevemos 12 testes unitários mapeando o comportamento exato de cada item (*Aged Brie*, *Sulfuras*, *Backstage passes* e itens comuns) antes e depois do vencimento, além de configurar o teste de aprovação global (*Golden Master / Approval Tests*) para uma simulação de 30 dias.
- **Ganho Técnico:**
    - **Confiança.**
        - Criamos uma rede de segurança que garantiu que nenhuma refatoração subsequente alterasse o comportamento matemático do negócio.

Fase 2

### Fase 2: Cláusulas de Guarda e Código Calistênico

- **O Cenário Inicial:**
    - Uma escada de `if/else` aninhados profundamente espalhada por mais de 70 linhas de código.
- **O que foi feito:**
    - Aplicamos a técnica de **Cláusulas de Guarda (Guard Clauses)**. Invertemos as condicionais para retornar erros e validar os limites de qualidade (`0` e `50`) logo no início do fluxo, limpando o caminho feliz.
- **Ganho Técnico:**
    - **Legibilidade.**
        - Reduzimos o aninhamento de código a zero e preparamos a estrutura para o mapeamento polimórfico.

Fase 3

### Fase 3: O Padrão Strategy (Orientação a Objetos de Verdade)

- **O Cenário Inicial:**
    - Embora o código estivesse mais legível, a classe principal ainda acumulava a responsabilidade de saber as regras de atualização de *todos* os itens do mundo (Violação do SRP).
- **O que foi feito:**
    - Implementamos o padrão de projeto **Strategy** combinando com uma **Fábrica Polimórfica**. Isolamos a lógica de cada item em sua própria classe especialista derivada de uma classe base abstrata (`UpdateStrategy`).
- **Ganho Técnico:**
    - **Separação de Responsabilidades (SRP).**
        - A classe principal parou de adivinhar regras e passou apenas a delegar o comportamento.

Fase 4

### Fase 4: Desacoplamento com Arquitetura Limpa

- **O Cenário Inicial:**
    - O código estava modularizado, mas os arquivos de estratégia e a fábrica estavam todos misturados na raiz, confundindo design de código com arquitetura.
- **O que foi feito:**
    - Separamos o projeto em 3 camadas estritas de acordo com o Uncle Bob:
        - **Domínio** (estratégias e constantes puras)
        - **Casos de Uso** (Fábrica e o caso de uso `UpdateInventoryUseCase`) e
        - **Infraestrutura** (a classe `GildedRose` atuando como um *Boundary Adapter*).
        - Usamos o padrão **Facade** na raiz para manter a retrocompatibilidade com os testes antigos.
- **Ganho Técnico:**
    - **Independência de Tecnologia.**
        - O coração do negócio ficou 100% isolado de entradas e saídas e de restrições do código legado.

Fase 5

### Fase 5: Expansão de Funcionalidade (O Item Conjurado)

- **O Cenário Inicial:**
    - O negócio solicitou a adição do item *Conjured*, que degrada a qualidade duas vezes mais rápido.
- **O que foi feito:**
    - Graças à arquitetura das fases anteriores, apenas criamos o arquivo `conjured.py` com a nova estratégia e a registramos no cache da fábrica. Evoluímos a fábrica para ler categorias por substring (`in`) e aplicamos o padrão **Flyweight Cache** para otimizar o uso de memória.
- **Ganho Técnico:**
    - **Total aderência ao Princípio Aberto/Fechado (OCP).**
        - Expandimos o sistema escrevendo código novo, com zero impacto e zero alteração no código antigo.
		

## Versionamento final

<aside>
<img src="https://app.notion.com/icons/git_gray.svg" alt="https://app.notion.com/icons/git_gray.svg" width="40px" />

#### Versionamento Final

[Sem título](Sem%20t%C3%ADtulo%20384486a71eae809abcc8cbfc916047e8.csv)

<aside>
<img src="https://app.notion.com/icons/branch-merge_gray.svg" alt="https://app.notion.com/icons/branch-merge_gray.svg" width="40px" />

#### Pull Request

[https://github.com/dultradev/GildedRose/pull/6](https://github.com/dultradev/GildedRose/pull/6)

**Objetivo do Pull Request**

Este PR consolida a **Fase 5: Expansão de Funcionalidade (Itens Conjurados)**. O objetivo foi introduzir a regra de negócio para os novos itens mágicos (*Conjured*), colocando à prova a arquitetura extensível construída nas fases anteriores. A implementação foi feita de forma puramente aditiva, seguindo o Princípio Aberto/Fechado (OCP).

---

**Critérios de Aceitação Cumpridos**

- [x]  **1. Implementação sem Impacto (Aderência ao OCP)**
    - Nenhuma das classes especialistas criadas na Fase 3 para os outros itens (*Aged Brie*, *Sulfuras*, *Backstage passes* ou *Common*) foi modificada para adicionar o item *Conjured*.
    - A nova regra foi isolada em sua própria classe (`ConjuredUpdateStrategy`), demonstrando que o sistema está fechado para modificação e aberto para expansão.
- [x]  **2. Novos Testes Unitários**
Foram adicionados testes unitários específicos para cobrir todos os cenários de comportamento dos itens *Conjured*:
    - **Degradação normal ($-2$):** Validação de que o item perde o dobro de qualidade antes do vencimento.
    - **Degradação pós-vencimento ($-4$):** Validação de que o item perde o dobro de qualidade após o prazo.
    - **Limites de qualidade:** Garantia de que a qualidade do item nunca cai abaixo do piso regulatório ($0$).
- [x]  **3. Sucesso Global (Zero Regressão)**
    - **100% dos testes estão passando em verde.**
    - A rede de segurança histórica (12 testes originais) continuou intacta. O teste de cobertura global do Golden Master (*Approval Tests*) foi atualizado e aprovado com sucesso, garantindo a consistência da simulação de 30 dias com o novo item no inventário.
- [x]  **4. Pronto para o Merge na Main**
    - O código foi revisado, os commits foram devidamente fatiados por responsabilidade técnica e a branch `feat/conjured-items` está estável e pronta para ser integrada com segurança na branch principal (`main`).

---

**Alterações Relevantes de Design (Bônus de Engenharia)**

- **Generalização na Fábrica:**
    - A `ItemStrategyFactory` foi evoluída para identificar categorias por substring (`in`), permitindo que o sistema aceite qualquer variação futura de itens conjurados (ex: *"Conjured Mana Cake"*, *"Conjured Shirataki"*).
- **Consolidação do Padrão Flyweight:**
    - O dicionário interno da fábrica foi convertido em um `_flyweight_cache` estático para reutilizar as instâncias das estratégias em memória, otimizando o Garbage Collector do Python ao processar grandes volumes de itens.
</aside>

</aside>