# -*- coding: utf-8 -*-
from distutils import dir_util
import os
import pytest
from jatsutils import JatsElementTree as JET


@pytest.fixture()
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, bytes(tmpdir))

    return tmpdir


@pytest.fixture()
def static_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")


@pytest.fixture()
def element_tree(static_dir):
    return JET(from_file=os.path.join(static_dir, 'manuscript.xml'))
