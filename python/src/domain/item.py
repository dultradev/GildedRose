# -*- coding: utf-8 -*-

class Item:
    """Modelo de domínio representando um item do inventário da taverna.

    Note:
        De acordo com as regras do Gilded Rose Kata, esta classe
        não deve ser modificada.
    """

    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)