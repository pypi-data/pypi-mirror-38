import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = 'Thumbor mongodb lp adapters'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lp_mongodb",
    version="1.2.0",
    author="TechLaProvence",
    description=("Thumbor thumbor lp adapters"),
    license="MIT",
    keywords="thumbor mongodb mongo",
    url="https://github.com/TechLaProvence/lp_mongodb",
    packages=[
        'lp_mongodb',
        'lp_mongodb.storages',
        'lp_mongodb.loaders',
    ],
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'thumbor>=5.0.0',
        'pymongo'
    ]
)
