from typing import List, Optional

import typer
from rich.prompt import Prompt

from app.lista.lista_service import ListaService
from app.usuario.usuario_service import UsuarioService

lista_app = typer.Typer()
itens_app = typer.Typer()
lista_app.add_typer(itens_app, name="itens")


@lista_app.command("listar")
def listar_listas_de_compras():
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    listas = ListaService.obter_listas(usuario)
    for lista in listas:
        print(lista)


@lista_app.command("adicionar")
def adicionar_lista_de_compras(nome: str, descricao: Optional[str] = None):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    pedir_item = True
    itens: List[str] = []
    while pedir_item:
        nome_item = Prompt.ask("Qual item quer adicionar?")
        itens.append(nome_item)
        pedir_item = typer.confirm("Adicionar outro?")

    ListaService.adicionar_lista(usuario, nome, descricao, itens)
    UsuarioService.salvar_dados_usuario(usuario)


@lista_app.command("remover")
def remover_lista_de_compras(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    ListaService.remover_lista(usuario, nome)
    UsuarioService.salvar_dados_usuario(usuario)


@itens_app.command("listar")
def ver_itens_lista(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    itens = ListaService.listar_itens(usuario, nome)
    for item in itens:
        print(item)


@itens_app.command("adicionar")
def adicionar_item_lista(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    nome_item = Prompt.ask("Qual item quer adicionar?")
    ListaService.adicionar_item_lista(usuario, nome, nome_item)
    UsuarioService.salvar_dados_usuario(usuario)


@itens_app.command("remover")
def remover_item_lista(nome: str):
    usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()
    nome_item = Prompt.ask("Qual item quer remover?")
    ListaService.remover_item_lista(usuario, nome, nome_item)
    UsuarioService.salvar_dados_usuario(usuario)
