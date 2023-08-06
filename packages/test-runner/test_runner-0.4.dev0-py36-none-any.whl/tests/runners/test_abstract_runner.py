# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from pytesting_utils import IllegalArgumentException

from testrunner.runners.abstract_runner import AbstractRunner


class AbstractRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        files = {
            "requirements.txt": "foo",
            "dev-requirements.txt": "bar",
            "test-requirements.txt": "baz",
            "requirements-test.txt": "-r requirements.txt",
        }
        for k, v in files.items():
            with open(os.path.join(self._tmp_dir, k), "w") as f:
                f.write(v)

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    def test_cannot_instantiate(self):
        """Showing we normally cannot instantiate an abstract class"""
        with self.assertRaises(TypeError):
            AbstractRunner("foo", "bar")

    @patch.multiple(AbstractRunner, __abstractmethods__=set())
    def test_empty_project_name(self):
        with self.assertRaises(IllegalArgumentException) as context:
            AbstractRunner("", "bar")
        self.assertTrue(isinstance(context.exception, IllegalArgumentException))
        self.assertTrue(
            "Project name must not be empty!" in str(context.exception)
        )

    @patch.multiple(AbstractRunner, __abstractmethods__=set())
    def test_empty_path(self):
        with self.assertRaises(IllegalArgumentException) as context:
            AbstractRunner("foo", "")
        self.assertTrue(isinstance(context.exception, IllegalArgumentException))
        self.assertTrue("Path must not be empty!" in str(context.exception))

    @patch.multiple(AbstractRunner, __abstractmethods__=set())
    def test_extract_necessary_packages(self):
        runner = AbstractRunner("foo", self._tmp_dir)
        result = runner._extract_necessary_packages()
        self.assertTrue("foo" in result)
        self.assertTrue("bar" in result)
        self.assertTrue("baz" in result)


if __name__ == "__main__":
    unittest.main()
