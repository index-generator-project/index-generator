import os
import mimetypes


class Entry(object):
    def __init__(self, file, root, base='/'):
        path = root + os.path.sep + file
        self.path = base + path.lstrip('.*/')
        self.name = os.path.basename(path)
        self.mime = mimetypes.guess_type(path)[0]
        self.size = os.path.getsize(path)
        self.modified = os.path.getmtime(path)
        self.isDir = os.path.isdir(path)
