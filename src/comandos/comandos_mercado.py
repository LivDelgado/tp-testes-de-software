import typer

from mercado import MercadoService
from usuario import UsuarioService

mercados_app = typer.Typer()

usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()


@mercados_app.command("listar")
def listar_mercados():
    mercados = MercadoService.listar_mercados(usuario)
    for mercado in mercados:
        print(mercado)


@mercados_app.command("adicionar")
def adicionar_mercado(nome: str):
    MercadoService.adicionar_mercado(usuario, nome)
    UsuarioService.salvar_dados_usuario(usuario)


@mercados_app.command("remover")
def remover_mercado(nome: str):
    MercadoService.remover_mercado(usuario, nome)
    UsuarioService.salvar_dados_usuario(usuario)
