from typing import List
from mercado import Mercado


class MercadoService:
    @staticmethod
    def listar_mercados(usuario: "Usuario") -> List[Mercado]:
        mercados = usuario.listar_mercados()
        if not mercados:
            raise ValueError("Não foi cadastrado nenhum mercado")

        return mercados

    @staticmethod
    def adicionar_mercado(usuario: "Usuario", nome_mercado: str) -> None:
        mercado = Mercado(nome_mercado)
        usuario.cadastrar_mercado(mercado)

    @staticmethod
    def remover_mercado(usuario: "Usuario", nome_mercado: str) -> None:
        mercado = usuario.obter_mercado(nome_mercado)
        if not mercado:
            raise ValueError("Mercado não encontrado")

        usuario.remover_mercado(mercado)
