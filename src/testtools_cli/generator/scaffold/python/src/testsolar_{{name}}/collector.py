import time
from typing import Optional, BinaryIO

from loguru import logger
from testsolar_testtool_sdk.model.load import LoadResult, LoadError
from testsolar_testtool_sdk.model.param import EntryParam
from testsolar_testtool_sdk.model.test import TestCase
from testsolar_testtool_sdk.reporter import Reporter


def collect_testcases(
    entry_param: EntryParam, pipe_io: Optional[BinaryIO] = None
) -> None:
    logger.info(f"loading testcase from workdir [{entry_param.ProjectPath}]")
    load_result: LoadResult = LoadResult(
        Tests=[],
        LoadErrors=[],
    )

    time.sleep(1)

    load_result.Tests.append(TestCase(Name="a/b/c?d"))
    load_result.LoadErrors.append(
        LoadError(name="load xxx.py failed", message="backtrace here")
    )

    reporter = Reporter(pipe_io=pipe_io)
    reporter.report_load_result(load_result)
