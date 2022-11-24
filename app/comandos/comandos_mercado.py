import typer

from app.mercado.mercado_service import MercadoService
from app.usuario.usuario_service import UsuarioService

mercados_app = typer.Typer()


@mercados_app.command("listar")
def listar_mercados():
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    mercados = MercadoService.listar_mercados(usuario)
    for mercado in mercados:
        print(mercado)


@mercados_app.command("adicionar")
def adicionar_mercado(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    MercadoService.adicionar_mercado(usuario, nome)
    UsuarioService.salvar_dados_usuario(usuario)


@mercados_app.command("remover")
def remover_mercado(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    MercadoService.remover_mercado(usuario, nome)
    UsuarioService.salvar_dados_usuario(usuario)
