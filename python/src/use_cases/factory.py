# -*- coding: utf-8 -*-
from typing import Dict
from src.domain.strategies.base import UpdateStrategy
from src.domain.strategies.common import CommonUpdateStrategy
from src.domain.strategies.aged_brie import AgedBrieUpdateStrategy
from src.domain.strategies.backstage_passes import BackstagePassesUpdateStrategy
from src.domain.strategies.sulfuras import SulfurasUpdateStrategy

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
        """Obtém a estratégia de atualização apropriada para o nome do item."""
        return cls._strategies.get(item_name, cls._default_strategy)