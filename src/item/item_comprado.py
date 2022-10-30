from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from item import Item
from mercado import Mercado

@dataclass
class ItemComprado:
    """
    Item comprado - o item associado a um preço e uma data
    """
    item: Item
    preco: Decimal
    data_compra: date
    mercado: Mercado
    quantidade: int = 1

    @property
    def valor_total(self) -> Decimal:
        return self.preco * self.quantidade
