# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='kittycat',
    version='1.0.1',
    description='asyncio REST API Resource database',  # noqa
    long_description='',
    keywords=['asyncio', 'REST', 'Framework', 'transactional'],
    author='David Glick',
    author_email='david@glicksoftware.com',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/plone/kittycat',
    license='BSD',
    zip_safe=True,
    include_package_data=True,
    package_data={'': ['*.txt', '*.rst']},
    packages=find_packages(),
    install_requires=[
        'guillotina',
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'kittycat = kittycat:command_runner',
            'k = kittycat:command_runner'
        ]
    }
)
