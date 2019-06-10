from index_generator.models.entries import sizeof_fmt, Entry


def test_sizeof_fmt():
    assert sizeof_fmt(100) == '100 B'
    assert sizeof_fmt(1099) == '1.1 KiB'
    assert sizeof_fmt(1499099) == '1.4 MiB'
    assert sizeof_fmt(2899099001) == '2.7 GiB'


def test_entry():
    entry = Entry('CODE_OF_CONDUCT.md', '.', base='/', human=False)
    assert entry.path == '/CODE_OF_CONDUCT.md'
    assert entry.mime == 'text/markdown'
    assert type(entry.modified) is float
    assert type(entry.size) is int
    assert entry.isDir is False
    assert entry.name == 'CODE_OF_CONDUCT.md'
