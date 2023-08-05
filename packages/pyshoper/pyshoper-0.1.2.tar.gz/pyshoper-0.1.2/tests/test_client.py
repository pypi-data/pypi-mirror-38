import json
from urllib.parse import urlencode

import pytest

from pyshoper.client import ShoperClient

BASE_URL = "https://example.pl"


@pytest.fixture()
def shoper_client(requests_mock):
    requests_mock.post('/webapi/rest/auth', json={'access_token': 'token'})
    api = ShoperClient('pyshoper', 'Lh9JbdaYnsqygzUNdsZt', base_url=BASE_URL)
    return api


def test_client_params_wrapper(shoper_client, requests_mock):
    filters = {'name': 'test_producer'}
    request_url = '/webapi/rest/producers?' + urlencode({'limit': 10, 'page': 1, 'filters': json.dumps(filters)})
    requests_mock.get(request_url, json=filters)
    res = shoper_client.producers_list(filters=filters)
    assert res == filters


def test_generator(shoper_client, requests_mock):
    requests_mock.get('/webapi/rest/producers', [{'json': {'list': [1, 2, 3]}}, {'json': {'list': [4, 5, 6]}}, {'json': {'list': []}}])
    results = list(shoper_client.producers_generator())
    assert results == [1, 2, 3, 4, 5, 6]


def test_retries_on_exception(shoper_client, requests_mock):
    requests_mock.get('/webapi/rest/producers',
                      [{'json': {'list': [1, 2, 3]}},
                       {'status_code': 429, 'json': {'error': 'temporarily_unavailable', 'error_description': ''}},
                       {'json': {'list': [4, 5, 6]}},
                       {'json': {'list': []}}])
    results = list(shoper_client.producers_generator())
    assert results == [1, 2, 3, 4, 5, 6]
