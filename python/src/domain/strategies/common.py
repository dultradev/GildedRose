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