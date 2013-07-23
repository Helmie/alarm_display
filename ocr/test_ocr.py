# coding=utf-8

import ocr
import os
import yaml


def pytest_generate_tests(metafunc):
    if 'resource' in metafunc.fixturenames:
        directory = os.path.dirname(os.path.realpath(__file__))
        resources = os.path.join(directory, 'resources', 'ocr')
        files = [os.path.join(resources, f) for f in os.listdir(resources) if not f.endswith('.yml')]
        metafunc.parametrize('resource', files)


def test_run(resource):
    name, ext = os.path.splitext(resource)
    with open('%s.yml' % name, 'r') as f:
        expected = yaml.load(f)
    actual = ocr.run(resource, debug=True)
    assert expected == actual