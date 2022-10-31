from datetime import date
from decimal import Decimal
from unittest import TestCase
from app.item.item import Item

from app.item.item_comprado import ItemComprado
from app.mercado.mercado import Mercado

class TestItemComprado(TestCase):
    def test_valor_total_WHEN_quantidade_igual_a_um_THEN_returns_preco(self):
        item_comprado = ItemComprado(
            item=Item("nome"),
            preco=Decimal(10),
            mercado=Mercado(nome="Teste"),
            data_compra=date(2022, 10, 1)
        )

        valor_total_obtido = item_comprado.valor_total

        self.assertEqual(item_comprado.preco, valor_total_obtido, "O valor obtido deveria ser igual ao preço")

    def test_valor_total_WHEN_quantidade_maior_que_um_THEN_returns_preco_multiplicado(self):
        item_comprado = ItemComprado(
            item=Item("nome"),
            preco=Decimal(10),
            mercado=Mercado(nome="Teste"),
            data_compra=date(2022, 10, 1),
            quantidade=3
        )

        valor_total_obtido = item_comprado.valor_total

        self.assertEqual(30, valor_total_obtido, "Multiplica preço por quantidade")
