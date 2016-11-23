from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(
    name='ibsearch',
    version='0.9',
    description='API wrapper for IbSearch.',
    long_description=long_description,
    url='https://github.com/AileenLumina/ibsearch',
    author='AileenLumina',
    author_email='aileenfromthemoon@gmail.com',
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