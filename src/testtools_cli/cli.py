import typer
from rich.traceback import install
from typing_extensions import Annotated

install(show_locals=True)

app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def init(
    lang: Annotated[
        str,
        typer.Argument(help="TestTool language you want to use"),
    ],
) -> None:
    """
    **Init** a testsolar testtool

    Current supported languages:

    - python

    - golang

    - javascript

    - java
    """
    print("init a testsolar testtool")


@app.command()
def check() -> None:
    """
    **Check** if the testing tools are effective

    - Check the validity of the testing tool metadata

    - Check the validity of the testing tool scripts
    """


def cli_entry() -> None:
    app()


if __name__ == "__main__":
    app()
