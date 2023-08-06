# -*- coding: utf-8 -*-

import contextlib

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
from typing import Union, Generator, Any, Callable

from testrunner.utils.virtual_environment import VirtualEnvironment


@contextlib.contextmanager
def cd(
    new_dir: Union[bytes, str, os.PathLike],
    cleanup: Callable[[], bool] = lambda: True,
) -> Generator[Any, Any, None]:
    """
    A context that changes directories

    :param new_dir: The new directory path
    :param cleanup: A function indicating whether the directory should be
    removed after the context was left
    :return: A generator for the context
    """
    prev_dir: Union[bytes, str] = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)
        cleanup()


@contextlib.contextmanager
def tempdir() -> Generator[Union[bytes, str], Any, None]:
    """
    Creates a context holding a temporary directory

    :return: The context generator
    """
    dir_path = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dir_path)
        return True

    with cd(dir_path, cleanup):
        yield dir_path


@contextlib.contextmanager
def virtualenv(env_name: str) -> Generator[VirtualEnvironment, Any, None]:
    venv = VirtualEnvironment(env_name)
    yield venv
    venv.cleanup()
