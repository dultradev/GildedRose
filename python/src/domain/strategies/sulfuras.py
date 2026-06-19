# -*- coding: utf-8 -*-
from src.domain.item import Item
from src.domain.strategies.base import UpdateStrategy

class SulfurasUpdateStrategy(UpdateStrategy):
    """Estratégia de atualização para o item lendário 'Sulfuras'."""
    def update(self, item: Item) -> None:
        # Item lendário permanece intocável
        pass