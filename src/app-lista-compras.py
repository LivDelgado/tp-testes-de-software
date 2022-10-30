import typer
from rich.prompt import Prompt
from typing import List, Optional

from lista import ListaService

from usuario import Usuario, UsuarioService
from item import Item

app = typer.Typer()

lista_app = typer.Typer()
compras_app = typer.Typer()
mercados_app = typer.Typer()

app.add_typer(lista_app, name="listas")
app.add_typer(compras_app, name="compras")
app.add_typer(mercados_app, name="mercados")

usuario = None

@lista_app.command("listar")
def listas_listas_de_compras():
    ListaService.imprimir_listas(usuario)

@lista_app.command("adicionar")
def adicionar_listas_de_compras(nome: str, descricao: Optional[str]):
    pedir_item = True
    itens: List[str] = []
    while pedir_item:
        nome_item = Prompt.ask("Qual item quer adicionar?")
        itens.append(Item(nome=nome_item))
        pedir_item = typer.confirm("Adicionar outro?")

    ListaService.adicionar_lista(usuario, nome, descricao, itens)
    UsuarioService.salvar_dados_usuario(usuario)

if __name__ == "__main__":
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    app()
