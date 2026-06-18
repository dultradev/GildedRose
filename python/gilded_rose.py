# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List, Dict

# ==========================================
# --- CLASSE ITEM - RESTRIÇÃO DO GOBLIN ---
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

# =============================
# --- STRATEGY PATTERN ---
# =============================
class UpdateStrategy(ABC):
    """Interface base para as estratégias de atualização de itens."""
    
    @abstractmethod
    def update(self, item: Item) -> None:
        """Atualiza a qualidade e o prazo de venda (sell_in) de um item.

        Args:
            item (Item): A instância do item a ser atualizada.
        """
        pass


class CommonUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para itens comuns."""
    
    def update(self, item: Item) -> None:
        item.sell_in -= 1

        if item.quality > 0:
            item.quality -= 1
            
            # Se já venceu, degrada em dobro (-2 no total)
            if item.sell_in < 0 and item.quality > 0:
                item.quality -= 1


class AgedBrieUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item 'Aged Brie'."""
    
    def update(self, item: Item) -> None:
        item.sell_in -= 1
        
        if item.quality < 50:
            item.quality += 1
            
            # Se já passou do prazo, ganha qualidade em dobro
            if item.sell_in < 0 and item.quality < 50:
                item.quality += 1


class BackstagePassesUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para 'Backstage passes'."""
    
    def update(self, item: Item) -> None:
        item.sell_in -= 1

        # Se o show já passou, o ingresso perde todo o valor
        if item.sell_in < 0:
            item.quality = 0
            return

        if item.quality < 50:
            item.quality += 1

            # Janela crítica de 10 dias ou menos (ganha +1 adicional)
            if item.sell_in < 10 and item.quality < 50:
                item.quality += 1

            # Janela crítica de 5 dias ou menos (ganha +1 adicional)
            if item.sell_in < 5 and item.quality < 50:
                item.quality += 1


class SulfurasUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item lendário 'Sulfuras'."""
    
    def update(self, item: Item) -> None:
        # Itens lendários não mudam prazo de validade nem qualidade
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