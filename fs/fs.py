from __future__ import unicode_literals

import os
import uuid

from datetime import datetime


class Repository(object):

    def __init__(self, path):
        self.path = path
        self._new = 'new'
        self._progress = 'progress'
        self._done = 'done'

    @property
    def new(self):
        return os.path.join(self.path, self._new)

    @property
    def progress(self):
        return os.path.join(self.path, self._progress)

    @property
    def done(self):
        return os.path.join(self.path, self._done)

    def _generate_name(self, ext):
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d-%H%M%S')
        uuid_hash = str(uuid.uuid4()).split('-', 1)[0]
        return '{0}-{1}.{2}'.format(timestamp, uuid_hash, ext)

    def next(self):
        """
        Fetches the oldest file from 'new', moves it into 'progress' and returns it.

        :return:
        """
        files = os.listdir(self.new)

        if files:
            def join(basename):
                return os.path.join(self.new, basename)

            oldest = min(files, key=lambda f: os.stat(join(f)).st_mtime)
            source = join(oldest)

            name, ext = os.path.splitext(source)
            basename = self._generate_name(ext)

            target = os.path.join(self.progress, basename)

            # from now on, it's in state progress
            os.rename(source, target)

            return target
        else:
            return None

    def finish(self, document):
        """
        Moves the specified document from 'progress' to 'done'.

        :param document:
        """
        basename = os.path.basename(document)
        source = os.path.join(self.progress, basename)
        target = os.path.join(self.done, basename)
        os.rename(source, target)
