from dataclasses import dataclass


@dataclass
class Item:
    nome: str

    def __str__(self) -> str:
        return self.nome
