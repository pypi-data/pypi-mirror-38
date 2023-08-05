import uplink

from .api_helpers import error_map, ShoperApiError


def raise_for_status(response):
    """Checks whether or not the response was successful."""
    if response.status_code != 200:
        res_data = response.json()
        if (response.status_code, res_data['error']) in error_map:
            raise error_map[(response.status_code, res_data['error'])](res_data['error_description'])
        raise ShoperApiError(res_data['error_description'])

    return response


def add_shoper_get_method(cls, name, path):
    @uplink.returns.json
    @uplink.response_handler(raise_for_status)
    @uplink.get(path + '/{id}')
    def shoper_get_method(self, id: uplink.Path):
        """Fetches an object."""
        pass

    setattr(cls, f"{name}_get", shoper_get_method)


def add_shoper_list_method(cls, name, path):
    @uplink.returns.json
    @uplink.response_handler(raise_for_status)
    @uplink.get(path)
    def shoper_list_method(self, limit: uplink.Query = 10, page: uplink.Query = 1, filters: uplink.Query=''):
        """Fetches objects collection."""
        pass

    setattr(cls, f"{name}_list", shoper_list_method)


def add_shoper_delete_method(cls, name, path):
    @uplink.returns.json
    @uplink.response_handler(raise_for_status)
    @uplink.delete(path + '/{id}')
    def shoper_delete_method(self, id: uplink.Path):
        """Deletes an object."""
        pass

    setattr(cls, f"{name}_delete", shoper_delete_method)


def add_shoper_insert_method(cls, name, path):
    @uplink.returns.json
    @uplink.response_handler(raise_for_status)
    @uplink.json
    @uplink.post(path)
    def shoper_insert_method(self, body: uplink.Body):
        """Fetches an object."""
        pass

    setattr(cls, f"{name}_insert", shoper_insert_method)


def add_shoper_update_method(cls, name, path):
    @uplink.returns.json
    @uplink.response_handler(raise_for_status)
    @uplink.json
    @uplink.put(path + '/{id}')
    def shoper_update_method(self, id: uplink.Path, body: uplink.Body):
        pass

    setattr(cls, f"{name}_update", shoper_update_method)


def add_shoper_methods_set(cls, name, path, methods=('get', 'delete', 'insert', 'list', 'update')):
    if 'get' in methods:
        add_shoper_get_method(cls, name, path)
    if 'list' in methods:
        add_shoper_list_method(cls, name, path)
    if 'delete' in methods:
        add_shoper_delete_method(cls, name, path)
    if 'insert' in methods:
        add_shoper_insert_method(cls, name, path)
    if 'update' in methods:
        add_shoper_update_method(cls, name, path)


@uplink.returns.json
@uplink.response_handler(raise_for_status)
class ShoperApi(uplink.Consumer):
    @uplink.post("/webapi/rest/auth")
    def authentication(self, client_id: uplink.Query("client_id"), client_secret: uplink.Query("client_secret")): pass

    def __init__(self, username, password, **kwargs):
        super().__init__(**kwargs)
        response = self.authentication(username, password)
        access_token = response['access_token']
        self.session.headers["Authorization"] = f'Bearer {access_token}'

