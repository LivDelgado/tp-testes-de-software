from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from item.item import Item
from mercado.mercado import Mercado

@dataclass
class ItemComprado:
    """
    Item comprado - o item associado a um preço e uma data
    """
    item: Item
    preco: Decimal
    data_compra: date
    mercado: Mercado
