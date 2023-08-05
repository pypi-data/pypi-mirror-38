# pyshoper - Python client to shoper.pl REST api

## Summary

## Exampler of use
Basic usage of pyshoper:
```python
from pyshoper.client import ShoperClient

base_url = "https://example.com"
api = ShoperClient('login', 'password', base_url=base_url)

print(api.products_list(filters={'stock.stock': 0}))
```
and expected result should something alike:
```python
{
    'count': '49',
    'list': [
        {'code': 'prod-0001', ...},
        {'code': 'prod-0002', ...},
        {'code': 'prod-0003', ...},
        {'code': 'prod-0004', ...},
        ...
    ],
    'page': 1,
    'pages': 5,
}
```

to iterate through all products using client's generator:
```python
for i, prod in enumerate(api.products_generator(limit=100)):
    print(prod)
    if i > 200:
        break
```

## More

Exceptions