# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = "1.0a1"
short_description = "Proxy for remote content"
long_description = "\n\n".join([
    open('README.rst').read(),
    open('CHANGES.rst').read()
])


setup(
    name='collective.proxytype',
    version=version,
    description=short_description,
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Johannes Raggam',
    author_email='thetetet@gmail.com',
    url='https://pypi.python.org/pypi/collective.proxytype',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.contentmenu',
        'plone.app.dexterity',
        'requests',
        'lxml',
        # 'beautifulsoup4',
        'setuptools',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
