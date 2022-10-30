import typer
from comandos import lista_app, compras_app, mercados_app

from usuario import UsuarioService

app = typer.Typer()

app.add_typer(lista_app, name="listas")
app.add_typer(compras_app, name="compras")
app.add_typer(mercados_app, name="mercados")


@app.command("limpar")
def limpar_dados():
    UsuarioService.limpar_dados()


if __name__ == "__main__":
    try:
        app()
    except Exception as error:
        print(error)
