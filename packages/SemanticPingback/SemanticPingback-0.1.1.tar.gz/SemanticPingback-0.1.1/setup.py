"""
SemanticPingback
----------------

This is a python library to make your server a SemanticPingback endpoint.

You will find more information about SemanticPingback here: https://aksw.github.io/SemanticPingback/
"""
from setuptools import setup


setup(
    name='SemanticPingback',
    version='0.1.1',
    url='https://github.com/AKSW/SemanticPingbackPy',
    license='MIT',
    author='Natanael Arndt',
    author_email='arndtn@gmail.com',
    description='SemanticPingback Server Library for Python',
    long_description=__doc__,
    py_modules=['semanticpingback'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'rdflib'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
