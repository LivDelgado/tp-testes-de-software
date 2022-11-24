from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.usuario.usuario import Usuario
from app.usuario.usuario_service import UsuarioService


class TestUsuarioService(TestCase):
    def setUp(self) -> None:
        self.usuario_service = UsuarioService()
        return super().setUp()

    def tearDown(self) -> None:
        patch.stopall()
        return super().tearDown()

    @patch("os.path.exists", return_value=True)
    @patch("os.remove")
    def test_limpar_dados_WHEN_arquivo_existe_THEN_remove_arquivo(self, remove_mock, _):
        self.usuario_service.limpar_dados()

        remove_mock.assert_called_once()

    @patch("os.path.exists", return_value=False)
    @patch("os.remove")
    def test_limpar_dados_WHEN_arquivo_nao_existe_THEN_nao_remove_arquivo(
        self, remove_mock, _
    ):
        self.usuario_service.limpar_dados()

        remove_mock.assert_not_called()

    @patch("pickle.load", return_value=Usuario())
    @patch("builtins.open")
    def test_obter_usuario_ou_criar_default_WHEN_dados_salvos_THEN_obtem_dados_salvos(
        self, _, load
    ):
        usuario = self.usuario_service.obter_usuario_salvo_ou_criar_default()

        load.assert_called_once()
        self.assertIsNotNone(usuario)

    @patch("pickle.load")
    @patch("builtins.open", side_effect=Exception())
    def test_obter_usuario_ou_criar_default_WHEN_dados_nao_salvos_THEN_cria_usuario(
        self, open_mock, load
    ):
        usuario = self.usuario_service.obter_usuario_salvo_ou_criar_default()

        load.assert_not_called()
        self.assertIsNotNone(usuario)
