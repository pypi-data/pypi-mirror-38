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
import unittest
from unittest import mock

from testrunner.runners.pytest_runner import PyTestRunner
from testrunner.runners.setup_py_runner import SetupPyRunner
from testrunner.runner import Runner, RunnerType
from testrunner.utils.preconditions import IllegalStateException


class TestRunner(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
