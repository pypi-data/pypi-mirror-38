import uuid
import copy
import requests
import requests.auth
import json
import logging
import datetime
import dateutil.parser
import dateutil.tz

import productstatus.utils
import productstatus.exceptions
import productstatus.event


SERVICE_UNAVAILABLE_EXCEPTIONS = (requests.exceptions.RequestException,
                                  requests.exceptions.Timeout,
                                  )


class Api(object):
    """
    This class provides fluent access to the Productstatus REST API. Resource
    collections are exposed as members of the Api class, and specific resources
    can be retrieved by indexes.

    The API client tries to be as lazy as possible, and does not make any
    unneccessary requests to the server.

    Examples of use:

    api = Api('http://localhost:8000')
    products = api.product
    arome = products['66340f0b-2c2c-436d-a077-3d939f4f7283']
    print(arome.grid_resolution)
    """

    def __init__(self, base_url, verify_ssl=True, username=None, api_key=None, timeout=3):
        """
        Initialize the Api class.

        @param base_url The root URL where the Productstatus server serves data.
        @param verify_ssl Whether or not to verify SSL certificates.
        @param username Client API username.
        @param api_key Client API key.
        @param timeout Request timeout in seconds.
        """
        self._base_url = base_url.rstrip('/')
        self._url_prefix = '/api/v1/'
        self._url = productstatus.utils.build_url(self._base_url, self._url_prefix)
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._session = requests.Session()
        self._session.verify = self._verify_ssl
        self._session.headers.update({'content-type': 'application/json'})
        self._event_listener = None
        if username and api_key:
            self._session.auth = TastypieApiKeyAuth(username, api_key)
        self._resource_collection = {}
        self._schema = {}

    def get_event_listener_configuration(self):
        """!
        @brief Fetch the message queue configuration from the Productstatus server.
        """
        return self.kafka['default']

    def get_event_listener(self, **kwargs):
        """!
        @brief Instantiate a message delivery object with configuration
        retrieved from the Productstatus server.
        @returns A productstatus.event.Listener object.
        """
        if not self._event_listener:
            configuration = self.get_event_listener_configuration()
            kwargs['bootstrap_servers'] = configuration.brokers
            kwargs['ssl'] = configuration.ssl
            kwargs['ssl_verify'] = configuration.ssl_verify
            self._event_listener = productstatus.event.Listener(str(configuration.topic), **kwargs)
        return self._event_listener

    def delete_event_listener(self):
        """!
        @brief Destroy the event listener object.
        """
        if not self._event_listener:
            return
        self._event_listener.close()
        del self._event_listener
        self._event_listener = None

    def has_credentials(self):
        """!
        @brief Returns True if a username and API key was supplied with the API
        object constructor, False otherwise.
        """
        return self._session.auth is not None

    def _do_request(self, method, *args, **kwargs):
        """
        Run a request through the requests API. This function wraps
        self.session.{get,post,patch,put,delete} and adds exception handling.

        Returns a response object.
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self._timeout
        try:
            response = self._session.request(method, *args, **kwargs)
        except SERVICE_UNAVAILABLE_EXCEPTIONS as e:
            raise productstatus.exceptions.ServiceUnavailableException(
                "Could not perform request: %s" % str(e)
            )

        self._raise_response_exceptions(response)
        return response

    def _get_response_data(self, response):
        """
        Get unserialized contents from a response object.
        """
        if response.content:
            return self._unserialize(response.content)
        return response.content

    def _raise_response_exceptions(self, response):
        """
        Conditionally raise exceptions if a response object has errors.
        """
        if response.status_code < 400:
            return
        if response.status_code >= 500:
            exception = productstatus.exceptions.ServiceUnavailableException
        elif response.status_code == 401:
            exception = productstatus.exceptions.UnauthorizedException
        elif response.status_code == 404:
            exception = productstatus.exceptions.NotFoundException
        else:
            exception = productstatus.exceptions.ClientErrorException
        raise exception(response.text)

    def _unserialize(self, data):
        """
        Convert JSON encoded data into a dictionary.
        """
        try:
            return json.loads(data.decode('UTF-8'))
        except ValueError as e:
            raise productstatus.exceptions.UnserializeException(e)

    def _get_schema_from_server(self):
        """
        Retrieve a list of possible resource types from the server.
        """
        response = self._do_request('get', self._url)
        self._schema = self._get_response_data(response)

    def _validate_url_component(self, name):
        """
        Raise an exception if an URL slug cannot be used to determine the
        location of a resource or collection.
        """
        if len(name) == 0:
            raise NameError('URL components cannot be empty')
        if name[0] == '_':
            raise NameError('URL components cannot begin with an underscore')

    def __getattr__(self, name):
        """
        Return a ResourceCollection object which can be used to retrieve
        resources. E.g. api.productinstance will point to /api/v1/productinstance/.
        """
        if name not in self._resource_collection.keys():
            if not self._schema:
                self._get_schema_from_server()
            if name not in self._schema.keys():
                # ignore Python internal functions
                if name[:2] == '__':
                    raise AttributeError('Attribute %s not found' % name)
                raise productstatus.exceptions.ResourceTypeNotFoundException(
                    "The resource '%s' is not supported by the Productstatus server" % name)
            self._resource_collection[name] = ResourceCollection(self, name)
        return self._resource_collection[name]

    def __getitem__(self, index):
        """
        Provide direct access to an API object. For instance, accessing
        api['/api/v1/product/66340f0b-2c2c-436d-a077-3d939f4f7283/'] will return a
        Resource object.
        """
        prefix_length = len(self._url_prefix)
        if self._url_prefix != index[:prefix_length]:
            raise KeyError('The URL %s is unsupported by this API instance; the URL must begin with %s' %
                           (index, self._url_prefix))
        components = index[prefix_length:].strip('/').split('/')

        # Sanity checks
        if len(components) == 0:
            return self
        for slug in components:
            self._validate_url_component(slug)

        # Load collection
        collection = getattr(self, components[0])
        if len(components) == 1:
            return collection

        # Load resource
        resource = collection[components[1]]
        if len(components) == 2:
            return resource

        raise NameError('The URL %s in unsupported by this API instance; the URL contains too many components' %
                        index)

    def __repr__(self):
        """
        Return a human-readable string representing this Api object.
        """
        return '<Productstatus API at %s>' % self._url


class QuerySet(object):
    """
    The QuerySet class facilitates listing and filtering a resource collection.

    Example usage:
    --------------
    qs = api.productinstance.objects  # instantiates a QuerySet
    qs.filter(product=api.product['66340f0b-2c2c-436d-a077-3d939f4f7283'], reference_time=datetime.datetime.now())
    qs.order_by('-version')  # order by version field, descending
    qs.limit(5)  # limit query to 5 results
    qs.count()  # returns total matches, regardless of limit
    qs[2]  # returns the 3rd element matching the criteria
    """

    def __init__(self, api, collection):
        self._api = api
        self._collection = collection
        self._filters = {}
        self._results = {}

    def _relative_item_index(self, index):
        """
        Convert an item's absolute list position to the relative list position
        in self._results['objects']. Returns None if the object is not locally cached.
        """
        if not self._results:
            return None
        offset = self._results['meta']['offset']
        limit = self._results['meta']['limit']
        if index < offset or index >= limit + offset:
            return None
        return index - offset

    def filter(self, **kwargs):
        """
        Add a search constraint and return a reference to self.
        """
        self._results = {}
        [self._add_filter(key, value) for key, value in kwargs.items()]
        return self

    def all(self):
        """
        Deletes all search constraints and return a reference to self.
        """
        self._filters = {}
        return self.filter()

    def order_by(self, *args):
        """
        Apply list ordering. Sorted ascending by default. Prefix member names
        with a minus sign to have descending order.
        """
        return self.filter(order_by=list(args))

    def limit(self, limit):
        """
        Limit the number of results returned from the server.
        """
        return self.filter(limit=int(limit))

    def execute(self):
        """
        Fetch results from the server.
        """
        response = self._api._do_request('get', self._collection._url, params=sorted(self._filters.items()))
        self._results = self._api._get_response_data(response)

    def execute_if_empty(self):
        """
        Ensure there exists some search results.
        """
        if not self._results:
            self.execute()

    def count(self):
        """!
        @brief Return the number of results in the search query.
        """
        self.execute_if_empty()
        return self._results['meta']['total_count']

    def __len__(self):
        """!
        @see count().
        """
        return self.count()

    def _add_filter(self, key, value):
        """
        Add a filter to the search query, serializing if neccessary.
        """
        if isinstance(value, productstatus.api.EvaluatedResource):
            value = value.resource
        if isinstance(value, productstatus.api.Resource):
            if not value.id:
                raise productstatus.exceptions.InvalidFilterDataException(
                    'Trying to filter "%s" by a Productstatus resource, but the resource is not persisted on the backend yet' % key
                )
            self._filters[key] = value.id
        elif isinstance(value, datetime.datetime):
            if not value.tzname():
                raise productstatus.exceptions.InvalidFilterDataException(
                    'Cannot use a naive timestamp for filtering'
                )
            self._filters[key] = value.astimezone(dateutil.tz.tzutc()).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            self._filters[key] = value

    def _dict(self):
        """!
        @brief Return a simple serializable dictionary representation of the entire QuerySet.
        """
        return [x._dict() for x in self]

    def __getitem__(self, index):
        """
        Return the Resource of Nth index in the search results, running a
        remote request if needs be.
        """
        relative_index = self._relative_item_index(index)
        if relative_index is None or not self._results:
            self.filter(offset=index)
            self.execute()
            relative_index = self._relative_item_index(index)
        if relative_index is None:
            raise IndexError('Out of range: %d' % index)
        item = self._results['objects'][relative_index]
        return Resource(self._api, self._collection, item['id'], item)

    def __repr__(self):
        """
        Return a human-readable string representing this query set.
        """
        return '<QuerySet on %s>' % self._collection._url


class ResourceCollection(object):
    """
    The ResourceCollection class is used to retrieve resources from the REST
    API. Resources are accessed using indexes.
    For instance, resource['66340f0b-2c2c-436d-a077-3d939f4f7283'] will return
    a Resource object.
    """

    def __init__(self, api, resource_name):
        self._api = api
        self._resource_name = resource_name
        self._url = productstatus.utils.build_url(self._api._url, self._resource_name)
        self._schema_url = productstatus.utils.build_url(self._url, 'schema')
        self._schema = {}

    def create(self):
        """
        Create a new, temporary Resource object that might be saved, and thus
        stored on the server.
        """
        return Resource(self._api, self, None)

    def find_or_create_ephemeral(self, data, order_by=None, extra_params={}):
        """
        Find or create a resource matching the given parameters in the `data`
        variable. If none is found, one is created, but it is NOT saved to Productstatus.

        @param data data to search for, or to set if nothing is found
        @param order_by ordering
        @param extra_params Extra parameters to insert into the object, without searching for them
        @returns a single Resource object.
        """
        # search for existing
        qs = self.objects
        qs.filter(**data)
        if order_by:
            qs.order_by(order_by)

        # create if not found
        if qs.count() == 0:
            logging.info('No matching %s resource found, creating...' % self._resource_name)
            resource = self.create()
            [setattr(resource, key, value) for key, value in data.items()]
            [setattr(resource, key, value) for key, value in extra_params.items()]
            logging.info('%s: ephemeral resource created' % resource)
        else:
            resource = qs[0]
            logging.info('%s: using existing resource' % resource)

        return resource

    def find_or_create(self, *args, **kwargs):
        """
        Find or create a resource matching the given parameters in the
        `data` variable. If none is found, create one and save it as a new Resource.

        Parameters as ResourceCollection.find_or_create_ephemeral.
        """
        resource = self.find_or_create_ephemeral(*args, **kwargs)
        if not resource.id:
            resource.save()
            logging.info('%s: resource created' % resource)
        return resource

    def _get_schema_from_server(self):
        """
        Retrieve from the server the data model schema for this resource type.
        """
        response = self._api._do_request('get', self._schema_url)
        self._schema = self._api._get_response_data(response)

    def __getitem__(self, id):
        """
        Resource accessor. Will create and return a Resource instance pointing
        to a specific resource. Tries to create the object using an UUID, and
        when that fails, falls back to looking up the item by its slug attribute.
        """
        try:
            uuid_ = uuid.UUID(id)
            return Resource(self._api, self, id)
        except ValueError:
            qs = self.objects.filter(slug=id)
            if qs.count() == 0:
                raise productstatus.exceptions.ResourceNotFoundException(
                    '%s resource with slug "%s" not found.' % (
                        self._resource_name,
                        id,
                    )
                )
            return qs[0]

    def __getattr__(self, name):
        """
        Schema or query set accessor.

        Schema accessor returns a dictionary with the schema for this
        particular resource type. It is retrieved from the server unless it is
        locally cached.

        The query set accessor returns an object which is used to return a list
        of objects.
        """
        if name == 'schema':
            if not self._schema:
                self._get_schema_from_server()
            return self._schema
        elif name == 'objects':
            return QuerySet(self._api, self)

        raise AttributeError('Attribute does not exist: %s' % name)

    def __repr__(self):
        """
        Return a human-readable string representing this resource collection object.
        """
        return '<%s ResourceCollection at %s>' % (self._resource_name, self._url)


class Resource(object):
    """
    The Resource class represents a single REST API resource. All data is
    available as class members. The class members are automatically converted
    to their respective types using the resource schema. For instance,
    timestamps are converted into DateTime objects, integers are proper ints,
    and foreign keys point to other Resource objects.
    """

    def __init__(self, api, collection, id, data={}):
        self._api = api
        self._collection = collection
        self._id = id
        if self._id:
            self._url = productstatus.utils.build_url(self._collection._url, self._id)
        else:
            self._url = None
        self._data = copy.copy(data)
        self._unserialize()

    def save(self):
        """
        Store the locally cached values on the server.
        """
        serialized = self._serialize()
        if self._has_url():
            response = self._api._do_request('put', self._url, data=serialized)
        else:
            response = self._api._do_request('post', self._collection._url, data=serialized)
            self._url = productstatus.utils.build_url(self._api._base_url, response.headers['Location'])
        self._data = {}  # invalidate local cache

    def _has_url(self):
        """
        Returns True if this Resource has an URL which can be accessed at the
        server, False otherwise.
        """
        return self._url is not None

    def _uri(self):
        """!
        @brief Returns the resource URI. Raises an exception if the current
        resource does not have an URL defined.
        """
        if not self._has_url():
            raise productstatus.exceptions.ProductstatusException('Trying to get the object URI without a valid URL')
        return self._url.replace(self._api._base_url, '')

    def _get_resource_from_server(self):
        """
        Fetch the resource from the API server.
        """
        if not self._has_url():
            raise productstatus.exceptions.ProductstatusException('Trying to get an object without a primary key')
        try:
            response = self._api._do_request('get', self._url)
            self._data = self._api._get_response_data(response)
        except productstatus.exceptions.NotFoundException as e:
            raise productstatus.exceptions.ResourceNotFoundException(e)
        self._unserialize()

    def _ensure_complete_object(self):
        """
        Fetch the resource from the API server if we have an URL and it is not
        already cached.
        """
        if self._has_url() and not self._data:
            self._get_resource_from_server()

    def _evaluate_resource_member(self, key):
        """!
        @brief Run lazy evaluation on EvaluatedResource objects.
        """
        if isinstance(self._data[key], EvaluatedResource):
            self._data[key] = self._data[key].resource

    def _dict(self):
        """!
        @brief Return a simple serializable dictionary representation of this Resource.
        """
        self._ensure_complete_object()
        data = {}
        for key in self._data.keys():
            data[key] = self._serialize_member(key)
        return data

    def _serialize(self):
        """
        Return a JSON serialized representation of this resource.
        """
        return json.dumps(self._dict(), sort_keys=True)

    def _serialize_member(self, name):
        """
        Serialize a resource variable into a string, integer, boolean, or null.
        """
        if self._data[name] is None:
            return None

        # Run lazy evaluation
        self._evaluate_resource_member(name)

        description = self._collection.schema['fields'][name]
        type_ = description['type']
        if type_ == 'datetime':
            return self._data[name].strftime('%Y-%m-%dT%H:%M:%S%z')
        elif type_ == 'related' and description['related_type'] == 'to_one':
            return self._data[name].resource_uri
        return self._data[name]

    def _unserialize(self):
        """
        Replace all string members with their proper types.
        """
        for member in self._data.keys():
            self._unserialize_member(member)

    def _unserialize_member(self, name):
        """
        Convert string data into their proper types, according to the resource schema.
        """
        if self._data[name] is None:
            return

        description = self._collection.schema['fields'][name]
        type_ = description['type']
        if type_ == 'integer':
            self._data[name] = int(self._data[name])
        elif type_ == 'datetime':
            self._data[name] = dateutil.parser.parse(self._data[name])
        elif type_ == 'related' and description['related_type'] == 'to_one':
            self._data[name] = self._api[self._data[name]]

    def __getattr__(self, name):
        """
        Attribute accessor. Will load data from the server unless it is cached.
        Enables lazy loading of the resource.
        """
        fields = self._collection.schema['fields']
        if name not in fields:
            raise AttributeError('Attribute does not exist: %s' % name)
        # This value usually comes from the server, but to cut down on requests
        # and make the API client a lot faster when iterating on huge data
        # sets, we generate it here instead.
        if name == 'resource_uri' and name not in self._data:
            return self._uri()
        self._ensure_complete_object()
        if name not in self._data:
            return None
        # Run lazy evaluation
        self._evaluate_resource_member(name)
        return self._data[name]

    def __setattr__(self, name, value):
        """
        Attribute setter. Will store data cached locally until saved using save().
        Will only allow setting variables that can be stored on the server, and
        disallow changing read-only attributes.
        """
        if name[0] == '_':
            return object.__setattr__(self, name, value)
        fields = self._collection.schema['fields']
        if name not in fields:
            raise KeyError('Attribute does not exist: %s' % name)
        if fields[name]['readonly']:
            raise AttributeError('Attribute is read only: %s' % name)
        # FIXME: more tests?
        self._ensure_complete_object()
        self._data[name] = value

    def __repr__(self):
        """
        Return a human-readable string representing this resource object.
        """
        if self._has_url():
            return '<Resource at %s>' % self.resource_uri
        return '<non-persistent %s Resource>' % self._collection._resource_name


class EvaluatedResource(object):
    """!
    @brief Represents a resource that will be lazily evaluated through a
    function. The function is not evaluated until the moment it is saved.
    """
    def __init__(self, function, *args, **kwargs):
        """!
        @param function The function that will be evaluated to return a resource.
        @param args Indexed argument list to the function.
        @param kwargs Named argument list to the function.
        """
        self._resource = None
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @property
    def resource(self):
        """!
        @brief Run the lazy evaluation and return a Resource object.
        """
        if not self._resource:
            self._resource = self.function(*self.args, **self.kwargs)
            if not isinstance(self._resource, Resource):
                raise RuntimeError('Lazy evaluated function "%s" did not return a Resource object.' % self.function.__name__)
        return self._resource


class TastypieApiKeyAuth(requests.auth.AuthBase):
    """
    Django Tastypie requires a special Authorization header format, which is
    implemented by this class.
    """

    def __init__(self, username, api_key):
        self.username = username
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update({'Authorization': 'ApiKey %s:%s' % (self.username, self.api_key)})
        return request
