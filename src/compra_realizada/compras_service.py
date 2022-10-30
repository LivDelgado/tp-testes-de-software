from datetime import date
from decimal import Decimal
from typing import List

from compra_realizada import Compra
from item import ItemComprado

class ComprasService:
    @staticmethod
    def obter_historico_compras(usuario: "Usuario") -> List[Compra]:
        compras = usuario.obter_historico_compras()
        if not compras:
            raise ValueError("Nenhuma compra encontrada")

        return compras

    @staticmethod
    def adicionar_compra(
        usuario: "Usuario",
        data_compra: date,
        nome_mercado: str,
        nome_lista_base: str,
        valor_total: Decimal,
        itens: List[ItemComprado]
    ) -> None:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        lista = usuario.obter_lista(nome_lista_base)
        if not lista:
            raise ValueError("Essa lista não existe")

        compra = Compra(
            data_compra = data_compra,
            mercado = mercado,
            lista_compras_base = lista,
            valor_total = valor_total
        )
        for item in itens:
            compra.adicionar_item_comprado(item)

        usuario.cadastrar_compra(compra)

    @staticmethod
    def remover_compra(usuario: "Usuario", data_compra: date, nome_mercado: str) -> None:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        compra = usuario.obter_compra(data_compra, mercado)
        if not compra:
            raise ValueError("Essa compra não foi realizada")
        
        usuario.remover_compra(compra)

