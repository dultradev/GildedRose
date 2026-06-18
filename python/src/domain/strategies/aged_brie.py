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