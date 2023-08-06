# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
from typing import Union, List, Optional, Tuple, Dict, Any

from pytesting_utils import Preconditions


class AbstractRunner(metaclass=ABCMeta):
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        Preconditions.check_argument(
            len(project_name) > 0, "Project name must not be empty!"
        )
        Preconditions.check_argument(len(path) > 0, "Path must not be empty!")
        self._project_name = project_name
        self._path = path

    @abstractmethod
    def run(self) -> Optional[Tuple[str, str]]:
        pass  # pragma: no cover

    @abstractmethod
    def get_total_result(self, log: str) -> Optional[Tuple[int, int, str]]:
        pass  # pragma: no cover

    @abstractmethod
    def get_summary_result(self, log: str) -> Optional[Dict[str, Any]]:
        pass  # pragma: no cover

    def _extract_necessary_packages(self) -> List[str]:
        packages = []
        file_names = [
            "requirements.txt",
            "dev-requirements.txt",
            "dev_requirements.txt",
            "test-requirements.txt",
            "test_requirements.txt",
            "requirements-dev.txt",
            "requirements_dev.txt",
            "requirements-test.txt",
            "requirements_test.txt",
        ]
        for file_name in file_names:
            packages.extend(
                self._extract_packages(os.path.join(self._path, file_name))
            )
        return packages

    @staticmethod
    def _extract_packages(requirements_file):
        packages = []
        if os.path.exists(requirements_file) and os.path.isfile(
            requirements_file
        ):
            with open(requirements_file) as f:
                for line in f.readlines():
                    if "requirements" in line:
                        continue
                    packages.append(line.strip())
        return packages
