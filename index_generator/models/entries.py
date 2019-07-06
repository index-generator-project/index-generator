import os
import mimetypes
import base64


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            if unit == '':
                return '%3.0f %s%s' % (num, unit, suffix)
            else:
                return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024.0
    return '%.1f %s%s' % (num, 'Yi', suffix)


class Entry(object):
    def __init__(self, file, root, base=os.path.sep, human=False, iconset='material'):
        path = root + os.path.sep + file
        self.path = base + path.lstrip('.*' + os.path.sep)
        self.name = os.path.basename(path)
        self.mime = mimetypes.guess_type(path)[0]
        if human:
            self.size = sizeof_fmt(os.path.getsize(path))
        else:
            self.size = os.path.getsize(path)
        self.modified = os.path.getmtime(path)
        self.isDir = os.path.isdir(path)
        iconFile = 'file.svg'
        if self.isDir:
            iconFile = 'folder-cluster.svg'
        with open(os.path.dirname(__file__) + os.path.sep + '..' + os.path.sep + 'icons' + os.path.sep + iconset + os.path.sep + iconFile, 'rb') as f:
            self.icon = base64.b64encode(f.read()).decode()
