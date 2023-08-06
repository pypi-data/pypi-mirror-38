from dateutil.parser import parse as parse_date


class DictProxy(object):
    def __init__(self, request, data):
        self.__request = request
        self.__data = data

    def __getattr__(self, attr):
        try:
            return self.__data[attr]
        except KeyError:
            raise AttributeError(
                '\'%s\' has no attribute \'%s\'' % (
                    type(self).__name__,
                    attr
                )
            )


class AttributeProxy(object):
    def __init__(self, request, name):
        self.__locked = True
        self.__request = request
        self.__name = name
        self.__populated = False
        self.__value = None

    def __getvalue__(self):
        if not self.__populated:
            self.__request.__populate__()

        return self.__value

    def __setvalue__(self, value):
        self.__value = value
        self.__populated = True

    def __abs__(self):
        return self.__getvalue__().__abs__()

    def __and__(self, other):
        return self.__getvalue__().__and__(other)

    def __bool__(self):
        return self.__getvalue__().__bool__()

    def __ceil__(self):
        return self.__getvalue__().__ceil__()

    def __cmp__(self, other):
        return self.__getvalue__().__cmp__(other)

    def __dir__(self):
        return self.__getvalue__().__dir__()

    def __doc__(self):
        return self.__getvalue__().__doc__()

    def __eq__(self, other):
        return self.__getvalue__() == other

    def __float__(self):
        return self.__getvalue__().__float__()

    def __floor__(self):
        return self.__getvalue__().__floor__()

    def __format__(self, f):
        return self.__getvalue__().__format__(f)

    def __ge__(self, other):
        return self.__getvalue__() >= other

    def __get__(self, key):
        return self.__getvalue__().__get__(key)

    def __gt__(self, other):
        return self.__getvalue__() > other

    def __hash__(self):
        return self.__getvalue__().__hash__()

    def __int__(self):
        return int(self.__getvalue__())

    def __le__(self, other):
        return self.__getvalue__() <= other

    def __len__(self):
        return len(self.__getvalue__())

    def __lt__(self, other):
        return self.__getvalue__() < other

    def __ne__(self, other):
        return self.__getvalue__() != other

    def __or__(self, other):
        return self.__getvalue__() or other

    def __pos__(self):
        return self.__getvalue__().__pos__()

    def __repr__(self):
        return self.__getvalue__().__repr__()

    def __round__(self, *args):
        return self.__getvalue__().__round__(*args)

    def __str__(self):
        return str(self.__getvalue__())

    def __getattr__(self, attr):
        value = self.__getvalue__()
        return getattr(value, attr)

    def __call__(self, **kwargs):
        path = '%s%s/' % (self.__request.path, self.__name)
        return self.__request.client.post(path, kwargs)

    def to(self, totype):
        try:
            converter = {
                'str': str,
                'unicode': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'tuple': tuple,
                'set': set,
                'dict': dict,
                'date': parse_date,
                'datetime': parse_date
            }[totype]
        except KeyError:
            raise TypeError('Unknown type: \'%s\'', totype)

        return converter(self.__getvalue__())


class ObjectProxy(object):
    def __init__(
        self,
        client, path, query={},
        kind=None, id=None, attributes=None, links=None, meta=None
    ):
        self.client = client
        self.path = path
        self.query = query
        self.__id = id
        self.__kind = kind
        self.__cache = {}
        self.__attributes = attributes if attributes is not None else {}

        if id is not None:
            self.id = id

        if links is not None:
            cls_name = '%sLinkCollection' % (
                kind.replace('-', ' ').title().replace(' ', '')
            )

            cls = type(
                cls_name,
                (DictProxy,),
                {}
            )

            self.links = cls(self, links)

        if meta is not None:
            cls_name = '%sMetaCollection' % (
                kind.replace('-', ' ').title().replace(' ', '')
            )

            cls = type(
                cls_name,
                (DictProxy,),
                {}
            )

            self.meta = cls(self, meta)

    def __repr__(self):
        if self.__id is not None:
            return '<%s %s>' % (
                type(self).__name__,
                self.__id
            )

        return '<%s>' % type(self).__name__

    def __str__(self):
        return self.__repr__()

    def dict(self):
        if self.__id is None or self.__kind is None:
            self.__populate__()

        if self.__id is None:
            raise AttributeError(
                '\'%s\' has no attribute \'dict\'' % (
                    type(self).__name__
                )
            )

        d = dict(**self.__attributes)
        d['id'] = self.id

        return d

    def all(self):
        return self.filter()

    def filter(self, id=None, **kwargs):
        if id:
            Model = type(self)
            path = '%s%s/' % (self.path, id)
            return Model(self.client, path)

        query = dict(**self.query)
        for key, value in kwargs.items():
            query['filter[%s]' % key] = value

        return self.client.get(self.path, **query)

    def __getattr__(self, attr):
        if attr in ('links', 'meta'):
            if self.__id is None and self.__kind is None:
                self.__populate__()

            return getattr(self, attr)

        if attr not in self.__cache:
            jsonapi_version = attr.replace('_', '-')
            self.__cache[attr] = AttributeProxy(self, jsonapi_version)

            if jsonapi_version in self.__attributes:
                self.__cache[attr].__setvalue__(
                    self.__attributes[jsonapi_version]
                )

        return self.__cache[attr]

    def __populate__(self):
        if self.__id is not None or self.__kind is not None:
            return

        data = self.client.load(self.path, **self.query)
        self.__kind = data['type']
        self.__id = data['id']
        self.__attributes = data['attributes']
        self.id = data['id']

        for jsonapi_version, value in data['attributes'].items():
            python_version = jsonapi_version.replace('-', '_')
            if python_version not in self.__cache:
                self.__cache[python_version] = AttributeProxy(
                    self, jsonapi_version
                )

            self.__cache[python_version].__setvalue__(value)

        cls_name = '%sLinkCollection' % (
            data['type'].replace('-', ' ').title().replace(' ', '')
        )

        cls = type(
            cls_name,
            (DictProxy,),
            {}
        )

        self.links = cls(self, data['links'])

        cls_name = '%sMetaCollection' % (
            data['type'].replace('-', ' ').title().replace(' ', '')
        )

        cls = type(
            cls_name,
            (DictProxy,),
            {}
        )

        self.meta = cls(self, data.get('meta'))
