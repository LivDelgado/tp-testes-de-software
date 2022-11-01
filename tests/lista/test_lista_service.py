from unittest import TestCase

from app.lista.lista_compras import ListaCompras
from app.lista.lista_service import ListaService
from app.usuario.usuario import Usuario


class TestListaService(TestCase):
    def setUp(self) -> None:
        self.usuario = Usuario()
        self.lista_service = ListaService()
        return super().setUp()

    def test_obter_listas_WHEN_nenhuma_lista_cadastrada_THEN_raise_error(self):
        with self.assertRaises(ValueError):
            self.lista_service.obter_listas(self.usuario)

    def test_obter_listas_WHEN_lista_cadastrada_THEN_retorna_listas(self):
        self.usuario.adicionar_lista(ListaCompras(nome="teste", descricao="teste"))

        listas = self.lista_service.obter_listas(self.usuario)

        self.assertEqual(1, len(listas))

    def test_adicionar_lista_WHEN_lista_sem_itens_THEN_salva_lista_sem_itens(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=[]
        )

        itens = self.lista_service.listar_itens(self.usuario, nome_lista)

        self.assertEqual([], itens)

    def test_adicionar_lista_WHEN_lista_com_itens_THEN_salva_lista_com_itens(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=["item1", "item2"]
        )

        itens = self.lista_service.listar_itens(self.usuario, nome_lista)

        self.assertEqual(2, len(itens))

    def test_adicionar_lista_WHEN_adiciona_lista_THEN_salva_nova_lista_para_usuario(
        self,
    ):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=["item1", "item2"]
        )

        self.assertEqual(1, len(self.usuario.obter_listas()))

    def test_remover_lista_WHEN_lista_nao_existe_THEN_retorna_erro(self):
        with self.assertRaises(ValueError):
            self.lista_service.remover_lista(self.usuario, "inexistente")

    def test_remover_lista_WHEN_lista_existe_THEN_remove_lista(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=["item1", "item2"]
        )

        self.lista_service.remover_lista(self.usuario, nome_lista)

        self.assertEqual([], self.usuario.obter_listas())

    def test_listar_itens_WHEN_lista_nao_existe_THEN_raise_erro(self):
        with self.assertRaises(ValueError):
            self.lista_service.listar_itens(self.usuario, "lista")

    def test_listar_itens_WHEN_lista_xiste_THEN_retorna_itens(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=["item1"]
        )

        itens = self.lista_service.listar_itens(self.usuario, nome_lista)

        self.assertEqual(1, len(itens))

    def test_adicionar_item_lista_WHEN_lista_nao_existe_THEN_raise_erro(self):
        with self.assertRaises(ValueError):
            self.lista_service.adicionar_item_lista(self.usuario, "lista", "item")

    def test_adicionar_item_lista_WHEN_lista_existe_THEN_adiciona_item(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=[]
        )

        self.lista_service.adicionar_item_lista(self.usuario, nome_lista, "item")

        self.assertEqual(
            1, len(self.lista_service.listar_itens(self.usuario, nome_lista))
        )

    def test_remover_item_lista_WHEN_lista_nao_existe_THEN_raise_erro(self):
        with self.assertRaises(ValueError):
            self.lista_service.remover_item_lista(self.usuario, "lista", "item")

    def test_remover_item_lista_WHEN_lista_existe_e_item_existe_THEN_remove_item(self):
        nome_lista = "lista"
        self.lista_service.adicionar_lista(
            self.usuario, nome_lista, "descricao", itens=[]
        )
        self.lista_service.adicionar_item_lista(self.usuario, nome_lista, "item")

        self.lista_service.remover_item_lista(self.usuario, "lista", "item")

        self.assertEqual([], self.lista_service.listar_itens(self.usuario, nome_lista))
