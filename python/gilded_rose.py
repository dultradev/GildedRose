# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        # O laço principal agora apenas lê o nome e direciona para a função correta
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                self._update_sulfuras(item)
            elif item.name == "Aged Brie":
                self._update_aged_brie(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self._update_backstage_passes(item)
            else:
                self._update_common_item(item)

    def _update_aged_brie(self, item):
        # RF-01 & RF-06: Diminui o prazo de venda e aumenta a qualidade
        item.sell_in -= 1
        
        if item.quality < 50:
            item.quality += 1
            
            # RF-07: Se já passou do prazo, ganha qualidade em dobro
            if item.sell_in < 0 and item.quality < 50:
                item.quality += 1

    def _update_backstage_passes(self, item):
        # RF-01: Diminui o prazo de venda
        item.sell_in -= 1

        # RF-14: Se o show já passou, o ingresso perde todo o valor
        if item.sell_in < 0:
            item.quality = 0
            return

        # RF-11: Valorização padrão (+1)
        if item.quality < 50:
            item.quality += 1

            # RF-12: Janela crítica de 10 dias ou menos (ganha +1 adicional, totalizando +2)
            if item.sell_in < 10 and item.quality < 50:
                item.quality += 1

            # RF-13: Janela crítica de 5 dias ou menos (ganha +1 adicional, totalizando +3)
            if item.sell_in < 5 and item.quality < 50:
                item.quality += 1

    def _update_common_item(self, item):
        # RF-01: Diminui o prazo de venda
        item.sell_in -= 1

        # RF-02 & RF-04: Degradação padrão respeitando o piso de 0
        if item.quality > 0:
            item.quality -= 1
            
            # RF-03: Se já venceu, degrada em dobro (-2 no total)
            if item.sell_in < 0 and item.quality > 0:
                item.quality -= 1

    def _update_sulfuras(self, item):
        # RF-11.1, RF-11.2, RF-11.3: Itens lendários não mudam nada
        pass

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)