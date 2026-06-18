# -*- coding: utf-8 -*-
from typing import List
from src.domain.item import Item
from src.use_cases.factory import ItemStrategyFactory

class UpdateInventoryUseCase:
    """Caso de Uso Puro: Gerencia a orquestração da atualização de inventário."""

    def execute(self, items: List[Item]) -> None:
        """Itera sobre o inventário e aplica as atualizações de qualidade e validade."""
        for item in items:
            strategy = ItemStrategyFactory.get_strategy(item.name)
            strategy.update(item)