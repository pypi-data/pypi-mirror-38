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
from testrunner.runner import Runner, RunnerType  # noqa: F401
from testrunner.utils.preconditions import (  # noqa: F401
    IllegalArgumentException,
    IllegalStateException,
    NoneValueException,
)

__version__ = "0.1.dev9"
__name__ = "test-runner"
__author__ = "Stephan Lukasczyk"
