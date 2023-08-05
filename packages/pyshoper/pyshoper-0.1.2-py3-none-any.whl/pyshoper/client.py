import json

import backoff

from pyshoper.api import ShoperApi, shoper_resources
from pyshoper import exceptions

API_METHOD_MAX_RETRIES = 12
API_METHOD_MAX_TIME = 60 * 15


class ShoperClient:

    def __init__(self, username, password, base_url, max_tries=API_METHOD_MAX_RETRIES, max_time=API_METHOD_MAX_TIME):
        self.username = username
        self.password = password
        self.api = ShoperApi(username, password, base_url=base_url)

        self.max_tries = max_tries
        self.max_time = max_time
        self.special_methods = dict()
        self._preapre_clinet()

    def _preapre_clinet(self):
        for resource in shoper_resources:
            methods = resource.get('methods', ('get', 'delete', 'insert', 'list', 'update'))
            if 'list' in methods:
                self.special_methods[f'{resource["name"]}_generator'] = f'{resource["name"]}_list'

    @staticmethod
    def _list_resource_decorator(method):
        def new_method(*args, **kwargs):
            if 'filters' in kwargs:
                kwargs['filters'] = json.dumps(kwargs['filters'])
            result = method(*args, **kwargs)
            return result

        return new_method

    def _list_resource_generator(self, method):
        method = backoff.on_exception(backoff.expo, exceptions.CallsLimitExceededError,
                                      max_tries=self.max_tries, max_time=self.max_time, jitter=None)(method)

        def new_method(*args, **kwargs):
            page = 1
            while True:
                kwargs['page'] = page
                result = method(*args, **kwargs)
                if not result['list']:
                    break
                for elem in result['list']:
                    yield elem
                page += 1

        return new_method

    def __getattr__(self, item):
        if item in self.special_methods:
            orig_attr = self.__getattr__(self.special_methods[item])
            return self._list_resource_generator(orig_attr)
        orig_attr = self.api.__getattribute__(item)
        if item.endswith('_list'):
            return self._list_resource_decorator(orig_attr)
        else:
            return orig_attr
