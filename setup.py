import json
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


with open(join(dirname(__file__), 'README.md'), mode='r') as readme:
    long_description = readme.read()


with open(join(dirname(__file__), 'src', 'meta.json'), mode='r') as meta:
    meta_info = json.load(meta)


def main():
    setup(
        name=meta_info['name'],
        author=meta_info['author'],
        version=meta_info['version'],
        description=meta_info['description'],
        long_description=long_description,
        long_description_content_type='text/markdown',
        classifiers=[],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=(),
    )


if __name__ == '__main__':
    main()
