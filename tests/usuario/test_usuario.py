from datetime import date
from decimal import Decimal
from unittest import TestCase

from app.compra_realizada.compra import Compra
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

    def __nova_compra(self) -> Compra:
        data = date(2022, 10, 31)
        mercado = Mercado("nome")
        lista = ListaCompras("a", "b")
        compra_cadastrada = Compra(
            data_compra=data,
            mercado=mercado,
            lista_compras_base=lista,
            valor_total=Decimal(300),
        )

        return compra_cadastrada
