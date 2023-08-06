# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


description = ("A django package that allows url authentication")

setup(
    name='urlauth',
    version='0.1.1',
    author='Arpit Srivastava, Rohit Prakashs Singh',
    author_email='arpt.svt@gmail.com, rohitprakashsingh21@gmail.com',
    packages=find_packages(),
    url='https://rpsingh_IN@bitbucket.org/rpsingh_IN/django-url-auth-package.git',
    license='MIT',
    description=description,
    long_description='Provides a unique url that enables users to sign in without a password',
    install_requires=['django', 'PyJWT'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
