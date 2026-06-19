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