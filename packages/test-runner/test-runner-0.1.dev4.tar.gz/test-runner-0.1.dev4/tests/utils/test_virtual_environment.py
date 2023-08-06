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
import unittest

from testrunner.utils.preconditions import IllegalArgumentException
from testrunner.utils.virtual_environment import VirtualEnvironment


class VirtualEnvironmentTest(unittest.TestCase):
    def setUp(self):
        self._env_name = "VirtualEnvironmentTest"
        self._venv = VirtualEnvironment(self._env_name)

    def tearDown(self):
        self._venv.cleanup()

    def test_init_fail_without_environment_name(self):
        with self.assertRaises(IllegalArgumentException) as context:
            VirtualEnvironment("")
        self.assertTrue(isinstance(context.exception, IllegalArgumentException))
        self.assertTrue(
            "Cannot create an virtual environment without a name!"
            in str(context.exception)
        )

    def test_get_env_dir(self):
        env_dir = self._venv.get_env_dir()
        self.assertTrue(os.path.isdir(env_dir))
        self.assertEqual(self._env_name, env_dir[-len(self._env_name) :])

    def test_run_commands(self):
        self._venv.add_package_for_installation("benchexec")
        out, err = self._venv.run_commands([""])
        self.assertTrue("Successfully installed benchexec" in str(out))

    def test_add_package_for_installation(self):
        package = "test-foo"
        self._venv.add_package_for_installation(package)
        packages = self._venv._packages
        self.assertTrue(len(packages) == 1)
        self.assertEqual(package, packages[0])

    def test_add_packages_for_installation(self):
        package = ["test-foo", "test-bar"]
        self._venv.add_packages_for_installation(package)
        packages = self._venv._packages
        self.assertTrue(len(packages) == 2)
        self.assertEqual(package[0], packages[0])
        self.assertEqual(package[1], packages[1])


if __name__ == "__main__":
    unittest.main()
