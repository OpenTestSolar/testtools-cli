import os
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jinja2.nativetypes import NativeEnvironment
from loguru import logger


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
        self.native_env = NativeEnvironment()

    def generate(self) -> None:
        if self.lang == LangType.Python:
            self.generate_scaffold(language_name=LangType.Python.value)

    def generate_scaffold(self, language_name: str) -> None:
        scaffold_dir = Path(__file__).parent / "scaffold" / language_name
        env = Environment(loader=FileSystemLoader(scaffold_dir))

        for dirpath, dirnames, filenames in os.walk(scaffold_dir):

            # 计算模板文件的相对目录
            relative_dir = os.path.relpath(dirpath, scaffold_dir)

            # dirnames是目录，不用管
            # 仅处理当前目录下的filenames即可
            for filename in filenames:
                relative_file = Path(relative_dir) / filename

                path_template = self.native_env.from_string(str(relative_file))
                dest_path = Path(self.workdir) / path_template.render(name=self.testtool_name)

                Path(dest_path).parent.mkdir(parents=True, exist_ok=True)

                logger.info(f"Generating scaffold file [{dest_path}]")
                with open(dest_path, "w", encoding="utf-8") as file_out:
                    logger.debug(f"  From template file [{relative_file}]")
                    logger.debug(f"  Into dest file [{dest_path}]")
                    template = env.get_template(str(relative_file))
                    content = template.render(name=self.testtool_name)
                    file_out.write(content)
