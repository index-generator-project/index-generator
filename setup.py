from setuptools import setup
from index_generator import APP_URL, APP_VERSION, PACKAGE_NAME, LICENSE, AUTHOR, EMAIL, DESCRIPTION

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()

with open('requirements.txt') as f:
    REQUIREMENTS = [l for l in f.read().splitlines() if l]

with open('test_requirements.txt') as f:
    TEST_REQUIREMENTS = [l for l in f.read().splitlines() if l]

setup(
    name=PACKAGE_NAME,
    version=APP_VERSION,
    packages=[
        'index_generator',
        'index_generator.models'
    ],
    package_data={
        'index_generator': ['templates/*/*', 'icons/*/*']
    },
    include_package_data=True,
    url=APP_URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    keywords=['index', 'listing', 'directory'],
    python_requires='>=3.5',
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    setup_requires=["pytest-runner"],
    entry_points={
        'console_scripts': [
            'index-generator=index_generator.__main__:main'
        ]
    }
)
