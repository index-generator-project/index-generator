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
