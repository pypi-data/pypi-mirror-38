# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
import subprocess

import pytest

from pex import interpreter
from pex.compatibility import PY3
from pex.testing import (
    IS_PYPY,
    PY27,
    PY35,
    ensure_python_distribution,
    ensure_python_interpreter,
    temporary_dir
)

try:
  from mock import patch
except ImportError:
  from unittest.mock import patch


def tuple_from_version(version_string):
  return tuple(int(component) for component in version_string.split('.'))


class TestPythonInterpreter(object):

  @pytest.mark.skipif(PY3,
                      reason='This test relies on the `reload` builtin which is not available in '
                             'python 3 as a builtin.')
  def test_all_does_not_raise_with_empty_path_envvar(self):
    """ additionally, tests that the module does not raise at import """
    with patch.dict(os.environ, clear=True):
      reload(interpreter)
      interpreter.PythonInterpreter.all()

  TEST_INTERPRETER1_VERSION = PY27
  TEST_INTERPRETER1_VERSION_TUPLE = tuple_from_version(TEST_INTERPRETER1_VERSION)

  TEST_INTERPRETER2_VERSION = PY35
  TEST_INTERPRETER2_VERSION_TUPLE = tuple_from_version(TEST_INTERPRETER2_VERSION)

  @pytest.fixture
  def test_interpreter1(self):
    return ensure_python_interpreter(self.TEST_INTERPRETER1_VERSION)

  @pytest.fixture
  def test_interpreter2(self):
    return ensure_python_interpreter(self.TEST_INTERPRETER2_VERSION)

  @pytest.mark.skipif(IS_PYPY)
  def test_interpreter_versioning(self, test_interpreter1):
    py_interpreter = interpreter.PythonInterpreter.from_binary(test_interpreter1)
    assert py_interpreter.identity.version == self.TEST_INTERPRETER1_VERSION_TUPLE

  @pytest.mark.skipif(IS_PYPY)
  def test_interpreter_caching_basic(self, test_interpreter1, test_interpreter2):
    py_interpreter1 = interpreter.PythonInterpreter.from_binary(test_interpreter1)
    py_interpreter2 = interpreter.PythonInterpreter.from_binary(test_interpreter2)
    assert py_interpreter1 is not py_interpreter2
    assert py_interpreter2.identity.version == self.TEST_INTERPRETER2_VERSION_TUPLE

    py_interpreter3 = interpreter.PythonInterpreter.from_binary(test_interpreter1)
    assert py_interpreter1 is py_interpreter3

  @pytest.mark.skipif(IS_PYPY)
  def test_interpreter_caching_include_site_extras(self, test_interpreter1):
    py_interpreter1 = interpreter.PythonInterpreter.from_binary(test_interpreter1,
                                                                include_site_extras=False)
    py_interpreter2 = interpreter.PythonInterpreter.from_binary(test_interpreter1,
                                                                include_site_extras=True)
    py_interpreter3 = interpreter.PythonInterpreter.from_binary(test_interpreter1)
    assert py_interpreter1 is not py_interpreter2
    assert py_interpreter1.identity.version == py_interpreter2.identity.version
    assert py_interpreter2 is py_interpreter3

  @pytest.mark.skipif(IS_PYPY)
  def test_interpreter_caching_path_extras(self):
    python, pip = ensure_python_distribution(self.TEST_INTERPRETER1_VERSION)
    with temporary_dir() as td:
      path_extra = os.path.realpath(td)
      subprocess.check_call([pip,
                             'install',
                             '--target={}'.format(path_extra),
                             'ansicolors==1.1.8'])
      py_interpreter1 = interpreter.PythonInterpreter.from_binary(python,
                                                                  path_extras=[path_extra],
                                                                  include_site_extras=False)
      py_interpreter2 = interpreter.PythonInterpreter.from_binary(python,
                                                                  include_site_extras=False)
      py_interpreter3 = interpreter.PythonInterpreter.from_binary(python,
                                                                  path_extras=[path_extra],
                                                                  include_site_extras=False)
      assert py_interpreter1 is not py_interpreter2
      assert py_interpreter1.extras == {('ansicolors', '1.1.8'): path_extra}
      assert py_interpreter2.extras == {}
      assert py_interpreter1 is py_interpreter3
