import os
from pathlib import Path
from loguru import logger


class PythonGenerator:
    """
    生成Python程序所需要的脚手架代码
    """

    def __init__(self, tool_name: str, workdir: Path | None = None):
        self.tool_name = tool_name
        self.workdir = workdir or Path.cwd()

    def generate_scaffold(self) -> None:
        scaffold_dir = Path(__file__).parent.joinpath("scaffold")

        for dirpath, dirnames, filenames in os.walk(scaffold_dir):
            logger.info(f"dirpath: {dirpath}")
            logger.info(f"dirnames: {dirnames}")
            logger.info(f"filenames: {filenames}")
