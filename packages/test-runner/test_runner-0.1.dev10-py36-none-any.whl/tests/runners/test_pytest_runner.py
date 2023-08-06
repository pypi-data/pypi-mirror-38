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

from testrunner.runners.pytest_runner import PyTestRunner


class PyTestRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
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

    def test_run(self):
        out, err = self._runner.run()
        self.assertFalse("error" in err.lower())
        self.assertTrue("passed" in out.lower())

    def test_get_total_result(self):
        s, m, c = self._dummy_runner.get_total_result(self._output)
        self.assertEqual(39, s)
        self.assertEqual(5, m)
        self.assertEqual("87%", c)

    def test_get_total_result_fail(self):
        self.assertIsNone(self._dummy_runner.get_total_result(""))

    def test_get_passed_result(self):
        f, p, s, t = self._dummy_runner.get_summary_result(self._output)
        self.assertEqual(0, f)
        self.assertEqual(13, p)
        self.assertEqual(0, s)
        self.assertEqual(0.06, t)

    def test_get_passed_result_with_skipped(self):
        f, p, s, t = self._dummy_runner.get_summary_result(
            "======== 49 passed, 3 skipped in 29.39 seconds ========="
        )
        self.assertEqual(0, f)
        self.assertEqual(49, p)
        self.assertEqual(3, s)
        self.assertEqual(29.39, t)

    def test_get_passed_result_skipped_error(self):
        f, p, s, t = self._dummy_runner.get_summary_result(
            "===== 1 failed, 49 passed, 3 skipped in 30.44 seconds ====="
        )
        self.assertEqual(1, f)
        self.assertEqual(49, p)
        self.assertEqual(3, s)
        self.assertEqual(30.44, t)

    def test_get_passed_result_with_error(self):
        f, p, s, t = self._dummy_runner.get_summary_result(
            "========= 1 failed, 49 passed in 38.12 seconds ======"
        )
        self.assertEqual(1, f)
        self.assertEqual(49, p)
        self.assertEqual(0, s)
        self.assertEqual(38.12, t)

    def test_get_passed_result_fail(self):
        self.assertIsNone(self._dummy_runner.get_summary_result(""))


if __name__ == "__main__":
    unittest.main()
