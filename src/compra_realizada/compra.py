from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List
from item.item_comprado import ItemComprado
from lista.lista_compras import ListaCompras

from mercado.mercado import Mercado


@dataclass
class Compra:
    data_compra: date
    mercado: Mercado
    lista_compras_base: ListaCompras
    valor_total: Decimal
    __itens_comprados: List[ItemComprado] = field(default_factory=lambda: [])

    def adicionar_item_comprado(self, item: ItemComprado) -> None:
        self.__itens_comprados.append(item)

    def remover_item(self, item: ItemComprado) -> None:
        self.__itens_comprados.remove(item)

    def obter_itens_comprados(self) -> List[ItemComprado]:
        return self.__itens_comprados

    def obter_valor_itens_fora_da_lista(self) -> Decimal:
        itens_fora_da_lista = self.obter_itens_fora_da_lista()
        return sum(item.preco for item in itens_fora_da_lista)

    def obter_itens_fora_da_lista(self):
        itens_lista_base = {
            item.nome: True for item in self.lista_compras_base.obter_itens()
        }
        return [
            item for item in self.__itens_comprados if not itens_lista_base[item.nome]
        ]
