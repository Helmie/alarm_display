"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import fs
import os
import shutil
import tempfile

from django.test import TestCase


class RepositoryTest(TestCase):

    def setUp(self):
        tmpdir = tempfile.mkdtemp()
        self.repo = fs.Repository(tmpdir)

        directory = os.path.dirname(__file__)
        resources = os.path.join(directory, 'resources')

        self.resources = os.listdir(resources)

        shutil.copytree(resources, self.repo.new)
        os.mkdir(self.repo.progress)
        os.mkdir(self.repo.done)

    def tearDown(self):
        shutil.rmtree(self.repo.path)

    @property
    def new(self):
        return len(os.listdir(self.repo.new))

    @property
    def progress(self):
        return len(os.listdir(self.repo.progress))

    @property
    def done(self):
        return len(os.listdir(self.repo.done))

    def test_start(self):
        assert self.new
        assert not self.progress

        while self.new:
            new_before = self.new
            progress_before = self.progress

            self.repo.next()

            new_after = self.new
            progress_after = self.progress

            assert new_before - 1 == new_after
            assert progress_before + 1 == progress_after

        assert not self.new
        assert self.progress

    def test_finish(self):
        documents = []
        while self.new:
            documents.append(self.repo.next())

        assert self.progress
        assert not self.done

        for document in documents:
            progress_before = self.progress
            done_before = self.done

            self.repo.finish(document)

            progress_after = self.progress
            done_after = self.done

            assert progress_before - 1 == progress_after
            assert done_before + 1 == done_after

        assert not self.progress
        assert self.done
