# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


long_description = '''On an average, a person uses 60-90 applications, it’s not fun to enter passwords anymore.
Plus millions of passwords get exposed and accounts get compromised each year.
According to a survey, users admit they reuse the same password because it’s hard to remember them.
Of course, these problems are being addressed in relatively complex ways using 2FA, password managers
and such but a passwordless sign in is much simpler and quicker.'''

setup(
    name='urlauth',
    version='0.0.1',
    author='Arpit Srivastava',
    author_email='arpt.svt@gmail.com',
    packages=find_packages(),
    url='https://rpsingh_IN@bitbucket.org/rpsingh_IN/django-url-auth-package.git',
    license='MIT',
    description='Paswordless authentication',
    long_description=long_description,
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
