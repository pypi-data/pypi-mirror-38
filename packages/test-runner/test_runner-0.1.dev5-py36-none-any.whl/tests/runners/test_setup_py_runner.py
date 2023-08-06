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
import shutil
import tempfile
import unittest
from git import Repo

from testrunner.runners.setup_py_runner import SetupPyRunner


class SetupPyRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        url = "https://github.com/audreyr/standardjson"
        self._repo = Repo.clone_from(url, self._tmp_dir)
        self._runner = SetupPyRunner("standardjson", self._tmp_dir)

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_run(self):
        out, err = self._runner.run()
        self.assertFalse("error" in err.lower())
        self.assertTrue("passed" in out.lower())

    def test_run_no_setup_py(self):
        runner = SetupPyRunner("test", "test")
        result = runner.run()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
