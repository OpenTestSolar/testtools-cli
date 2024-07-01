import logging
import os
from enum import Enum
from pathlib import Path
from pydantic import BaseModel

from jinja2 import Environment, FileSystemLoader
from jinja2.nativetypes import NativeEnvironment

log = logging.getLogger("rich")


class LangType(str, Enum):
    Python = "python"
    Golang = "golang"
    Java = "java"
    Javascript = "javascript"


class LeftToDos(BaseModel):
    file: Path
    line: int
    content: str


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

                log.info(f"Generating scaffold file [{dest_path}]")
                with open(dest_path, "w", encoding="utf-8") as file_out:
                    log.debug(f"  From template file [{relative_file}]")
                    log.debug(f"  Into dest file [{dest_path}]")
                    template = env.get_template(str(relative_file))
                    content = template.render(name=self.testtool_name)
                    file_out.write(content)

        logging.info(f"✅ Generated {language_name} scaffold done.")

        self.show_todos(Path(self.workdir))

    def show_todos(self, workdir: Path) -> None:
        """
        检查文件中的TODO，并输出到控制台提示用户还有多少个需要
        :param workdir: 工具目录
        """
        results: list[LeftToDos] = []
        for dirpath, dirnames, filenames in os.walk(workdir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]

            # 检查filenames里面有没有TODO
            for filename in filenames:
                file_to_check = Path(dirpath) / filename
                results.extend(self.get_todos(file_to_check))

        if results:
            log.warning(f"You still have {len(results)} TODOs.Please fix these todos below:")
            for result in results:
                log.warning(f"  {result.file}:{result.line}:\t\t{result.content}")

    def get_todos(self, file_to_check: Path) -> list[LeftToDos]:
        if file_to_check.name.startswith("."):
            return []

        results: list[LeftToDos] = []
        try:
            content = file_to_check.read_text(encoding="utf-8")
            for i, line_content in enumerate(content.splitlines()):
                if "TODO" in line_content:
                    results.append(LeftToDos(file=file_to_check, line=i + 1, content=line_content))
            return results
        except Exception as e:
            return []
