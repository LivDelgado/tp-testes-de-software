import typer

from usuario.usuario import Usuario

app = typer.Typer()

lista_app = typer.Typer()
compras_app = typer.Typer()

app.add_typer(lista_app, name="listas")
app.add_typer(compras_app, name="compras")


usuario = None

@lista_app.command("listar")
def listas_listas_de_compras():
    for lista in usuario.obter_listas():
        print(lista.nome, lista.descricao, ' - ')

if __name__ == "__main__":
    usuario = Usuario()
    app()
