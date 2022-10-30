from dataclasses import dataclass
from typing import List

from item.item import Item


@dataclass
class ListaCompras:
    __itens : List[Item]
    nome: str
    descricao: str | None

    def adicionar_item(self, item: Item) -> None:
        self.__itens.append(item)
    
    def remover_item(self, item: Item) -> None:
        self.__itens.remove(item)

    def obter_itens(self) -> List[Item]:
        return self.__itens
