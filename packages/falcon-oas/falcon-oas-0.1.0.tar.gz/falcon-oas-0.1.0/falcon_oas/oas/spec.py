from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from jsonschema import RefResolver

try:
    from functools import lru_cache
except ImportError:  # pragma: no cover
    from functools32 import lru_cache
from six.moves.urllib_parse import urlparse

DEFAULT_SERVER = {'url': '/'}


def create_spec_from_dict(spec_dict, base_path=None):
    return Spec(spec_dict, base_path=base_path)


class Spec(object):
    def __init__(self, spec_dict, base_path=None):
        self.spec_dict = spec_dict
        self.resolver = RefResolver.from_schema(spec_dict)
        self.base_path = (
            base_path if base_path is not None else get_base_path(spec_dict)
        )

    def deref(self, schema):
        while '$ref' in schema:
            _, schema = self.resolver.resolve(schema['$ref'])
        return schema

    @lru_cache(maxsize=None)
    def get_operation(self, full_path, method):
        if not full_path.startswith(self.base_path):
            return None

        path = full_path[len(self.base_path) :]
        try:
            path_item = self.deref(self.spec_dict['paths'][path])
            operation = path_item[method]
        except KeyError:
            return None

        result = operation.copy()
        result['parameters'] = list(
            self._iter_parameters(path_item, operation)
        )
        try:
            result['requestBody'] = self.deref(operation['requestBody'])
        except KeyError:
            pass
        return result

    def _iter_parameters(self, path_item, operation):
        seen = set()
        for spec_dict in (operation, path_item):
            if 'parameters' not in spec_dict:
                continue
            for parameter_spec_dict in spec_dict['parameters']:
                parameter_spec_dict = self.deref(parameter_spec_dict)
                key = (parameter_spec_dict['in'], parameter_spec_dict['name'])
                if key in seen:
                    continue
                seen.add(key)
                yield parameter_spec_dict


def get_base_path(spec_dict):
    try:
        server = spec_dict['servers'][0]
    except (KeyError, IndexError):
        server = DEFAULT_SERVER
    return urlparse(server['url']).path.rstrip('/')
