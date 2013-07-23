# coding=utf-8

from __future__ import unicode_literals

import os
import ocr


def test_partial():
    """
    Tests that partial finds best matches
    """
    ratio, word, start, end = ocr.fuzzy.partial('Sachverhalt:  Suterent Lichtschacht läuft voll.', 'Sachverhalt')
    assert word == "Sachverhalt"


def test_engines():
    with open(os.path.join(os.path.dirname(__file__), 'resources', 'fuzzy', 'test.txt')) as f:
        content = unicode(f.read(), 'utf-8')
    ratio, word, start, end, = ocr.fuzzy.partial(content, 'Einsatzmittelliste')
    assert word is not None
    assert word == 'Einsatzmittelliste'
    assert start == 107
