# -*- coding: utf-8 -*-

# This file is part of test-runner.
#
# test-runner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# test-runner is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with test-runner.  If not, see <https://www.gnu.org/licenses/>.
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
            "test-requirements.txt",
            "requirements-dev.txt",
            "requirements-test.txt",
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
