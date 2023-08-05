from os import path
from io import open
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="amanita",
    version="0.0.1",
    url="https://github.com/constrict0r/amanita",
    license='MIT',

    author="constrict0r",
    author_email="constrict0r@protonmail.com",

    description="Create python customizable projects",
    long_description=long_description,

    packages=find_packages(exclude=('tests',)),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'amanita = amanita.__main__:main'
        ]
    },

    zip_safe=False,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
