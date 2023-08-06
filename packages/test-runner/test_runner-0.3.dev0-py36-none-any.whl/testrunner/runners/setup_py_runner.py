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
from typing import Union, Optional, Tuple, Dict, Any

from pytesting_utils import virtualenv

from testrunner.runners.abstract_runner import AbstractRunner


class SetupPyRunner(AbstractRunner):
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        super().__init__(project_name, path)

    def run(self) -> Optional[Tuple[str, str]]:
        setup_py = os.path.join(self._path, "setup.py")
        if not os.path.exists(setup_py) and not os.path.isfile(setup_py):
            return None

        with virtualenv(self._project_name) as env:
            old_dir = os.getcwd()
            os.chdir(self._path)
            packages = self._extract_necessary_packages()
            env.add_packages_for_installation(packages)
            out, err = env.run_commands(["python setup.py test"])
            os.chdir(old_dir)
            return out, err

    def get_total_result(self, log: str) -> Optional[Tuple[int, int, str]]:
        raise NotImplementedError("Implement me!")

    def get_summary_result(self, log: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("Implement me!")
