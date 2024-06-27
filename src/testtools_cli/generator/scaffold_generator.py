import os
from enum import Enum


class LangType(str, Enum):
    Python = "python"
    Golang = "golang"
    Java = "java"
    Javascript = "javascript"


class ScaffoldGenerator:
    def __init__(self, lang: LangType, testtool_name: str, workdir: str | None) -> None:
        self.lang = lang
        self.testtool_name = testtool_name
        self.workdir = workdir or os.getcwd()

    def generate(self) -> None:
        pass
