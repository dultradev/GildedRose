# -*- coding: utf-8 -*-
"""Arquivo de fachada mantido para preservar a compatibilidade com o sistema legado."""

from src.domain.item import Item
from src.infrastructure.gilded_rose_adapter import GildedRose

__all__ = ["Item", "GildedRose"]