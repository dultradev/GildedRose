# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.domain.item import Item

class UpdateStrategy(ABC):
    """Interface base para as estratégias de atualização de itens."""

    @abstractmethod
    def update(self, item: Item) -> None:
        pass