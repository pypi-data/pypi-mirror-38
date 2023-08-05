from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import falcon

from .middlewares.unmarshalers import RequestUnmarshaler
from .oas.exceptions import UnmarshalError
from .oas.parameters.unmarshalers import ParametersUnmarshaler
from .oas.request_body import RequestBodyUnmarshaler
from .oas.schema.unmarshalers import SchemaUnmarshaler
from .oas.schema.validators import SchemaValidator
from .oas.spec import create_spec_from_dict
from .problems import http_error_handler
from .problems import serialize_problem
from .problems import unmarshal_error_handler
from .request import Request
from .routing import generate_routes


def create_api(
    spec_dict, middlewares=None, parsers=None, base_module='', base_path=None
):
    spec = create_spec_from_dict(spec_dict, base_path=base_path)

    request_unmarshaler = create_request_unmarshaler(spec, parsers=parsers)
    api = falcon.API(
        middleware=[request_unmarshaler] + (middlewares or []),
        request_type=Request,
    )
    api.req_options.auto_parse_qs_csv = False
    api.add_error_handler(falcon.HTTPError, http_error_handler)
    api.add_error_handler(UnmarshalError, unmarshal_error_handler)
    api.set_error_serializer(serialize_problem)

    for uri_template, resource in generate_routes(
        spec, base_module=base_module
    ):
        api.add_route(uri_template, resource)
    return api


def create_request_unmarshaler(spec, parsers=None):
    schema_validator = SchemaValidator(spec, parsers=parsers)
    schema_unmarshaler = SchemaUnmarshaler(spec, parsers=parsers)
    parameters_unmarshaler = ParametersUnmarshaler(
        spec, schema_validator, schema_unmarshaler
    )
    request_body_unmarshaler = RequestBodyUnmarshaler(
        spec, schema_validator, schema_unmarshaler
    )
    return RequestUnmarshaler(
        spec, parameters_unmarshaler, request_body_unmarshaler
    )
