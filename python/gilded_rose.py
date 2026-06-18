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