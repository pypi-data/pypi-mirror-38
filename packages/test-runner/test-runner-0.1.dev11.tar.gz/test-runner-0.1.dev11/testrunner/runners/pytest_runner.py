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
import re
from typing import Union, Optional, Tuple

from testrunner.runners.abstract_runner import AbstractRunner
from testrunner.utils.context_managers import virtualenv


class PyTestRunner(AbstractRunner):
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        super().__init__(project_name, path)

    def run(self) -> Optional[Tuple[str, str]]:
        # TODO make sure nothing goes wrong here

        with virtualenv(self._project_name) as env:
            old_dir = os.getcwd()
            os.chdir(self._path)
            packages = self._extract_necessary_packages()
            env.add_packages_for_installation(packages)
            env.add_package_for_installation("pytest")
            env.add_package_for_installation("pytest-cov")
            out, err = env.run_commands(
                [
                    "pytest --cov={} --cov-report=term-missing".format(
                        self._project_name
                    )
                ]
            )
            os.chdir(old_dir)
            return out, err

    def get_total_result(self, log: str) -> Optional[Tuple[int, int, str]]:
        matches = re.search(r"TOTAL\s+([0-9]+)\s+([0-9]+)\s+([0-9]+%)", log)
        if matches:
            statements = int(matches.group(1)) if matches.group(1) else 0
            missing = int(matches.group(2)) if matches.group(2) else 0
            coverage = matches.group(3) if matches.group(3) else "0.0%"
            return statements, missing, coverage
        return None

    def get_summary_result(
        self, log: str
    ) -> Optional[Tuple[int, int, int, float]]:
        matches = re.search(
            r"[=]+ (([0-9]+) failed, )?"
            r"([0-9]+) passed"
            r"(, ([0-9]+) skipped)?"
            r"(, ([0-9]+) warnings)? in ([0-9.]+) seconds",
            log,
        )
        if matches:
            failed = int(matches.group(2)) if matches.group(2) else 0
            passed = int(matches.group(3)) if matches.group(3) else 0
            skipped = int(matches.group(5)) if matches.group(5) else 0
            time = float(matches.group(8)) if matches.group(8) else 0.0
            return failed, passed, skipped, time
        return None
