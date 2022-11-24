from unittest import TestCase

from app.mercado.mercado import Mercado
from app.mercado.mercado_service import MercadoService
from app.usuario.usuario import Usuario


class TestMercadoService(TestCase):
    def setUp(self) -> None:
        self.usuario = Usuario()
        self.mercado_service = MercadoService()
        return super().setUp()

    def test_listar_mercados_WHEN_nenhum_mercado_cadastrado_THEN_raise_error(self):
        with self.assertRaises(ValueError):
            self.mercado_service.listar_mercados(self.usuario)

    def test_listar_mercados_WHEN_mercado_cadastrado_THEN_lista_mercados(self):
        self.usuario.cadastrar_mercado(Mercado("mercado de teste"))

        mercados = self.mercado_service.listar_mercados(self.usuario)

        self.assertEqual(1, len(mercados))

    def test_adicionar_mercado_WHEN_mercado_valido_THEN_cadastra_mercado(self):
        nome_mercado = "mercado"

        self.mercado_service.adicionar_mercado(self.usuario, nome_mercado)

        self.assertIsNotNone(self.usuario.obter_mercado(nome_mercado))

    def test_remover_mercado_WHEN_mercado_cadastrado_THEN_remove_mercado(self):
        mercado = "mercado"
        self.usuario.cadastrar_mercado(Mercado(mercado))

        self.mercado_service.remover_mercado(self.usuario, mercado)

        self.assertEqual([], self.usuario.listar_mercados())

    def test_remover_mercado_WHEN_mercado_nao_encontrado_THEN_raise_erro(self):
        with self.assertRaises(ValueError):
            self.mercado_service.remover_mercado(self.usuario, "nao existe")
