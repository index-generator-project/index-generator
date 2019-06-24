import sys
from index_generator.__main__ import main
from index_generator import APP_NAME, APP_VERSION, APP_URL


def test_app_version(capfd):
    sys.argv = ['index_generator', '--version']
    main()
    out, _ = capfd.readouterr()
    assert out == APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL + "\n"
    sys.argv = ['index_generator', '-V']
    main()
    out, _ = capfd.readouterr()
    assert out == APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL + "\n"


def test_app_missing_argument(capfd):
    sys.argv = ['index_generator']
    main()
    out, _ = capfd.readouterr()
    assert out == APP_NAME + ' ' + APP_VERSION + ' ' + APP_URL + "\nUsage: index-generator [OPTIONS] PATH.\nSee: index-generator --help\n"


def test_app_template_not_found(capfd):
    sys.argv = ['index_generator', '--template', '/tmp/not_existed', '/tmp']
    main()
    out, _ = capfd.readouterr()
    assert 'IndexGeneratorTemplateNotFound' in out
    sys.argv = ['index_generator', '-T', '/tmp/not_existed', '/tmp']
    main()
    out, _ = capfd.readouterr()
    assert 'IndexGeneratorTemplateNotFound' in out


def test_app_path_not_exists(capfd):
    sys.argv = ['index_generator', '/tmp/not_existed']
    main()
    out, _ = capfd.readouterr()
    assert 'IndexGeneratorPathNotExists' in out
