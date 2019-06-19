import sys
from index_generator.__main__ import main
from index_generator import *


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
