from unittest import TestCase

from app.item.item import Item
from app.lista.lista_compras import ListaCompras


class TestListaCompras(TestCase):
    def setUp(self) -> None:
        self.lista = ListaCompras(nome="Teste", descricao="Teste")
        return super().setUp()

    def test_adicionar_item_WHEN_item_unico_THEN_salva_item(self):
        item = Item("item1")

        self.lista.adicionar_item(item)

        self.assertEqual(1, len(self.lista.obter_itens()))

    def test_adicionar_item_WHEN_tenta_adicionar_item_repetido_THEN_salva_um_item(self):
        item = Item("item1")

        self.lista.adicionar_item(item)
        self.lista.adicionar_item(item)

        self.assertEqual(1, len(self.lista.obter_itens()))

    def test_remover_item_WHEN_item_nao_existe_THEN_nao_remove(self):
        item = Item("item1")

        self.lista.remover_item(item)

        self.assertEqual([], self.lista.obter_itens())

    def test_remover_item_WHEN_item_existe_THEN_remove_item(self):
        item = Item("item1")
        self.lista.adicionar_item(item)

        self.lista.remover_item(item)

        self.assertEqual([], self.lista.obter_itens())

    def test_obter_itens_WHEN_nenhum_item_adicionado_THEN_retorna_vazio(self):
        self.assertEqual([], self.lista.obter_itens())

    def test_obter_itens_WHEN_item_adicionado_THEN_retorna_todos_os_itens(self):
        item = Item("item1")
        self.lista.adicionar_item(item)
        item = Item("item2")
        self.lista.adicionar_item(item)

        itens = self.lista.obter_itens()

        self.assertEqual(2, len(itens))

    def test_obter_item_WHEN_item_existe_THEN_retorna_item(self):
        item = Item("item1")
        self.lista.adicionar_item(item)

        item_cadastrado = self.lista.obter_item(item)

        self.assertIsNotNone(item_cadastrado)

    def test_obter_item_WHEN_item_nao_existe_THEN_retorna_nulo(self):
        item = Item("item1")

        item_cadastrado = self.lista.obter_item(item)

        self.assertIsNone(item_cadastrado)
