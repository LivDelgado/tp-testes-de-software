from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from app.compra_realizada.compra import Compra
from app.item.item import Item
from app.mercado.mercado import Mercado


@dataclass
class Usuario:
    __listas: List["ListaCompras"] = field(default_factory=lambda: [])
    __compras_realizadas: List[Compra] = field(default_factory=lambda: [])
    __mercados: List[Mercado] = field(default_factory=lambda: [])

    def obter_listas(self) -> List["ListaCompras"]:
        return self.__listas

    def obter_lista(self, nome: str) -> Optional["ListaCompras"]:
        for lista in self.__listas:
            if lista.nome == nome:
                return lista
        return None

    def adicionar_lista(self, lista: "ListaCompras") -> None:
        if self.obter_lista(lista.nome):
            raise ValueError(
                "Não é permitido adicionar mais de uma lista com o mesmo nome"
            )

        self.__listas.append(lista)

    def remover_lista(self, nome: str) -> None:
        lista = self.obter_lista(nome)
        if not lista:
            raise ValueError("Essa lista não existe")

        self.__listas.remove(lista)

    def obter_historico_compras(self) -> List[Compra]:
        return self.__compras_realizadas

    def cadastrar_compra(self, compra: Compra) -> None:
        if not self.obter_compra(compra.data_compra, compra.mercado):
            self.__compras_realizadas.append(compra)

    def obter_compra(self, data_compra: date, mercado: Mercado) -> Optional[Compra]:
        return next(
            (
                compra
                for compra in self.__compras_realizadas
                if compra.data_compra == data_compra and compra.mercado == mercado
            ),
            None,
        )

    def remover_compra(self, compra: Compra) -> None:
        if self.obter_compra(compra.data_compra, compra.mercado):
            self.__compras_realizadas.remove(compra)

    def listar_mercados(self) -> List[Mercado]:
        return self.__mercados

    def obter_mercado(self, nome: str) -> Optional[Mercado]:
        return next(
            (mercado for mercado in self.__mercados if mercado.nome == nome), None
        )

    def cadastrar_mercado(self, mercado: Mercado) -> None:
        if not self.obter_mercado(mercado.nome):
            self.__mercados.append(mercado)

    def remover_mercado(self, mercado: Mercado) -> None:
        if self.obter_mercado(mercado.nome):
            self.__mercados.remove(mercado)

    def obter_data_ultima_compra(self) -> date:
        return max(compra.data_compra for compra in self.__compras_realizadas)

    def obter_valor_compra_mais_cara(
        self, mercado: Mercado | None = None
    ) -> Decimal | None:
        if not self.__compras_realizadas:
            return None

        if mercado:
            return max(
                (
                    compra.valor_total
                    for compra in self.__compras_realizadas
                    if compra.mercado == mercado
                ),
                default=None,
            )

        return max(
            (compra.valor_total for compra in self.__compras_realizadas), default=None
        )

    def indicar_mercado_compra(self, lista_compras: "ListaCompras") -> Mercado:
        """
        considerar compras realizadas no mercado
        menor valor médio das compras por mercado
        """

        compras_por_mercado = {}
        for compra in self.__compras_realizadas:
            if compra.lista_compras_base == lista_compras:
                if not compras_por_mercado[compra.mercado]:
                    compras_por_mercado[compra.mercado] = []

                compras_por_mercado[compra.mercado].append(compra)

        minimo_valor_compra = None
        mercado_minimo_valor = None

        for mercado, compras in compras_por_mercado.items():
            valor_medio = sum(compra.valor_total for compra in compras) / len(compras)
            if not minimo_valor_compra or valor_medio < minimo_valor_compra:
                minimo_valor_compra = valor_medio
                mercado_minimo_valor = mercado

        return mercado_minimo_valor

    def indicar_mercado_comprar_item(self, item: Item) -> Mercado:
        historico_compra_itens = []
        for compra in self.__compras_realizadas:
            itens_compra = compra.obter_itens_comprados()
            historico_compra_itens += [
                item_comprado
                for item_comprado in itens_compra
                if item_comprado.item == item
            ]

        item_mais_barato = None

        for compra_item in historico_compra_itens:
            if not item_mais_barato or compra_item.preco < item_mais_barato.preco:
                item_mais_barato = compra_item

        return item_mais_barato.mercado
