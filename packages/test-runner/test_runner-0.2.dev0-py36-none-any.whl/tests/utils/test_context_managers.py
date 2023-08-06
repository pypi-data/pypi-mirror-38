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
import sys
import tempfile
import unittest

from testrunner.utils.context_managers import tempdir, cd, virtualenv


class ContextManagerTest(unittest.TestCase):
    @unittest.skipIf("darwin" in sys.platform.lower(), "Skip on macOS")
    def test_temp_dir(self):
        with tempdir() as temp_dir:
            self.assertTrue(os.path.isdir(temp_dir))
            self.assertEqual(temp_dir, os.getcwd())
        self.assertFalse(os.path.isdir(temp_dir))

    @unittest.skipUnless("darwin" in sys.platform.lower(), "Only for macOS")
    def test_temp_dir_macOS(self):
        with tempdir() as temp_dir:
            self.assertTrue(os.path.isdir(temp_dir))
            t_dir = "/private{}".format(temp_dir)
            self.assertEqual(t_dir, os.getcwd())
        self.assertFalse(os.path.isdir(temp_dir))

    @unittest.skipIf("darwin" in sys.platform.lower(), "Skip on macOS")
    def test_cd_without_cleanup(self):
        cwd = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        with cd(tmp_dir):
            self.assertEqual(tmp_dir, os.getcwd())
        self.assertEqual(cwd, os.getcwd())
        self.assertTrue(os.path.exists(tmp_dir))
        shutil.rmtree(tmp_dir)

    @unittest.skipUnless("darwin" in sys.platform.lower(), "Only on macOS")
    def test_cd_without_cleanup_macOS(self):
        cwd = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        with cd(tmp_dir):
            t_dir = "/private{}".format(tmp_dir)
            self.assertEqual(t_dir, os.getcwd())
        self.assertEqual(cwd, os.getcwd())
        self.assertTrue(os.path.exists(tmp_dir))
        shutil.rmtree(tmp_dir)

    @unittest.skipIf("darwin" in sys.platform.lower(), "Skip on macOS")
    def test_cd_with_cleanup(self):
        def cleanup():
            shutil.rmtree(tmp_dir)
            return True

        cwd = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        with cd(tmp_dir, cleanup):
            self.assertEqual(tmp_dir, os.getcwd())
        self.assertEqual(cwd, os.getcwd())
        self.assertFalse(os.path.exists(tmp_dir))

    @unittest.skipUnless("darwin" in sys.platform.lower(), "Only on macOS")
    def test_cd_with_cleanup_macOS(self):
        def cleanup():
            shutil.rmtree(tmp_dir)
            return True

        cwd = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        with cd(tmp_dir, cleanup):
            t_dir = "/private{}".format(tmp_dir)
            self.assertEqual(t_dir, os.getcwd())
        self.assertEqual(cwd, os.getcwd())
        self.assertFalse(os.path.exists(tmp_dir))

    def test_virtualenv(self):
        with virtualenv("test") as venv:
            self.assertTrue(os.path.isdir(venv.get_env_dir()))
        self.assertFalse(os.path.isdir(venv.get_env_dir()))


if __name__ == "__main__":
    unittest.main()
