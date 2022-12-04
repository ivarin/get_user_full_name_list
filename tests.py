import json
import logging
import pytest
import requests

from main import get_users_full_name_list
from main import url

logger = logging.getLogger(__name__)


@pytest.fixture
def total_amount():
    r = requests.get(url)
    yield json.loads(r.text)['total']


@pytest.fixture
def full_list(total_amount):
    yield get_users_full_name_list(1, total_amount)


@pytest.mark.parametrize(
    'ids, names', [((1, 1), ['George Bluth']),
                   ((2, 3), ['Emma Wong', 'Janet Weaver']),
                   ((5, 7), ['Charles Morris', 'Michael Lawson', 'Tracey Ramos']),
                   ((12, 12), ['Rachel Howell'])]
)
def test_users_id(ids, names):
    logger.info(f'check if {ids} mathes {names}')
    assert get_users_full_name_list(*ids) == names


@pytest.mark.parametrize(
    'values', [(1, 0), ('0', 0), (1, 5, 7), ('ø', 15, '¡∞')]
)
def test_users_id_bad_values(values):
    logger.info(f'check {values} for []')
    assert get_users_full_name_list(values) == []


def test_total_twelve(full_list, total_amount):
    assert len(full_list) == total_amount


def test_names_capital(full_list):
    for name in full_list:  # decided to avoid parametrization here
        assert all([x[0].isupper() for x in name.split()]), \
        f'Unexpected value {name}'


def test_exactly_two_fields(full_list):
    for name in full_list:
        assert len(name.split()) == 2, \
        f'Unexpected value {name}'


def test_total_amount(total_amount):
    logger.info(total_amount)
