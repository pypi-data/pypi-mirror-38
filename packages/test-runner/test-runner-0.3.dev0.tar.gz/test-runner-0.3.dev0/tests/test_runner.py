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
from unittest import mock

from pytesting_utils import IllegalStateException

from testrunner.runner import Runner, RunnerType
from testrunner.runners.pytest_runner import PyTestRunner
from testrunner.runners.setup_py_runner import SetupPyRunner


class TestRunner(unittest.TestCase):
    def setUp(self):
        self._pytest_dir = tempfile.mkdtemp()
        self._setup_py_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._pytest_dir)
        shutil.rmtree(self._setup_py_dir)

    def test_instantiate_pytest_runner(self):
        test_runner = Runner("test", "test", RunnerType.PYTEST)
        runner = test_runner._instantiate_runner()
        self.assertTrue(isinstance(runner, PyTestRunner))

    def test_instantiate_setup_py_runner(self):
        test_runner = Runner("test", "test", RunnerType.SETUP_PY)
        runner = test_runner._instantiate_runner()
        self.assertTrue(isinstance(runner, SetupPyRunner))

    def test_instantiate_unknown_runner(self):
        with self.assertRaises(IllegalStateException) as context:
            Runner("test", "test", RunnerType.AUTO_DETECT)
        self.assertTrue(
            "Could not find a matching runner!" in str(context.exception)
        )

    def test_run(self):
        with mock.patch("testrunner.runner.PyTestRunner") as MockHelper:
            MockHelper.return_value.run.return_value = ("foo", "bar")
            runner = Runner("test", "test", RunnerType.PYTEST)
            result = runner.run()
            MockHelper.assert_called_once()
            self.assertEqual(("foo", "bar"), result)

    def test_get_total_result(self):
        with mock.patch("testrunner.runner.PyTestRunner") as MockHelper:
            MockHelper.return_value.get_total_result.return_value = (
                23,
                42,
                "foo",
            )
            runner = Runner("test", "test", RunnerType.PYTEST)
            result = runner.get_total_result("bar")
            MockHelper.assert_called_once()
            self.assertEqual((23, 42, "foo"), result)

    def test_get_summary_result(self):
        with mock.patch("testrunner.runner.PyTestRunner") as MockHelper:
            MockHelper.return_value.get_summary_result.return_value = {
                "failed": 0,
                "passed": 8,
                "skipped": 15,
                "time": 23.42,
            }
            runner = Runner("test", "test", RunnerType.PYTEST)
            result = runner.get_summary_result("bar")
            MockHelper.assert_called_once()
            r = {"failed": 0, "passed": 8, "skipped": 15, "time": 23.42}
            self.assertEqual(r, result)

    def test_is_not_pytest(self):
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertFalse(runner._is_pytest())

    def test_is_not_setup_py(self):
        runner = Runner("test", self._setup_py_dir, RunnerType.SETUP_PY)
        self.assertFalse(runner._is_setup_py())

    def test_is_not_pytest_setup_py(self):
        with open(os.path.join(self._pytest_dir, "setup.py"), "w") as f:
            f.write("    test_suite=nose")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertFalse(runner._is_pytest())

    def test_is_pytest_setup_test_suite_pytest(self):
        with open(os.path.join(self._pytest_dir, "setup.py"), "w") as f:
            f.write("    test_suite=pytest")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_is_pytest_setup_test_suite_py_test(self):
        with open(os.path.join(self._pytest_dir, "setup.py"), "w") as f:
            f.write("    test_suite=py.test")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_is_pytest_ini(self):
        with open(os.path.join(self._pytest_dir, "pytest.ini"), "w") as f:
            f.write("foo")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_is_pytest_import(self):
        with open(os.path.join(self._pytest_dir, "foo.py"), "w") as f:
            f.write("import pytest")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_is_pytest_from_import(self):
        with open(os.path.join(self._pytest_dir, "foo.py"), "w") as f:
            f.write("from pytest import foo")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_is_pytest_grep(self):
        with open(os.path.join(self._pytest_dir, "foo.txt"), "w") as f:
            f.write("foo pytest bar")
        runner = Runner("test", self._pytest_dir, RunnerType.PYTEST)
        self.assertTrue(runner._is_pytest())

    def test_detect_runner_type_pytest(self):
        with open(os.path.join(self._pytest_dir, "foo.txt"), "w") as f:
            f.write("foo pytest bar")
        runner = Runner("test", self._pytest_dir, RunnerType.AUTO_DETECT)
        runner_type = runner._detect_runner_type()
        self.assertEqual(runner_type, RunnerType.PYTEST)

    def test_is_setup_py_test(self):
        with open(os.path.join(self._setup_py_dir, "setup.py"), "w") as f:
            f.write("    test_suite=nose")
        runner = Runner("test", self._setup_py_dir, RunnerType.SETUP_PY)
        self.assertTrue(runner._is_setup_py())

    def test_is_not_setup_py_test(self):
        with open(os.path.join(self._setup_py_dir, "setup.py"), "w") as f:
            f.write("foo")
        runner = Runner("test", self._setup_py_dir, RunnerType.SETUP_PY)
        self.assertFalse(runner._is_setup_py())

    def test_detect_runner_type_setup_py(self):
        with open(os.path.join(self._setup_py_dir, "setup.py"), "w") as f:
            f.write("    test_suite=nose")
        runner = Runner("test", self._setup_py_dir, RunnerType.SETUP_PY)
        runner_type = runner._detect_runner_type()
        self.assertEqual(runner_type, RunnerType.SETUP_PY)


if __name__ == "__main__":
    unittest.main()
