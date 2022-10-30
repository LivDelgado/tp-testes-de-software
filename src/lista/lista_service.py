from usuario import Usuario
from typing import List

from item import Item
from lista import ListaCompras


class ListaService:
    @staticmethod
    def obter_listas(usuario: Usuario) -> List[ListaCompras]:
        listas = usuario.obter_listas()
        if not listas:
            raise ValueError("Nenhuma lista encontrada")

        return listas

    @staticmethod
    def adicionar_lista(
        usuario: Usuario, nome: str, descricao: str | None, itens: List[str]
    ) -> None:
        lista = ListaCompras(nome=nome, descricao=descricao)

        for nome_item in itens:
            novo_item = Item(nome=nome_item)
            lista.adicionar_item(novo_item)

        usuario.adicionar_lista(lista)

    @staticmethod
    def remover_lista(usuario: Usuario, nome: str) -> None:
        usuario.remover_lista(nome)

    @staticmethod
    def listar_itens(usuario: Usuario, nome: str) -> List[Item]:
        lista = usuario.obter_lista(nome)
        if lista:
            itens = lista.obter_itens()
            return itens

        raise ValueError("Essa lista não existe")

    @staticmethod
    def adicionar_item_lista(usuario: Usuario, nome: str, nome_item: str) -> None:
        lista = usuario.obter_lista(nome)
        if lista:
            lista.adicionar_item(Item(nome=nome_item))
        else:
            raise ValueError("Essa lista não existe")

    @staticmethod
    def remover_item_lista(usuario: Usuario, nome: str, nome_item: str) -> None:
        lista = usuario.obter_lista(nome)
        if lista:
            lista.remover_item(Item(nome=nome_item))
        else:
            raise ValueError("Essa lista não existe")
