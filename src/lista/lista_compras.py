from dataclasses import dataclass, field
from typing import List

from item import Item


@dataclass
class ListaCompras:
    nome: str
    descricao: str | None
    __itens: List[Item] = field(default_factory=lambda : [])

    def adicionar_item(self, item: Item) -> None:
        self.__itens.append(item)
    
    def remover_item(self, item: Item) -> None:
        self.__itens.remove(item)

    def obter_itens(self) -> List[Item]:
        return self.__itens
