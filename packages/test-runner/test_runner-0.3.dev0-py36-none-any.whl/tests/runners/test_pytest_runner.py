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
import shutil
import tempfile
import unittest
from git import Repo
from typing import List, Tuple
from unittest import mock
from unittest.mock import MagicMock

from testrunner.runners.pytest_runner import PyTestRunner


class VenvMock(MagicMock):
    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)

    def add_packages_for_installation(self, packages: List[str]) -> None:
        pass

    def add_package_for_installation(self, package: str) -> None:
        pass

    def run_commands(self, commands: List[str]) -> Tuple[str, str]:
        return "out", "err"


class PyTestRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self._dummy_dir = tempfile.mkdtemp()
        url = "https://github.com/audreyr/standardjson"
        self._repo = Repo.clone_from(url, self._tmp_dir)
        self._runner = PyTestRunner("standardjson", self._tmp_dir)
        self._dummy_runner = PyTestRunner("test", "test")
        self._output = """
----------- coverage: platform linux, python 3.7.0-final-0 -----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
standardjson/__init__.py            4      0   100%
standardjson/encoder_funcs.py      18      2    89%   8, 10
standardjson/encoders.py           17      3    82%   26-29
-------------------------------------------------------------
TOTAL                              39      5    87%


========================== 13 passed in 0.06 seconds ===========================
        """

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)
        shutil.rmtree(self._dummy_dir)

    def test_run(self):
        out, err = self._runner.run()
        self.assertFalse("error" in err.lower())
        self.assertTrue("passed" in out.lower())

    @mock.patch("testrunner.runners.pytest_runner.virtualenv")
    def test_run_with_minus(self, venv_mock: MagicMock):
        def create_mock(project_name: str):
            return VenvMock(project_name)

        venv_mock.return_value.__enter__ = create_mock

        os.mkdir(os.path.join(self._dummy_dir, "testfoo"))

        r = PyTestRunner("test-foo", self._dummy_dir)
        o, e = r.run()

        self.assertEqual("out", o)
        self.assertEqual("err", e)

    @mock.patch("testrunner.runners.pytest_runner.virtualenv")
    def test_run_with_underscore(self, venv_mock: MagicMock):
        def create_mock(project_name: str):
            return VenvMock(project_name)

        venv_mock.return_value.__enter__ = create_mock

        os.mkdir(os.path.join(self._dummy_dir, "testfoo"))

        r = PyTestRunner("test_foo", self._dummy_dir)
        o, e = r.run()

        self.assertEqual("out", o)
        self.assertEqual("err", e)

    @mock.patch("testrunner.runners.pytest_runner.virtualenv")
    def test_run_with_underscore_to_minus(self, venv_mock: MagicMock):
        def create_mock(project_name: str):
            return VenvMock(project_name)

        venv_mock.return_value.__enter__ = create_mock

        os.mkdir(os.path.join(self._dummy_dir, "test_foo"))

        r = PyTestRunner("test-foo", self._dummy_dir)
        o, e = r.run()

        self.assertEqual("out", o)
        self.assertEqual("err", e)

    def test_get_total_result(self):
        s, m, c = self._dummy_runner.get_total_result(self._output)
        self.assertEqual(39, s)
        self.assertEqual(5, m)
        self.assertEqual("87%", c)

    def test_get_total_result_with_branches(self):
        s, m, c = self._dummy_runner.get_total_result(
            "TOTAL                             244      5     56      1    97%"
        )
        self.assertEqual(244, s)
        self.assertEqual(5, m)
        self.assertEqual("97%", c)

    def test_get_total_result_fail(self):
        self.assertIsNone(self._dummy_runner.get_total_result(""))

    def test_get_passed_result(self):
        r = self._dummy_runner.get_summary_result(self._output)
        self.assertEqual(0, r["failed"])
        self.assertEqual(13, r["passed"])
        self.assertEqual(0, r["skipped"])
        self.assertEqual(0, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(0.06, r["time"])

    def test_get_passed_result_with_skipped(self):
        r = self._dummy_runner.get_summary_result(
            "======== 49 passed, 3 skipped in 29.39 seconds ========="
        )
        self.assertEqual(0, r["failed"])
        self.assertEqual(49, r["passed"])
        self.assertEqual(3, r["skipped"])
        self.assertEqual(0, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(29.39, r["time"])

    def test_get_passed_result_skipped_error(self):
        r = self._dummy_runner.get_summary_result(
            "===== 1 failed, 49 passed, 3 skipped in 30.44 seconds ====="
        )
        self.assertEqual(1, r["failed"])
        self.assertEqual(49, r["passed"])
        self.assertEqual(3, r["skipped"])
        self.assertEqual(0, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(30.44, r["time"])

    def test_get_passed_result_with_failed(self):
        r = self._dummy_runner.get_summary_result(
            "========= 1 failed, 49 passed in 38.12 seconds ======"
        )
        self.assertEqual(1, r["failed"])
        self.assertEqual(49, r["passed"])
        self.assertEqual(0, r["skipped"])
        self.assertEqual(0, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(38.12, r["time"])

    def test_get_passed_result_with_error(self):
        r = self._dummy_runner.get_summary_result(
            "======== 55 failed, 18 passed, 13 error in 24.17 seconds ========="
        )
        self.assertEqual(55, r["failed"])
        self.assertEqual(18, r["passed"])
        self.assertEqual(0, r["skipped"])
        self.assertEqual(0, r["warnings"])
        self.assertEqual(13, r["error"])
        self.assertEqual(24.17, r["time"])

    def test_get_passed_result_with_warning(self):
        r = self._dummy_runner.get_summary_result(
            "======= 54 passed, 3 skipped, 1 warnings in 32.27 seconds ========"
        )
        self.assertEqual(0, r["failed"])
        self.assertEqual(54, r["passed"])
        self.assertEqual(3, r["skipped"])
        self.assertEqual(1, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(32.27, r["time"])

    def test_get_passed_result_with_failed_warning(self):
        r = self._dummy_runner.get_summary_result(
            "======== 4 failed, 15 passed, 2 warnings in 0.84 seconds ========="
        )
        self.assertEqual(4, r["failed"])
        self.assertEqual(15, r["passed"])
        self.assertEqual(0, r["skipped"])
        self.assertEqual(2, r["warnings"])
        self.assertEqual(0, r["error"])
        self.assertEqual(0.84, r["time"])

    def test_get_passed_result_fail(self):
        self.assertIsNone(self._dummy_runner.get_summary_result(""))


if __name__ == "__main__":
    unittest.main()
