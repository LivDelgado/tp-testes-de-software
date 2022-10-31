from dataclasses import dataclass, field
from typing import List, Optional

from app.item.item import Item


@dataclass
class ListaCompras:
    nome: str
    descricao: str | None
    __itens: List[Item] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return f"{self.nome} {self.descricao or ''}"

    def adicionar_item(self, item: Item) -> None:
        if not self.obter_item(item):
            self.__itens.append(item)

    def remover_item(self, item: Item) -> None:
        self.__itens.remove(item)

    def obter_itens(self) -> List[Item]:
        return self.__itens

    def obter_item(self, item: Item) -> Optional[Item]:
        return next(
            (item_lista for item_lista in self.__itens if item_lista == item), None
        )
