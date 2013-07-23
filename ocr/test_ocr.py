# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import ocr
import os
import yaml

from glob import glob


def test_partial():
    """
    Tests that partial finds best matches
    """
    ratio, word = ocr.fuzzy.partial('Sachverhalt:  Suterent Lichtschacht läuft voll.', 'Sachverhalt')
    assert word == "Sachverhalt"


def pytest_generate_tests(metafunc):
    if 'resource' in metafunc.fixturenames:
        directory = os.path.dirname(os.path.realpath(__file__))
        resources = os.path.join(directory, 'resources')
        files = glob(os.path.join(resources, '*.tiff'))
        metafunc.parametrize('resource', files)


def test_run(resource):
    name, ext = os.path.splitext(resource)
    with open('%s.yml' % name, 'r') as f:
        expected = yaml.load(f)
    actual = ocr.run(resource)
    assert expected == actual