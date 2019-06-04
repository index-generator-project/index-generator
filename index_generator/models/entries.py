import os
import mimetypes


class Entry(object):
    def __init__(self, path, root='/'):
        self.name = os.path.basename(path)
        self.mime = mimetypes.guess_type(path)[0]
        self.path = root + path
        self.size = os.path.getsize(path)
        self.modified = os.path.getmtime(path)
