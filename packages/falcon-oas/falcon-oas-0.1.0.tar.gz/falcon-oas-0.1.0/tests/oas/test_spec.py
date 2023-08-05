# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from falcon_oas.oas.spec import create_spec_from_dict
from falcon_oas.oas.spec import get_base_path
from tests.helpers import yaml_load_dedent


def test_spec_deref():
    spec = create_spec_from_dict(
        yaml_load_dedent(
            """\
            a:
              b:
                type: object
            """
        )
    )
    schema = {'$ref': '#/a/b'}

    resolved = spec.deref(schema)
    assert resolved == {'type': 'object'}


def test_spec_deref_without_ref():
    spec = create_spec_from_dict({})
    schema = {'type': 'object'}

    resolved = spec.deref(schema)
    assert resolved is schema


def test_spec_deref_nested():
    spec = create_spec_from_dict(
        yaml_load_dedent(
            """\
            a:
              b:
                $ref: '#/c'
            c:
              type: object
            """
        )
    )
    schema = {'$ref': '#/a/b'}

    resolved = spec.deref(schema)
    assert resolved == {'type': 'object'}


def test_spec_get_operation_parameters():
    spec = create_spec_from_dict(
        yaml_load_dedent(
            """\
            paths:
              /path:
                get:
                  parameters:
                  - name: param1
                    in: query
                  - name: param2
                    in: path
                parameters:
                - name: param1
                  in: query
                  required: true
                - name: param3
                  in: cookie
            """
        )
    )

    operation = spec.get_operation('/path', 'get')
    assert operation['parameters'] == [
        {'name': 'param1', 'in': 'query'},
        {'name': 'param2', 'in': 'path'},
        {'name': 'param3', 'in': 'cookie'},
    ]
    assert 'requestBody' not in operation


def test_spec_get_operation_request_body():
    spec = create_spec_from_dict(
        yaml_load_dedent(
            """\
            paths:
              /path:
                get:
                  requestBody:
                    content: {}
            """
        )
    )

    operation = spec.get_operation('/path', 'get')
    assert operation['parameters'] == []
    assert operation['requestBody'] == {'content': {}}


def test_spec_get_operation_foreign_base_path():
    spec = create_spec_from_dict({'servers': [{'url': '/api'}], 'paths': {}})
    assert spec.get_operation('/path', 'get') is None


def test_spec_get_operation_undocumented_request():
    spec = create_spec_from_dict({})
    assert spec.get_operation('/path', 'get') is None


@pytest.mark.parametrize(
    'spec_dict,expected',
    [
        ({}, ''),
        ({'servers': []}, ''),
        ({'servers': [{'url': '/'}]}, ''),
        ({'servers': [{'url': '/path/'}]}, '/path'),
        ({'servers': [{'url': '/path'}]}, '/path'),
        ({'servers': [{'url': 'http://example.org'}]}, ''),
        ({'servers': [{'url': 'http://example.org/'}]}, ''),
        ({'servers': [{'url': 'http://example.org/path'}]}, '/path'),
        ({'servers': [{'url': 'http://example.org/path/'}]}, '/path'),
        ({'servers': [{'url': '/path1'}, {'url': '/path2'}]}, '/path1'),
    ],
)
def test_base_path(spec_dict, expected):
    assert get_base_path(spec_dict) == expected
