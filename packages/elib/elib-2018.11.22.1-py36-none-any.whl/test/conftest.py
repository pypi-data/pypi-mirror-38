# coding=utf-8
"""
Pytest config
"""
import os
import sys

import pytest
from mockito import unstub


# noinspection PyUnusedLocal
def pytest_configure(config):
    """Setup"""
    sys._called_from_test = True


# noinspection PyUnusedLocal,SpellCheckingInspection
def pytest_unconfigure(config):
    """Tear down"""
    # noinspection PyUnresolvedReferences,PyProtectedMember
    del sys._called_from_test


@pytest.fixture(autouse=True)
def cleandir(request, tmpdir):
    """Provides a clean working dir"""
    if 'nocleandir' in request.keywords:
        yield
    else:
        current_dir = os.getcwd()
        os.chdir(str(tmpdir))
        yield os.getcwd()
        os.chdir(current_dir)


@pytest.fixture(autouse=True)
def _clean_os_env():
    env = os.environ.copy()
    yield
    for key, value in env.items():
        os.environ[key] = value
    for key in os.environ.keys():
        if key not in env.keys():
            del os.environ[key]


@pytest.fixture(autouse=True)
def _unstub():
    unstub()
    yield
    unstub()


@pytest.fixture(autouse=True)
def _setup_logging():
    import logging
    logger = logging.getLogger('elib')
    logger.setLevel(logging.DEBUG)
    yield


def pytest_addoption(parser):
    """Add option for long tests"""
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    """Skip long tests"""
    long_marker = item.get_marker("long")
    if long_marker is not None and not item.config.getoption('long'):
        pytest.skip('skipping long tests')
