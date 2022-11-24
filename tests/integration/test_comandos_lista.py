from unittest import TestCase

from typer.testing import CliRunner

from lista_compras import app


class TestComandosLista(TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.runner.invoke(app, ["limpar"])

    def tearDown(self):
        self.runner.invoke(app, ["limpar"])

    def test_adicionar_listas_de_compras_WHEN_nenhuma_lista_THEN_retorna_erro_nenhuma_lista(
        self,
    ):
        result = self.runner.invoke(app, ["listas", "listar"])

        self.assertEqual("Nenhuma lista encontrada", str(result.exception))

    def test_adicionar_listas_de_compras_WHEN_adiciona_lista_THEN_retorna_lista_ao_obter_todas(
        self,
    ):
        result = self.runner.invoke(
            app, ["listas", "adicionar", "listaTeste"], input="Cafe\nN\n"
        )

        result = self.runner.invoke(app, ["listas", "listar"])

        self.assertTrue("listaTeste" in result.stdout)

    def test_remover_listas_de_compras_WHEN_lista_inexistente_THEN_retorna_erro_lista_inexistente(
        self,
    ):
        result = self.runner.invoke(app, ["listas", "remover", "teste"])

        self.assertEqual("Essa lista não existe", str(result.exception))

    def test_remover_listas_de_compras_WHEN_lista_existente_THEN_remove_lista(self):
        result = self.runner.invoke(
            app, ["listas", "adicionar", "teste"], input="Cafe\nN\n"
        )
        result = self.runner.invoke(app, ["listas", "listar"])
        self.assertTrue("teste" in result.stdout)

        result = self.runner.invoke(app, ["listas", "remover", "teste"])

        result = self.runner.invoke(app, ["listas", "listar"])
        self.assertFalse("teste" in result.stdout)

    def test_ver_itens_lista_WHEN_lista_inexistente_THEN_retorna_mensagem_lista_inexistente(
        self,
    ):
        result = self.runner.invoke(
            app, ["listas", "itens", "listar", "itensListaTeste"]
        )

        self.assertEqual("Essa lista não existe", str(result.exception))

    def test_ver_itens_lista_WHEN_lista_existente_THEN_retorna_itens_lista(self):
        result = self.runner.invoke(
            app, ["listas", "adicionar", "itensListaTeste"], input="Cafe\ny\nLeite\nN\n"
        )

        result = self.runner.invoke(
            app, ["listas", "itens", "listar", "itensListaTeste"]
        )
        print(result)

        self.assertTrue("Cafe" in result.stdout)
        self.assertTrue("Leite" in result.stdout)

    def test_adicionar_item_lista_WHEN_lista_nao_existe_THEN_retorna_mensagem_lista_inexistente(
        self,
    ):
        result = self.runner.invoke(
            app, ["listas", "itens", "adicionar", "itensListaTeste"], input="Cafe\n"
        )

        self.assertEqual("Essa lista não existe", str(result.exception))

    def test_adicionar_item_lista_WHEN_lista_existe_THEN_adiciona_item(self):
        result = self.runner.invoke(
            app, ["listas", "adicionar", "itensListaTeste"], input="Cafe\ny\nLeite\nN\n"
        )
        result = self.runner.invoke(
            app, ["listas", "itens", "adicionar", "itensListaTeste"], input="Arroz\n"
        )

        self.assertEqual(0, result.exit_code)

        result = self.runner.invoke(
            app, ["listas", "itens", "listar", "itensListaTeste"]
        )
        self.assertTrue("Arroz" in result.stdout)
