# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
import ocr
import os

from django.test import TestCase
from glob import glob
from ocr import fuzzy


class FuzzyTest(TestCase):
    def test_partial(self):
        """
        Tests that partial finds best matches
        """
        ratio, word = fuzzy.partial('Sachverhalt:  Suterent Lichtschacht läuft voll.', 'Sachverhalt')
        self.assertEqual(word, "Sachverhalt")


class OcrTest(TestCase):
    maxDiff = None

    def test_run(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        resources = os.path.join(directory, 'resources')
        for resource in glob(os.path.join(resources, '*.tiff')):
            name, ext = os.path.splitext(resource)
            with open('%s.json' % name) as f:
                expected = json.load(f)
            actual = ocr.run(resource)
            self.assertEqual(actual, expected)