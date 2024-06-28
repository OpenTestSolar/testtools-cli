from typing import Optional

import typer
from rich.traceback import install
from typing_extensions import Annotated

from .generator.scaffold_generator import ScaffoldGenerator, LangType

install(show_locals=True)

app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def init(
    workdir: Annotated[
        Optional[str],
        typer.Argument(
            help="Where you want the scaffolding code to be stored, defaulting to the current directory"
        ),
    ] = None,
) -> None:
    """
    **Init** a testsolar testtool with guide

    Current supported languages:

    - python

    - golang

    - javascript

    - java
    """
    tool_name = typer.prompt("Name of the test tool?")
    pre_langs = "/".join([e.value for e in LangType])
    lang = LangType(
        typer.prompt(f"The language you want to use for development({pre_langs})?")
    )

    gen = ScaffoldGenerator(lang=lang, testtool_name=tool_name, workdir=workdir)
    gen.generate()


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
