# test_gilded_rose.py
from gilded_rose import Item, GildedRose

# ==========================================
# 📦 1. ITENS COMUNS (RF-01 ao RF-05)
# ==========================================

def test_item_comum_degrada_qualidade_e_sell_in_corretamente():
    """RF-01 & RF-02: Item comum perde 1 de SellIn e 1 de Quality antes do vencimento"""
    items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == 9
    assert items[0].quality == 19

def test_item_comum_degrada_em_dobro_apos_vencimento():
    """RF-03: Quando vencido (SellIn < 0), a qualidade cai de 2 em 2"""
    items = [Item(name="+5 Dexterity Vest", sell_in=0, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 18

def test_qualidade_de_um_item_nunca_e_negativa():
    """RF-04: Qualidade do item comum não pode cair abaixo de 0"""
    items = [Item(name="Elixir of the Mongoose", sell_in=5, quality=0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 0

# ==========================================
# 🧀 2. AGED BRIE (RF-05 ao RF-07)
# ==========================================

def test_aged_brie_limite_maximo_de_qualidade():
    """RF-05: Qualidade do Brie nunca pode passar de 50"""
    items = [Item(name="Aged Brie", sell_in=5, quality=50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 50

def test_aged_brie_aumenta_qualidade_conforme_envelhece():
    """RF-06: Aged Brie ganha +1 de qualidade antes do vencimento"""
    items = [Item(name="Aged Brie", sell_in=5, quality=10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 11

def test_aged_brie_ganha_qualidade_em_dobro_apos_vencimento():
    """RF-07: A pegadinha do código legado! Vencido, o Brie ganha +2 de qualidade"""
    items = [Item(name="Aged Brie", sell_in=0, quality=10)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 12

# ==========================================
# 🌋 3. SULFURAS (RF-11.1 ao RF-11.3)
# ==========================================

def test_sulfuras_permanece_imutavel():
    """RF-08 & RF-10: Item lendário não altera SellIn e nem Quality"""
    items = [Item(name="Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == 10
    assert items[0].quality == 80

# ==========================================
# 🎟️ 4. BACKSTAGE PASSES (RF-08 ao RF-11)
# ==========================================

def test_backstage_passes_com_mais_de_10_dias():
    """RF-11: Aumenta em 1 quando faltam mais de 10 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 21

def test_backstage_passes_com_10_dias_ou_menos():
    """RF-12: Aumenta em 2 quando faltam entre 6 e 10 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 22

def test_backstage_passes_com_5_dias_ou_menos():
    """RF-13: Aumenta em 3 quando faltam entre 0 e 5 dias"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == 23

def test_backstage_passes_apos_o_show():
    """RF-14: Qualidade cai para 0 imediatamente após o show (SellIn < 0)"""
    items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == -1
    assert items[0].quality == 0