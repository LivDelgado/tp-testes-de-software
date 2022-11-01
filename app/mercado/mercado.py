from dataclasses import dataclass


@dataclass
class Mercado:
    nome: str

    def __str__(self) -> str:
        return self.nome

    def __hash__(self):
        return hash(self.nome)
