# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the SpinDrops_ Sphinx_ extension.

.. _SpinDrops: https://spindrops.org
.. _Sphinx: http://sphinx.pocoo.org/
.. _DROPS: https://doi.org/10.1103/PhysRevA.91.042122

SpinDrops_ is a program and a reStructuredText_ directive to allow embededed
DROPS_ figures to be rendered as nice images in sphinx documentation. The
``drops`` directive takes a number of options to control the generated images.

This extension adds the ``drops`` directive that generates a DROPS_
image, and a ``pton`` directive that converts plain-text operator
notation into nicely formatted math display.

Usage example::

    .. drops:: I1z
       :nspin: 1; v1=1

'''

requires = ['Sphinx>=1.7']

setup(
    name='sphinxcontrib-spindrops',
    version='2.0',
    url='https://gitlab.com/tesch1/sphinxcontrib-spindrops',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-spindrops',
    license='GPL',
    author='Michael Tesch',
    author_email='tesch1@gmail.com',
    description='SpinDrops Sphinx extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
