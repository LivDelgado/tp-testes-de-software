from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from app.item.item import Item
from app.mercado.mercado import Mercado


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

    def __str__(self) -> str:
        return f"{self.quantidade}x {self.item} - {self.preco} => {self.valor_total}"
