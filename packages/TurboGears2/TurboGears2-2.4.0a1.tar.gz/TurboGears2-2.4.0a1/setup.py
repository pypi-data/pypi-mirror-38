import os
here = os.path.abspath(os.path.dirname(__file__))
exec(compile(open(os.path.join(here, 'tg', 'release.py')).read(), 'release.py', 'exec'), globals(), locals())

from setuptools import find_packages, setup

import sys
py_version = sys.version_info[:2]

if py_version < (2, 6):
    raise RuntimeError('TurboGears2 requires Python 2.6 or better')

if py_version[0] == 3 and py_version < (3, 2):
    raise RuntimeError('When using Python3 TurboGears2 requires at least Python3.2')

test_requirements = ['nose',
                     'zope.sqlalchemy >= 0.4',
                     'repoze.who',
                     'repoze.who.plugins.sa >= 1.0.1',
                     'Genshi >= 0.5.1',
                     'Mako',
                     'WebTest',
                     'backlash >= 0.0.7',
                     'raven',
                     'formencode>=1.3.0a1',
                     'tw2.forms',
                     'Beaker',
                     'Kajiki >= 0.4.4']


if py_version == (3, 2):
    # jinja2 2.7 is incompatible with Python 3.2
    test_requirements.append('jinja2 < 2.7')
    # coverage 4.0 is incompatible with Python 3.2
    test_requirements.append('coverage < 4.0')
else:
    test_requirements.append('jinja2')
    test_requirements.append('coverage')

if py_version == (2, 6):
    # SQLAlchemy 1.2+ doesn't support Python 2.6
    test_requirements.append('sqlalchemy < 1.2')
    # Ming 0.5.6+ has 2.7+ syntax
    test_requirements.append('ming < 0.5.6')
else:
    test_requirements.append('sqlalchemy')
    test_requirements.append('ming > 0.5.0')

if py_version[0] == 2:
    test_requirements.extend(['TurboKid >= 1.0.4',
                              'tgming',
                              'tw.forms'])

install_requires=[
    'WebOb >= 1.8.0, < 1.10.0',
    'crank >= 0.8.0, < 0.9.0',
    'repoze.lru'
]

if py_version == (3, 2):
    # markupsafe 0.16 is incompatible with Python 3.2
    install_requires.append('MarkupSafe < 0.16')
else:
    install_requires.append('MarkupSafe')

setup(
    name='TurboGears2',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    keywords='turbogears',
    author=author,
    author_email=email,
    url=url,
    license=license,
    packages=find_packages(exclude=('ez_setup', 'examples', 'tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
       # Used by Travis and Coverage due to setup.py nosetests
       # causing a coredump when used with coverage
       'testing':test_requirements,
    },
    test_suite='nose.collector',
    tests_require = test_requirements,
    entry_points='''
    '''
)
