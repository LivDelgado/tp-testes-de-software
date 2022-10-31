import os
import pickle

from app.usuario.usuario import Usuario

FILE_PATH = "./dados-usuario.pkl"


class UsuarioService:
    @staticmethod
    def limpar_dados() -> None:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

    @staticmethod
    def salvar_dados_usuario(usuario: Usuario) -> None:
        arquivo = open(FILE_PATH, "wb")
        pickle.dump(usuario, arquivo, pickle.HIGHEST_PROTOCOL)
        arquivo.close()

    @staticmethod
    def obter_usuario_salvo_ou_criar_default() -> Usuario:
        try:
            arquivo = open(FILE_PATH, "rb")
            usuario = pickle.load(arquivo)
            arquivo.close()
            return usuario
        except Exception as error:
            return Usuario()
