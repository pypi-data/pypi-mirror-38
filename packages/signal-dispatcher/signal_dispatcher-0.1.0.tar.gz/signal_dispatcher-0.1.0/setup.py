"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='signal_dispatcher',
    version='0.1.0',
    description='Simple PyQt signal dispatcher. Used to connect signals with handlers.',
    author='Todor Todorov',
    author_email='todstoychev@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='PyQt5, signals, handlers, signal, handler, dispatcher, dispatch, handle, emit, connect',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['PyQt5', 'sip']
)
