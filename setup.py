from setuptools import setup
from index_generator import APP_NAME, APP_URL, APP_VERSION, PACKAGE_NAME

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name=PACKAGE_NAME,
    version=APP_VERSION,
    packages=[
        'index_generator',
        'index_generator.models'
    ],
    package_data={
        'index_generator': ['templates/*/*']
    },
    include_package_data=True,
    url='https://github.com/BruceZhang1993',
    license='MIT',
    author='Bruce Zhang, Edward P',
    author_email='',
    description='Yet another index generator.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['index', 'listing', 'directory'],
    install_requires=requirements,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'index-generator=index_generator.__main__:main'
        ]
    }
)
