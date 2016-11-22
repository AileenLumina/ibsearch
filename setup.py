from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(
    name='ibsearch',

    version='1.3.0',

    description='Api wrapper for ibsear.ch and ibsearch.xxx',
    long_description=long_description,

    url='https://github.com/aileenlumina/ibsearch',

    author='aileenlumina',
    author_email='username"example.com', # I don´t know this

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: API Wrapper',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4+',
    ],
    py_modules=["ibsearch"],
    keywords='ibsearch api wrapper',
)