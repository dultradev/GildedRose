# -*- coding: utf-8 -*-
from typing import List
from src.domain.item import Item
from src.use_cases.update_inventory import UpdateInventoryUseCase

class GildedRose:
    """Gerenciador principal do inventário da taverna Gilded Rose.
    
    Atua como um adaptador (Infrastructure Layer) para conectar
    interfaces legadas ao caso de uso limpo.
    """

    def __init__(self, items: List[Item]) -> None:
        """Inicializa o inventário.

        Args:
            items (List[Item]): Lista de itens disponíveis na taverna.
        """
        self.items = items
        self._update_use_case = UpdateInventoryUseCase()

    def update_quality(self) -> None:
        """Delega o trabalho pesado para o Caso de Uso correspondente."""
        self._update_use_case.execute(self.items)