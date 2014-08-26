# coding=utf-8

import ocr
import os
import yaml
import fuzzy


def pytest_generate_tests(metafunc):
    if 'filename' in metafunc.fixturenames:
        directory = os.path.dirname(os.path.realpath(__file__))
        resources = os.path.join(directory, 'resources', 'ocr')
        files = [f for f in os.listdir(resources) if not f.endswith('.yml')]
        metafunc.parametrize('filename', files)


def t(actual_key, actual_text, expected_text, minimum_ratio=.8):
    if expected_text == '' and actual_text == '':
        return

    ratio, word, start, end = fuzzy.bitap(expected_text, actual_text)

    if ratio < minimum_ratio:
        raise AssertionError("Expected to match %s '%s', but found '%s' (scored: %d)" %
                             (actual_key, expected_text, actual_text, ratio))


def test_run(filename):
    directory = os.path.dirname(os.path.realpath(__file__))
    resource = os.path.join(directory, 'resources', 'ocr', filename)
    name, ext = os.path.splitext(resource)
    with open('%s.yml' % name, 'r') as f:
        expected = yaml.load(f)
    actual = ocr.run(resource, debug=True)

    for actual_key in actual.keys():
        if not actual_key in expected:
            raise AssertionError("Found '%s' but didn't expect" % (actual_key,))

    for expected_key in expected.keys():
        if not expected_key in actual:
            raise AssertionError("Expected '%s' but didn't find" % (expected_key,))

    for actual_key, actual_text in actual.iteritems():
        expected_text = expected[actual_key]

        if isinstance(expected_text, list):
            for expected_element, actual_element in zip(expected_text, actual_text):
                t(actual_key, actual_element, expected_element, minimum_ratio=.65)
        else:
            t(actual_key, actual_text, expected_text)
