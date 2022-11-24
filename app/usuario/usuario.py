from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from operator import attrgetter
from typing import Dict, List, Optional

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
        if mercado:
            return self.__obter_valor_compra_mais_cara_do_mercado(mercado)

    def __obter_valor_compra_mais_cara_do_mercado(self, mercado: Mercado) -> Decimal:
        return max(
            (
                compra.valor_total
                for compra in self.__compras_realizadas
                if compra.mercado == mercado
            ),
            default=None,
        )

    def indicar_mercado_compra(self, lista_compras: "ListaCompras") -> Mercado:
        """
        considerar compras realizadas no mercado
        menor valor médio das compras por mercado
        """

        compras_por_mercado = (
            self.__agrupar_compras_realizadas_por_mercado_com_lista_base(lista_compras)
        )

        mercado_minimo_valor = self.__obter_mercado_com_menor_valor_medio_de_compras(
            compras_por_mercado
        )

        if not mercado_minimo_valor and self.__mercados:
            mercado_minimo_valor = self.__mercados[0]

        return mercado_minimo_valor

    def __obter_mercado_com_menor_valor_medio_de_compras(
        self, compras_por_mercado: Dict
    ) -> Mercado:
        minimo_valor_compra = None
        mercado_minimo_valor = None

        for mercado, compras in compras_por_mercado.items():
            valor_medio = sum(compra.valor_total for compra in compras) / len(compras)

            mercado_mais_em_conta = not minimo_valor_compra or (
                valor_medio < minimo_valor_compra
            )

            if mercado_mais_em_conta:
                minimo_valor_compra = valor_medio
                mercado_minimo_valor = mercado

        return mercado_minimo_valor

    def __agrupar_compras_realizadas_por_mercado_com_lista_base(
        self, lista_compras: "ListaCompras"
    ) -> Dict:
        compras_por_mercado = {}

        for compra in self.__compras_realizadas:
            if compra.lista_compras_base == lista_compras:
                compras_por_mercado.setdefault(compra.mercado, []).append(compra)

        return compras_por_mercado

    def __agrupar_compras_realizadas_por_mercado(self) -> Dict:
        compras_por_mercado = {}

        for compra in self.__compras_realizadas:
            compras_por_mercado.setdefault(compra.mercado, []).append(compra)

        return compras_por_mercado

    def indicar_mercado_comprar_item(self, item: Item) -> Optional[Mercado]:
        if not self.__mercados and not self.__compras_realizadas:
            return None

        historico_compra_item = self.__listar_compras_que_incluiam_item(item)

        mercado = None

        if historico_compra_item:
            item_mais_barato = min(
                historico_compra_item, key=attrgetter("preco"), default=None
            )
            mercado = item_mais_barato.mercado

        else:
            preco_medio_por_mercado = self.__obter_preco_medio_por_mercado()

            mercado = min(
                preco_medio_por_mercado, key=preco_medio_por_mercado.get, default=None
            )

        return mercado

    def __obter_preco_medio_por_mercado(self) -> Dict:
        compras_por_mercado = self.__agrupar_compras_realizadas_por_mercado()

        preco_medio_por_mercado = {}

        for mercado, compras in compras_por_mercado.items():
            total_de_itens_comprados = sum(
                len(compra.obter_itens_comprados()) for compra in compras
            )
            valor_total_das_compras = sum(compra.valor_total for compra in compras)
            preco_medio_por_mercado[mercado] = (
                valor_total_das_compras / total_de_itens_comprados
            )
        return preco_medio_por_mercado

    def __listar_compras_que_incluiam_item(self, item: Item) -> List[Compra]:
        historico_compra_item = []

        for compra in self.__compras_realizadas:
            itens_compra = compra.obter_itens_comprados()
            historico_compra_item += [
                item_comprado
                for item_comprado in itens_compra
                if item_comprado.item == item
            ]

        return historico_compra_item
