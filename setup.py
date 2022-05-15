from setuptools import setup, find_packages
from glob import glob

setup(
    name="python-esdump",
    version="1.0.0",
    author="Ian Panganiban",
    author_email="lkp@noypimaps.com",
    description=("A helper cli for backing up Elasticsearch index."),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'elasticdump=esdumppy.esdumppy:main'
        ]
    },
    install_requires=[
        'fire', 'requests'
    ],
)
