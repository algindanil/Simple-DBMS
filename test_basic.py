import logging
import os

import pytest

from core import DBManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(process)d | %(levelname)s | %(message)s'
)


TEST_DB_PATH = 'testdb.json'
TEST_DB_LOCK_PATH = '{}.lock'.format(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def run_around_tests():

    logging.debug('Test started.')
    yield
    logging.debug('Test ended.')

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    if os.path.exists(TEST_DB_LOCK_PATH):
        os.remove(TEST_DB_LOCK_PATH)


def test_get_and_set():

    database = DBManager(TEST_DB_PATH)
    key, val = 'test_key', list(range(100))
    database.set(key, val)

    assert database.get(key) == [val]


def test_remove():

    database = DBManager(TEST_DB_PATH)
    for i in range(10):
        database.set(i, i)

    database.remove(0)

    for i in range(10):
        if i == 0:
            assert database.get(i) == []
        else:
            assert database.get(i)

