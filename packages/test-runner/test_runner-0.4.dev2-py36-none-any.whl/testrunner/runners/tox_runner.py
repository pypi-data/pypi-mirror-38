# -*- coding: utf-8 -*-
import os
from typing import Union, Optional, Tuple, Dict, Any

from testrunner.runners.abstract_runner import AbstractRunner


class ToxRunner(AbstractRunner):
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        super().__init__(project_name, path)  # pragma: no cover

    def run(self) -> Optional[Tuple[str, str]]:
        pass  # pragma: no cover

    def get_total_result(self, log: str) -> Optional[Tuple[int, int, str]]:
        pass  # pragma: no cover

    def get_summary_result(self, log: str) -> Optional[Dict[str, Any]]:
        pass  # pragma: no cover
