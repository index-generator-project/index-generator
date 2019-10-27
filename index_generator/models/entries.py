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

def get_icon_by_mime(mime, iconset='papirus', isDir=False):
    if isDir:
        mime = 'inode/directory'
    if mime:
        segments = mime.split('/')
        valid_targets = [segments[0] + os.path.sep + segments[1], segments[1], segments[0], 'default']
    else:
        valid_targets = ['default']
    for target in valid_targets:
        path = os.path.dirname(__file__) + os.path.sep + '..' + os.path.sep + 'icons' + os.path.sep + iconset + os.path.sep + target + '.svg'
        if os.path.isfile(path):
            return base64.b64encode(open(path, 'rb').read()).decode()

class Entry(object):
    def __init__(self, file, root, base=os.path.sep, human=False, iconset='papirus'):
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
        self.icon = get_icon_by_mime(self.mime, iconset=iconset, isDir=self.isDir)
