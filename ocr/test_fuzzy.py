# coding=utf-8

from __future__ import unicode_literals

import ocr
import os

def pytest_generate_tests(metafunc):
    if 'example' in metafunc.fixturenames:
        metafunc.parametrize('example', [
            ('Einsatzmittelliste', 'Einsatzmittelliste'),
            ('Einsazumitttelliste', 'Einsatzmittelliste'),
            ('Sachvehrhalt', 'Sachverhalt'),
            ('Einsatzbeginnsoll', 'Einsatzbeginmsoll'),
            ('Einsatzbeginmsoll', 'Einsatzbeginmsoll'),
            ('Einsatzstichwort', 'Einsalzstiohwort'),
            ('Sachverhalt', 'Sachverhalt'),
            ('Sondersignal', 'Sondersignal'),
            ('Einsatzbeginn(Soll)', 'Einsatzbeginmsoll)'),
            ('Auftragsnummer', 'Auftragsnummer'),
            ('Strasse / Hausnummer', 'Strasse/ Hausnummer'),
            ('Strasse', 'Strasse'),
            ('Segment', 'Segment'),
            ('PLZ / Ort', 'PLZ / Ort'),
            ('Stadt', 'Stadt'),
            ('Region', 'Region'),
            ('Info', 'Info'),
            ('Telefon', 'Telefon'),
        ])

with open(os.path.join(os.path.dirname(__file__), 'resources', 'fuzzy', 'example.txt')) as f:
    content = unicode(f.read(), 'utf-8')

def test_substring(example):
    needle, expected = example
    ratio, word, start, end, = ocr.fuzzy.substring(content, needle)
    assert word == expected
    assert start == content.index(word)
    assert end == content.index(word) + len(word)