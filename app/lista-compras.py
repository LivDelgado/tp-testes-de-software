import typer

from app.comandos import compras_app, lista_app, mercados_app
from app.usuario.usuario_service import UsuarioService

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
