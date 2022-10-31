from datetime import datetime
from decimal import Decimal
from typing import Dict, List

import typer
from rich.prompt import Prompt

from app.usuario.usuario_service import UsuarioService
from app.compra_realizada.compras_service import ComprasService
from app.lista.lista_service import ListaService


compras_app = typer.Typer()

usuario = UsuarioService.obter_usuario_salvo_ou_criar_default()


@compras_app.command("listar")
def listar_historico_compras():
    compras = ComprasService.obter_historico_compras(usuario)
    for compra in compras:
        print(compra)


@compras_app.command("adicionar")
def adicionar_compra():
    mercado = Prompt.ask("Em qual mercado você comprou?")
    data_compra_str = Prompt.ask("Quando foi a compra? dd-MM-YYYY")
    data_compra = datetime.strptime(data_compra_str, "%d-%m-%Y").date()
    valor_total_str = Prompt.ask("Qual foi o valor da compra?")
    valor_total = Decimal(valor_total_str)

    lista_base = Prompt.ask("Qual lista foi usada?")
    itens_lista = ListaService.listar_itens(usuario, lista_base)

    itens: List[Dict] = []

    for item in itens_lista:
        adicionar_item = typer.confirm(f"O item {item} foi comprado?")
        if adicionar_item:
            quantidade_item = Prompt.ask("Quantos você comprou?")
            valor_item = Prompt.ask("Quanto foi cada item?")
            item_lista_comprado = {"preco": valor_item, "quantidade": quantidade_item, "nome": item.nome}

            itens.append(item_lista_comprado)

    pedir_item = typer.confirm(f"Você comprou algum item fora da lista {lista_base}?")
    while pedir_item:
        nome_item = Prompt.ask("Qual item quer adicionar?")
        quantidade_item = Prompt.ask("Quantos você comprou?")
        valor_item = Prompt.ask("Quanto foi cada item?")

        item = {"preco": valor_item, "quantidade": quantidade_item, "nome": nome_item}
        itens.append(item)

        pedir_item = typer.confirm("Adicionar outro?")

    ComprasService.adicionar_compra(
        usuario=usuario,
        data_compra=data_compra,
        nome_mercado=mercado,
        nome_lista_base=lista_base,
        valor_total=valor_total,
        itens=itens,
    )

    UsuarioService.salvar_dados_usuario(usuario)


@compras_app.command("remover")
def remover_compra():
    mercado = Prompt.ask("Em qual mercado você comprou?")
    data_compra_str = Prompt.ask("Quando foi a compra? dd-MM-YYYY")
    data_compra = datetime.strptime(data_compra_str, "%d-%m-%Y").date()

    ComprasService.remover_compra(usuario, data_compra, mercado)
    UsuarioService.salvar_dados_usuario(usuario)


@compras_app.command("itens")
def listar_itens_compra():
    mercado = Prompt.ask("Em qual mercado você comprou?")
    data_compra_str = Prompt.ask("Quando foi a compra? dd-MM-YYYY")
    data_compra = datetime.strptime(data_compra_str, "%d-%m-%Y").date()

    itens = ComprasService.listar_itens_compra(usuario, data_compra, mercado)
    for item in itens:
        print(item)


@compras_app.command("pago-extra")
def obter_valor_extra():
    mercado = Prompt.ask("Em qual mercado você comprou?")
    data_compra_str = Prompt.ask("Quando foi a compra? dd-MM-YYYY")
    data_compra = datetime.strptime(data_compra_str, "%d-%m-%Y").date()

    valor_extra = ComprasService.obter_valor_extra(usuario, data_compra, mercado)
    print(valor_extra)
