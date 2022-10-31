from unittest import TestCase

from app.lista.lista_compras import ListaCompras
from app.lista.lista_service import ListaService
from app.usuario.usuario import Usuario


# TODO - adicionar restante dos testes
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
