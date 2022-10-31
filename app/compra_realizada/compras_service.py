from datetime import date
from decimal import Decimal
from typing import List

from app.compra_realizada.compra import Compra
from app.item.item import Item
from app.item.item_comprado import ItemComprado


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
        itens: List[dict],
    ) -> None:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        lista = usuario.obter_lista(nome_lista_base)
        if not lista:
            raise ValueError("Essa lista não existe")

        compra = Compra(
            data_compra=data_compra,
            mercado=mercado,
            lista_compras_base=lista,
            valor_total=valor_total,
        )

        try:
            for item_cadastrado in itens:
                preco = item_cadastrado["preco"]
                nome_item = item_cadastrado["nome"]
                quantidade = item_cadastrado["quantidade"]

                item = Item(nome_item)
                item_comprado = ItemComprado(
                    item=item,
                    preco=Decimal(preco),
                    data_compra=data_compra,
                    mercado=mercado,
                    quantidade=int(quantidade),
                )
                compra.adicionar_item_comprado(item_comprado)
        except Exception as error:
            raise ValueError("Item inválido.") from error

        usuario.cadastrar_compra(compra)

    @staticmethod
    def remover_compra(
        usuario: "Usuario", data_compra: date, nome_mercado: str
    ) -> None:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        compra = usuario.obter_compra(data_compra, mercado)
        if not compra:
            raise ValueError("Essa compra não foi realizada")

        usuario.remover_compra(compra)

    @staticmethod
    def listar_itens_compra(
        usuario: "Usuario", data_compra: date, nome_mercado: str
    ) -> List[ItemComprado]:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        compra = usuario.obter_compra(data_compra, mercado)
        if not compra:
            raise ValueError("Essa compra não foi realizada")

        return compra.obter_itens_comprados()

    @staticmethod
    def obter_valor_extra(
        usuario: "Usuario", data_compra: date, nome_mercado: str
    ) -> Decimal:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Esse Mercado não existe")

        compra = usuario.obter_compra(data_compra, mercado)
        if not compra:
            raise ValueError("Essa compra não foi realizada")

        return compra.obter_valor_itens_fora_da_lista()