shoper_resources = [
    {
        'name': 'aboutpages',
        'path': '/webapi/rest/aboutpages/',
    },
    {
        'name': 'additional_fields',
        'path': '/webapi/rest/additional-fields',
    },
    {
        'name': 'application_config',
        'path': '/webapi/rest/application-config',
        'methods': ('list',),
    },
    {
        'name': 'application_lock',
        'path': '/webapi/rest/application-lock',
        'methods': ('get', 'delete', 'insert', 'update'),
    },
    {
        'name': 'application_version',
        'path': '/webapi/rest/application-version',
        'methods': ('list',),
    },
    {
        'name': 'attribute_groups',
        'path': '/webapi/rest/attribute-groups',
    },
    {
        'name': 'attributes',
        'path': '/webapi/rest/attributes',
    },
    {
        'name': 'auction_houses',
        'path': '/webapi/rest/auction-houses',
    },
    {
        'name': 'auction_orders',
        'path': '/webapi/rest/auction-orders',
        'methods': ('get', 'list', 'insert', 'update'),
    },
    {
        'name': 'auctions',
        'path': '/webapi/rest/auctions',
    },
    {
        'name': 'availabilities',
        'path': '/webapi/rest/availabilities',
        'methods': ('get', 'list'),
    },
    {
        'name': 'categories_tree',
        'path': '/webapi/rest/categories-tree',
        'methods': ('get', 'list'),
    },
    {
        'name': 'categories',
        'path': '/webapi/rest/categories',
    },
    {
        'name': 'currencies',
        'path': '/webapi/rest/currencies',
        'methods': ('get', 'list'),
    },
    {
        'name': 'dashboard_activities',
        'path': '/webapi/rest/dashboard-activities',
        'methods': ('list',),
    },
    {
        'name': 'dashboard_stats',
        'path': '/webapi/rest/dashboard-stats',
        'methods': ('get',),
    },
    {
        'name': 'deliveries',
        'path': '/webapi/rest/deliveries',
        'methods': ('get', 'list'),
    },
    {
        'name': 'gauges',
        'path': '/webapi/rest/gauges',
        'methods': ('get', 'list'),
    },
    {
        'name': 'geolocation_countries',
        'path': '/webapi/rest/geolocation-countries',
        'methods': ('get', 'list'),
    },

    {
        'name': 'geolocation_regions',
        'path': '/webapi/rest/geolocation-regions',
        'methods': ('get', 'list'),
    },
    {
        'name': 'geolocation_subregions',
        'path': '/webapi/rest/geolocation-subregions',
        'methods': ('get', 'list'),
    },
    {
        'name': 'languages',
        'path': '/webapi/rest/languages',
        'methods': ('get', 'list'),
    },
    {
        'name': 'metafield_values',
        'path': '/webapi/rest/metafield-values',
    },
    # {
    #     'name': 'metafields',
    #     'path': '/webapi/rest/metafields/<object>',
    # },
    {
        'name': 'news_categories',
        'path': '/webapi/rest/news-categories',
    },
    {
        'name': 'news_comments',
        'path': '/webapi/rest/news-comments',
    },
    {
        'name': 'news_files',
        'path': '/webapi/rest/news-files',
    },
    {
        'name': 'news_tags',
        'path': '/webapi/rest/news-tags',
    },
    {
        'name': 'news',
        'path': '/webapi/rest/news',
    },
    {
        'name': 'object_mtime',
        'path': '/webapi/rest/object-mtime',
        'methods': ('get',),
    },
    {
        'name': 'option_groups',
        'path': '/webapi/rest/option-groups',
    },
    {
        'name': 'option_values',
        'path': '/webapi/rest/option-values',
    },
    {
        'name': 'options',
        'path': '/webapi/rest/options',
    },
    {
        'name': 'order_products',
        'path': '/webapi/rest/order-products',
    },
    {
        'name': 'orders',
        'path': '/webapi/rest/orders',
    },
    {
        'name': 'parcels',
        'path': '/webapi/rest/parcels',
        'methods': ('get', 'list', 'insert', 'update'),
    },
    {
        'name': 'payments',
        'path': '/webapi/rest/payments',
        'methods': ('get', 'list'),
    },
    {
        'name': 'producers',
        'path': '/webapi/rest/producers',
    },
    {
        'name': 'product_files',
        'path': '/webapi/rest/product-files',
    },
    {
        'name': 'product_images',
        'path': '/webapi/rest/product-images',
    },
    {
        'name': 'product_stocks',
        'path': '/webapi/rest/product-stocks',
    },

    {
        'name': 'products',
        'path': '/webapi/rest/products',
    },
    {
        'name': 'shippings',
        'path': '/webapi/rest/shippings',
    },
    {
        'name': 'statuses',
        'path': '/webapi/rest/statuses',
        'methods': ('get', 'list'),
    },
    {
        'name': 'subscriber-groups',
        'path': '/webapi/rest/subscriber-groups',
    },
    {
        'name': 'product_stocks',
        'path': '/webapi/rest/product-stocks',
    },
    {
        'name': 'subscribers',
        'path': '/webapi/rest/subscribers',
    },
    {
        'name': 'taxes',
        'path': '/webapi/rest/taxes',
        'methods': ('get', 'list'),
    },
    {
        'name': 'units',
        'path': '/webapi/rest/units',
    },
    {
        'name': 'user_addresses',
        'path': '/webapi/rest/user-addresses',
    },
    {
        'name': 'user_groups',
        'path': '/webapi/rest/user-groups',
    },
    {
        'name': 'users',
        'path': '/webapi/rest/users',
    },
    {
        'name': 'webhooks',
        'path': '/webapi/rest/webhooks',
    },
    {
        'name': 'zones',
        'path': '/webapi/rest/zones',
    },
]

for resource in shoper_resources:
    if 'methods' in resource:
        add_shoper_methods_set(ShoperApi, resource['name'], resource['path'], resource['methods'])
    else:
        add_shoper_methods_set(ShoperApi, resource['name'], resource['path'])