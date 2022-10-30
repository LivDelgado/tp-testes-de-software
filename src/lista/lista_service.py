from usuario.usuario import Usuario
from typing import List

from item import Item
from lista import ListaCompras

class ListaService:

    @staticmethod
    def imprimir_listas(usuario: Usuario) -> None:
        for lista in usuario.obter_listas():
            print(lista.nome, lista.descricao, sep=' - ')

    @staticmethod
    def adicionar_lista(usuario: Usuario, nome: str, descricao: str | None, itens: List[str]) -> None:
        lista = ListaCompras(nome=nome, descricao=descricao)
        for item in itens:
            lista.adicionar_item(Item(nome=item))

        usuario.adicionar_lista(lista)
