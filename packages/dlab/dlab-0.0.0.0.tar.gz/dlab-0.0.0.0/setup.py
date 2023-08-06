#! /usr/bin/env python
# -*- coding: utf-8 -*_
# Author: Liu Yang <mkliuyang@gmail.com>

from distutils.core import setup

setup(
    name='dlab',
    version='0.0.0.0',
    description='Just do laboratory',
    author='Liu Yang',
    author_email='mkliuyang@gmail.com',
    url='',
    packages=['dlab'],
    install_requires=[
        'numpy>=1.14.0',
        'torch>=0.4.1',
        'torchvision'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
