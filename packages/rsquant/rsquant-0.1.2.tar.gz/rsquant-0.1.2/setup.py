#!/usr/bin/env python
#
# Copyright 2018 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import (
    find_packages,
    setup,
)

import versioneer

DISTNAME = "rsquant"
DESCRIPTION = """rsQuant is a Python library with \
securities exchange calendars used by Quantopian's Zipline."""
LONG_DESCRIPTION = """rsQuant is a Python library with
securities exchange calendars used by Quantopian's Zipline.

.. _Quantopian Inc: https://www.quantopian.com
.. _Zipline: http://zipline.io
"""

AUTHOR = "Jesse Kuang"
AUTHOR_EMAIL = "jkuang@21cn.com"
URL = ""
LICENSE = "Apache License, Version 2.0"

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "License :: OSI Approved :: Apache Software License",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Operating System :: OS Independent"
]


reqs = [
    "trading_calendars",
    "zipline",
    "numpy",
    "pandas",
    "pytz",
    "toolz",
]


#        data_files=[('rsquant',['rsquant/holidays_cn.txt'])],
if __name__ == '__main__':
    setup(
        name=DISTNAME,
        cmdclass=versioneer.get_cmdclass(),
        version=versioneer.get_version(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        entry_points={
            'console_scripts': [
                'rsquant = rsquant.__main__:main',
            ],
        },
        classifiers=classifiers,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(include='rsquant.*'),
        include_package_date=True,
        package_data={
           'rsquant':['*.txt'],
        },
        install_requires=reqs,
    )
