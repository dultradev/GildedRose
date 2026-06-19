# -*- coding: utf-8 -*-
from typing import Dict
from src.domain.strategies.base import UpdateStrategy
from src.domain.strategies.common import CommonUpdateStrategy
from src.domain.strategies.aged_brie import AgedBrieUpdateStrategy
from src.domain.strategies.backstage_passes import BackstagePassesUpdateStrategy
from src.domain.strategies.sulfuras import SulfurasUpdateStrategy
from src.domain.strategies.conjured import ConjuredUpdateStrategy

class ItemStrategyFactory:
    """Fábrica polimórfica que gerencia e distribui as estratégias de atualização.
    
    Utiliza um dicionário interno para garantir o reuso de instâncias (Flyweight).
    """
    
    # O dicionário agora funciona estritamente como o cache de instâncias únicas (Flyweight)
    _flyweight_cache: Dict[str, UpdateStrategy] = {
        "brie": AgedBrieUpdateStrategy(),
        "sulfuras": SulfurasUpdateStrategy(),
        "passes": BackstagePassesUpdateStrategy(),
        "conjured": ConjuredUpdateStrategy()
    }
    
    _default_strategy: UpdateStrategy = CommonUpdateStrategy()

    @classmethod
    def get_strategy(cls, item_name: str) -> UpdateStrategy:
        """Determina a estratégia analisando substrings (categorias) e matches exatos (itens únicos)."""
        if not item_name:
            return cls._default_strategy

        # 1. Avaliação de Categorias por Substring (Aberto para Expansão)
        if "Aged Brie" in item_name:
            return cls._flyweight_cache["brie"]

        if "Backstage passes" in item_name:
            return cls._flyweight_cache["passes"]
            
        if "Conjured" in item_name:
            return cls._flyweight_cache["conjured"]

        # 2. Match Exato para Itens Lendários Únicos
        if item_name == "Sulfuras, Hand of Ragnaros":
            return cls._flyweight_cache["sulfuras"]

        # 3. Fallback para itens comuns
        return cls._default_strategy