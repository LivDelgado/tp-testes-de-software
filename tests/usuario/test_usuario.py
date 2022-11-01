from datetime import date
from decimal import Decimal
from typing import Optional
from unittest import TestCase

from app.compra_realizada.compra import Compra
from app.item.item import Item
from app.item.item_comprado import ItemComprado
from app.lista.lista_compras import ListaCompras
from app.mercado.mercado import Mercado
from app.usuario.usuario import Usuario


class TestUsuario(TestCase):
    def test_obter_lista_WHEN_lista_existente_RETURN_lista(self):
        usuario = Usuario()
        lista = ListaCompras(nome="Teste", descricao="Lista")
        usuario.adicionar_lista(lista)

        lista_retorno = usuario.obter_lista(lista.nome)

        self.assertEqual(lista, lista_retorno)

    def test_obter_lista_WHEN_lista_inexistente_RETURN_nulo(self):
        usuario = Usuario()
        lista_retorno = usuario.obter_lista("nome")

        self.assertIsNone(lista_retorno)

    def test_adicionar_lista_WHEN_lista_unica_THEN_adiciona_lista(self):
        usuario = Usuario()
        lista = ListaCompras(nome="Teste", descricao="Lista")

        usuario.adicionar_lista(lista)

        self.assertEqual(1, len(usuario.obter_listas()))

    def test_adicionar_lista_WHEN_lista_duplicada_THEN_raise_erro(self):
        usuario = Usuario()
        lista = ListaCompras(nome="Teste", descricao="Lista")
        usuario.adicionar_lista(lista)

        with self.assertRaises(ValueError):
            usuario.adicionar_lista(lista)

    def test_remover_lista_WHEN_lista_inexistente_THEN_raise_erro(self):
        usuario = Usuario()

        with self.assertRaises(ValueError):
            usuario.remover_lista("nome")

    def test_remover_lista_WHEN_lista_existente_THEN_remove_lista(self):
        usuario = Usuario()
        lista = ListaCompras(nome="Teste", descricao="Lista")
        usuario.adicionar_lista(lista)

        usuario.remover_lista(lista.nome)

        self.assertEqual([], usuario.obter_listas())

    def test_obter_compra_WHEN_compra_inexistente_THEN_retorna_nulo(self):
        usuario = Usuario()

        compra = usuario.obter_compra(date(2022, 10, 31), Mercado("mercado"))

        self.assertIsNone(compra)

    def test_obter_compra_WHEN_compra_existente_THEN_retorna_compra(self):
        usuario = Usuario()
        compra_cadastrada = self.__nova_compra()
        usuario.cadastrar_compra(compra_cadastrada)

        compra = usuario.obter_compra(
            compra_cadastrada.data_compra, compra_cadastrada.mercado
        )

        self.assertIsNotNone(compra)

    def test_obter_valor_compra_mais_cara_WHEN_nenhuma_compra_cadastrada_THEN_retorna_nulo(
        self,
    ):
        usuario = Usuario()

        compra_mais_cara = usuario.obter_valor_compra_mais_cara(Mercado("teste"))

        self.assertIsNone(compra_mais_cara)

    def test_obter_valor_compra_mais_cara_WHEN_multiplas_compras_no_mesmo_mercado_THEN_retorna_valor(
        self,
    ):
        usuario = Usuario()
        compra_um = self.__nova_compra()
        compra_dois = self.__nova_compra()
        compra_dois.data_compra = date(2022, 10, 1)
        compra_dois.valor_total = compra_um.valor_total + 1000
        usuario.cadastrar_compra(compra_um)
        usuario.cadastrar_compra(compra_dois)

        compra_mais_cara = usuario.obter_valor_compra_mais_cara(compra_um.mercado)

        self.assertEqual(compra_dois.valor_total, compra_mais_cara)

    def test_obter_valor_compra_mais_cara_WHEN_nenhuma_compra_no_mercado_THEN_retorna_nulo(
        self,
    ):
        usuario = Usuario()
        compra_um = self.__nova_compra()
        usuario.cadastrar_compra(compra_um)

        compra_mais_cara = usuario.obter_valor_compra_mais_cara(
            Mercado("mercado diferente")
        )

        self.assertIsNone(compra_mais_cara)

    def test_indicar_mercado_compra_WHEN_nenhum_mercado_e_nenhuma_compra_THEN_retorna_nulo(
        self,
    ):
        usuario = Usuario()
        lista_compras = self.__nova_lista_de_compras()

        resultado = usuario.indicar_mercado_compra(lista_compras)

        self.assertIsNone(resultado)

    def test_indicar_mercado_compra_WHEN_nenhuma_compra_THEN_retorna_nulo(self):
        usuario = Usuario()
        lista_compras = self.__nova_lista_de_compras()

        resultado = usuario.indicar_mercado_compra(lista_compras)

        self.assertIsNone(resultado)

    def test_indicar_mercado_compra_WHEN_nenhuma_com_a_lista_mas_mercado_cadastrado_THEN_retorna_qualquer_mercado(
        self,
    ):
        usuario = Usuario()
        usuario.cadastrar_mercado(Mercado("novo"))
        usuario.cadastrar_compra(self.__nova_compra())
        lista_compras = self.__nova_lista_de_compras()
        lista_compras.nome = "lista teste nenhuma com a lista"

        resultado = usuario.indicar_mercado_compra(lista_compras)

        self.assertIsNotNone(resultado)

    def test_indicar_mercado_compra_WHEN_compra_em_varios_mercados_THEN_retorna_mais_barato(
        self,
    ):
        usuario = Usuario()
        compra_mais_barata = self.__nova_compra(
            valor=Decimal(500), nome_mercado="mercado_mais_barato"
        )
        usuario.cadastrar_compra(compra_mais_barata)
        usuario.cadastrar_compra(
            self.__nova_compra(valor=Decimal(1500), nome_mercado="mercado_mais_barato")
        )
        compra_mais_cara = self.__nova_compra(
            valor=Decimal(1500), nome_mercado="mercado_mais_caro"
        )
        usuario.cadastrar_compra(compra_mais_cara)

        resultado = usuario.indicar_mercado_compra(
            compra_mais_barata.lista_compras_base
        )

        self.assertEqual(compra_mais_barata.mercado, resultado)

    def test_indicar_mercado_comprar_item_WHEN_nenhuma_compra_RETURN_nulo(self):
        usuario = Usuario()

        resultado = usuario.indicar_mercado_comprar_item(Item("item"))

        self.assertIsNone(resultado)

    def test_indicar_mercado_comprar_item_WHEN_nenhuma_compra_com_item_mas_historico_RETURN_mercado_com_preco_medio_mais_barato(
        self,
    ):
        usuario = Usuario()
        usuario.cadastrar_compra(
            self.__nova_compra(valor=Decimal(200), nome_mercado="mais_barato")
        )
        usuario.cadastrar_compra(
            self.__nova_compra(valor=Decimal(300), nome_mercado="mais_caro")
        )

        resultado = usuario.indicar_mercado_comprar_item(Item("item_diferenciado"))

        self.assertEqual("mais_barato", resultado.nome)

    def test_indicar_mercado_comprar_item_WHEN_alguma_compra_com_item_mas_historico_RETURN_mercado_com_menor_preco_do_item(
        self,
    ):
        usuario = Usuario()
        usuario.cadastrar_compra(
            self.__nova_compra(valor=Decimal(200), nome_mercado="mais_barato")
        )
        usuario.cadastrar_compra(
            self.__nova_compra(valor=Decimal(300), nome_mercado="mais_caro")
        )

        resultado = usuario.indicar_mercado_comprar_item(Item("item"))

        self.assertEqual("mais_barato", resultado.nome)

    def __nova_lista_de_compras(self) -> ListaCompras:
        lista_compras = ListaCompras("nome", "descricao")
        item = Item("item")
        lista_compras.adicionar_item(item)
        item = Item("item2")
        lista_compras.adicionar_item(item)
        return lista_compras

    def __nova_compra(
        self,
        valor: Optional[Decimal] = Decimal(300),
        nome_mercado: Optional[str] = "mercado",
    ) -> Compra:
        data = date(2022, 10, 31)
        mercado = Mercado(nome_mercado)
        lista = self.__nova_lista_de_compras()
        compra_cadastrada = Compra(
            data_compra=data,
            mercado=mercado,
            lista_compras_base=lista,
            valor_total=valor,
        )

        for item in lista.obter_itens():
            compra_cadastrada.adicionar_item_comprado(
                ItemComprado(
                    item=item,
                    data_compra=data,
                    mercado=mercado,
                    preco=Decimal(20),
                    quantidade=2,
                )
            )

        return compra_cadastrada
