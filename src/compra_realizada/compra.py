from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from item.item_comprado import Item, ItemComprado
from mercado.mercado import Mercado


@dataclass
class Compra:
    data_compra: date
    mercado: Mercado
    lista_compras_base: "ListaCompras"
    valor_total: Decimal
    __itens_comprados: List[ItemComprado] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return f"{self.data_compra} - {self.mercado} => {self.valor_total}"

    def adicionar_item_comprado(self, item: ItemComprado) -> None:
        if not self.obter_item_comprado(item.item):
            self.__itens_comprados.append(item)

    def remover_item(self, item: ItemComprado) -> None:
        if self.obter_item_comprado(item.item):
            self.__itens_comprados.remove(item)

    def obter_item_comprado(self, item: Item) -> Optional[ItemComprado]:
        return next(
            (
                item_comprado
                for item_comprado in self.__itens_comprados
                if item_comprado.item == item
            ),
            None,
        )

    def obter_itens_comprados(self) -> List[ItemComprado]:
        return self.__itens_comprados

    def obter_valor_itens_fora_da_lista(self) -> Decimal:
        itens_fora_da_lista = self.obter_itens_fora_da_lista()
        return sum(item.valor_total for item in itens_fora_da_lista)

    def obter_itens_fora_da_lista(self):
        itens_lista_base = {
            item.nome: True for item in self.lista_compras_base.obter_itens()
        }
        itens_fora_da_lista = [
            item_comprado
            for item_comprado in self.__itens_comprados
            if not itens_lista_base[item_comprado.item.nome]
        ]
        return itens_fora_da_lista
