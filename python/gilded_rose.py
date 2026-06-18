# -*- coding: utf-8 -*-

# ==========================================
# 🗺️ 1. INTERFACE BASE DO STRATEGY
# ==========================================
class UpdateStrategy:
    def __init__(self, item):
        self.item = item

    def update_quality(self):
        """Método abstrato/contrato que todas as subclasses devem implementar"""
        raise NotImplementedError


# ==========================================
# 🧪 2. ESTRATÉGIAS ESPECIALIZADAS (SUBCLASSES)
# ==========================================
class StandardItemStrategy(UpdateStrategy):
    def update_quality(self):
        self.item.sell_in -= 1
        if self.item.quality > 0:
            self.item.quality -= 1
            if self.item.sell_in < 0 and self.item.quality > 0:
                self.item.quality -= 1


class AgedBrieStrategy(UpdateStrategy):
    def update_quality(self):
        self.item.sell_in -= 1
        if self.item.quality < 50:
            self.item.quality += 1
            if self.item.sell_in < 0 and self.item.quality < 50:
                self.item.quality += 1


class BackstagePassStrategy(UpdateStrategy):
    def update_quality(self):
        self.item.sell_in -= 1
        if self.item.sell_in < 0:
            self.item.quality = 0
            return

        if self.item.quality < 50:
            self.item.quality += 1
            if self.item.sell_in < 10 and self.item.quality < 50:
                self.item.quality += 1
            if self.item.sell_in < 5 and self.item.quality < 50:
                self.item.quality += 1


class SulfurasStrategy(UpdateStrategy):
    def update_quality(self):
        # Item lendário não altera prazo nem qualidade
        pass


# ==========================================
# 🏭 3. FABRICA DE ESTRATÉGIAS (SIMPLE FACTORY)
# ==========================================
class ItemStrategyFactory:
    _STRATEGIES = {
        "Aged Brie": AgedBrieStrategy,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy,
        "Sulfuras, Hand of Ragnaros": SulfurasStrategy
    }

    @classmethod
    def create(cls, item):
        # Se o nome do item estiver mapeado, usa a estratégia dele; caso contrário, é um item comum.
        strategy_class = cls._STRATEGIES.get(item.name, StandardItemStrategy)
        return strategy_class(item)


# ==========================================
# 🏰 4. CLASSE PRINCIPAL (PONTO DE ENTRADA LEGADO)
# ==========================================
class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # O método central agora é 100% polimórfico e livre de checagens de string!
        for item in self.items:
            strategy = ItemStrategyFactory.create(item)
            strategy.update_quality()


# ==========================================
# ⚠️ CLASSE ITEM INTACTA (RESTRIÇÃO DO GOBLIN)
# ==========================================
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)