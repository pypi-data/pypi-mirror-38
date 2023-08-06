#!/usr/bin/env python

from setuptools import setup

import djams

VERSION = djams.__version__

with open('README.md') as f:
    long_description = f.read()

setup(
    name="djams",
    version=VERSION,
    url="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eddy B",
    author_email="",
    license='MIT',
    packages=[
    'djams',
    'djams.migrations',
    ],
    include_package_data=True,
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ],
    keywords='django analytics microsite bindings',
    # project_urls = {
    # 'Source': "",
    # 'Tracker': "",
    # 'Documentation': '',
    # },
    install_requires = ['Django>=2',
                        'python-decouple',
                        'dj-database-url',
                        ],
    python_requires=">=3.5",
    )

