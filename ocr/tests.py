# coding=utf-8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import ocr
import os
import yaml

from django.test import TestCase
from glob import glob


class FuzzyTest(TestCase):
    def test_partial(self):
        """
        Tests that partial finds best matches
        """
        ratio, word = ocr.fuzzy.partial('Sachverhalt:  Suterent Lichtschacht läuft voll.', 'Sachverhalt')
        self.assertEqual(word, "Sachverhalt")


class OcrTest(TestCase):
    maxDiff = None

    def test_run(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        resources = os.path.join(directory, 'resources')
        files = glob(os.path.join(resources, '*.tiff'))
        for resource in files:
            name, ext = os.path.splitext(resource)
            with open('%s.yml' % name, 'r') as f:
                expected = yaml.load(f)
            actual = ocr.run(resource)
            self.assertEqual(expected, actual)