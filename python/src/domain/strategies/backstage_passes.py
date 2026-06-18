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