import json
from urllib.parse import urlencode

import pytest

import pyshoper
from pyshoper.api import ShoperApi

BASE_URL = "https://example.pl"


@pytest.fixture()
def shoper_api(requests_mock):
    requests_mock.post('/webapi/rest/auth', json={'access_token': 'token'})
    api = ShoperApi('secret-login', 'wrong-password', base_url=BASE_URL)
    return api


def test_authentication(requests_mock):
    access_token = 'secret-access-token'
    requests_mock.post('/webapi/rest/auth', json={'access_token': access_token})
    api = ShoperApi('secret-login', 'secret-password', base_url=BASE_URL)
    # Check if request contains proper Authorization header
    requests_mock.get('/webapi/rest/producers', request_headers={'Authorization': f'Bearer {access_token}'}, json={})
    api.producers_list()


def test_responses_codes(requests_mock):
    # Test authentication error
    requests_mock.post('/webapi/rest/auth', status_code=401,
                       json={'error': 'unauthorized_client', 'error_description': ''})
    with pytest.raises(pyshoper.exceptions.AuthenticationError):
        ShoperApi('secret-login', 'wrong-password', base_url=BASE_URL)
    requests_mock.post('/webapi/rest/auth', json={'access_token': 'token'})
    api = ShoperApi('secret-login', 'wrong-password', base_url=BASE_URL)

    # Test all error types
    def check_error(status_code, error, exception):
        requests_mock.get('/webapi/rest/producers', status_code=status_code,
                          json={'error': error, 'error_description': ''})
        with pytest.raises(exception):
            api.producers_list()

    for key, exception in pyshoper.exceptions.error_map.items():
        status_code, error = key
        check_error(status_code, error, exception)

    # Test not implemented exception
    requests_mock.get('/webapi/rest/producers', status_code=666,
                      json={'error': 'error', 'error_description': ''})
    with pytest.raises(pyshoper.exceptions.ShoperApiError):
        api.producers_list()


def test_resources(requests_mock, shoper_api):
    def test_crud_methods(path, method_prefix, methods=('get', 'delete', 'insert', 'list', 'update')):
        elem_id = 666
        elem = {'id': elem_id}
        if 'delete' in methods:
            requests_mock.delete(path + f'/{elem_id}', json=elem_id)
            assert getattr(shoper_api, f'{method_prefix}_delete')(elem_id) == elem_id
        if 'get' in methods:
            requests_mock.get(path + f'/{elem_id}', json=elem)
            assert getattr(shoper_api, f'{method_prefix}_get')(elem_id) == elem
        if 'insert' in methods:
            requests_mock.post(path, json=elem)
            assert getattr(shoper_api, f'{method_prefix}_insert')(elem) == elem
        if 'list' in methods:
            requests_mock.get(path, json=[elem, elem])
            assert getattr(shoper_api, f'{method_prefix}_list')() == [elem, elem]
        if 'update' in methods:
            requests_mock.put(path + f'/{elem_id}', json=elem)
            assert getattr(shoper_api, f'{method_prefix}_update')(elem_id, elem) == elem

    for resource in pyshoper.api.shoper_resources:
        if 'methods' in resource:
            test_crud_methods(resource['path'], resource['name'], resource['methods'])
        else:
            test_crud_methods(resource['path'], resource['name'])


def test_filters_in_list_resource(requests_mock, shoper_api):
    filters = json.dumps({'name': 'test_producer'})
    request_url = '/webapi/rest/producers?' + urlencode({'limit': 10, 'page': 1, 'filters': filters})

    requests_mock.get(request_url, json={'filters': filters})

    shoper_api.producers_list(filters=filters)

